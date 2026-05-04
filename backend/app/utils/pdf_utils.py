import logging
import os
from pypdf import PdfReader

logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_path: str) -> str:
    """
    Trích xuất toàn bộ văn bản từ một file PDF.
    
    Args:
        file_path (str): Đường dẫn tới file PDF.
        
    Returns:
        str: Nội dung text trích xuất được.
        
    Raises:
        FileNotFoundError: Nếu file không tồn tại.
        ValueError: Nếu file bị lỗi hoặc không thể đọc.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File không tồn tại: {file_path}")
        
    text_content = []
    try:
        reader = PdfReader(file_path)
        
        # Nếu file có password, có thể cần xử lý ở đây
        if reader.is_encrypted:
            logger.warning(f"File PDF {file_path} bị mã hóa. Có thể không đọc được nội dung.")
            
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                text_content.append(text)
                
        return "\n".join(text_content)
    except Exception as e:
        logger.error(f"Lỗi khi đọc file PDF {file_path}: {str(e)}")
        raise ValueError(f"Không thể trích xuất văn bản từ PDF: {str(e)}")
