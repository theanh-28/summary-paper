"""Background tasks — xử lý text extraction + AI summarization trong worker.

Task flow:
1. Upload API tạo record (status=uploaded), enqueue task
2. Worker pick task → status=processing
3. Download file từ Supabase → Extract text (giữ trong RAM, KHÔNG lưu DB)
4. Gọi AI summarizer → Lưu summary
5. Update status=completed (hoặc failed nếu lỗi)
"""
from __future__ import annotations

import logging
import os
import tempfile
import time

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.ml.summarizer import summarize
from app.models.paper import Paper
from app.models.summary import Summary
from app.utils.pdf_utils import extract_text_from_pdf
from app.utils.docx_utils import extract_text_from_docx

from sqlalchemy import select

logger = logging.getLogger(__name__)


async def process_paper_task(ctx: dict, paper_id: int) -> dict:
    """
    Background task: extract text từ uploaded file, gọi AI summarizer, lưu kết quả.
    
    Extracted text chỉ tồn tại trong RAM (biến Python), KHÔNG lưu vào database
    để tiết kiệm dung lượng. File gốc vẫn nằm trên Supabase nếu cần re-process.
    """
    logger.info("Worker starting task for paper_id=%s", paper_id)
    start_time = time.time()

    async with AsyncSessionLocal() as db:
        try:
            # 1. Lấy paper từ DB
            result = await db.execute(select(Paper).where(Paper.id == paper_id))
            paper = result.scalar_one_or_none()
            if not paper:
                logger.error("Paper %s not found", paper_id)
                return {"status": "error", "message": "Paper not found"}

            # 2. Cập nhật trạng thái → processing
            paper.status = "processing"
            await db.commit()

            # 3. Extract text từ file (download từ Supabase, giữ trong RAM)
            extracted_text = ""

            if paper.storage_path and paper.file_url:
                file_ext = os.path.splitext(paper.storage_path)[1].lower() if "." in paper.storage_path else ""

                from app.storage.supabase_storage import download_file_from_storage
                file_bytes = await download_file_from_storage(paper.storage_path)
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
                    tmp.write(file_bytes)
                    tmp_path = tmp.name
                
                try:
                    if file_ext == ".pdf":
                        extracted_text, _ = extract_text_from_pdf(tmp_path)
                    elif file_ext == ".docx":
                        extracted_text, _ = extract_text_from_docx(tmp_path)
                    elif file_ext == ".txt":
                        with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                            extracted_text = f.read()
                finally:
                    os.unlink(tmp_path)
            else:
                raise FileNotFoundError(f"No storage_path for paper {paper_id}")

            if not extracted_text.strip():
                paper.status = "failed"
                paper.error_message = "Không thể trích xuất nội dung từ file."
                await db.commit()
                return {"status": "failed", "message": "Empty content"}

            # 4. Gọi AI Summarizer (extracted_text chỉ tồn tại trong RAM)
            logger.info("Calling AI summarizer for paper_id=%s (content length: %d)", paper_id, len(extracted_text))
            generated_summary = await summarize(extracted_text)

            # 5. Lưu summary vào DB
            summary = Summary(paper_id=paper_id, content=generated_summary)
            db.add(summary)

            # 6. Update paper status → completed
            end_time = time.time()
            processing_time = int(end_time - start_time)
            paper.status = "completed"
            paper.processing_time_seconds = processing_time
            paper.error_message = ""

            await db.commit()

            logger.info(
                "Paper %s processed successfully in %ds",
                paper_id, processing_time
            )
            return {"status": "completed", "paper_id": paper_id, "processing_time": processing_time}

        except Exception as e:
            logger.error("Failed to process paper %s: %s", paper_id, str(e), exc_info=True)
            try:
                result = await db.execute(select(Paper).where(Paper.id == paper_id))
                paper = result.scalar_one_or_none()
                if paper:
                    paper.status = "failed"
                    paper.error_message = str(e)[:500]
                    await db.commit()
            except Exception:
                logger.error("Failed to update paper status to failed", exc_info=True)

            return {"status": "failed", "paper_id": paper_id, "error": str(e)}
