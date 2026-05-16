import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class SummarizationError(Exception):
    """Lỗi xảy ra khi gọi API AI tóm tắt không thành công."""
    pass


async def summarize(text: str) -> str:
    """
    Gọi API tóm tắt văn bản từ server AI.
    
    Raises:
        SummarizationError: Khi API trả lỗi hoặc không kết nối được.
        ValueError: Khi nội dung đầu vào trống.
    """
    if not text or not text.strip():
        raise ValueError("Nội dung bài báo trống, không thể tóm tắt.")
    
    api_endpoint = f"{settings.ai_api_url.rstrip('/')}/summarize"
    
    headers = {
        "Content-Type": "application/json"
    }
    if settings.hf_token:
        headers["Authorization"] = f"Bearer {settings.hf_token}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_endpoint, 
                json={"text": text}, 
                headers=headers,
                timeout=300.0  # Timeout 300s chờ model xử lý
            )
            
            response.raise_for_status()
            
            data = response.json()
            summary = data.get("summary")
            
            if not summary or not summary.strip():
                raise SummarizationError(
                    "Server AI trả về kết quả trống. Có thể nội dung quá ngắn hoặc không hỗ trợ."
                )
            
            return summary

    except httpx.ConnectError as exc:
        logger.error("Không thể kết nối tới server AI tại %s: %s", api_endpoint, exc)
        raise SummarizationError(
            f"Không thể kết nối tới server AI ({api_endpoint}). Kiểm tra lại URL hoặc server đã hoạt động chưa."
        ) from exc
    
    except httpx.TimeoutException as exc:
        logger.error("Timeout khi gọi API AI: %s", exc)
        raise SummarizationError(
            "Server AI phản hồi quá chậm (timeout 300s). Thử lại sau hoặc dùng bài báo ngắn hơn."
        ) from exc
    
    except httpx.HTTPStatusError as exc:
        status_code = exc.response.status_code
        detail = exc.response.text[:200] if exc.response.text else "Không có chi tiết"
        logger.error("Server AI trả lỗi HTTP %d: %s", status_code, detail)
        raise SummarizationError(
            f"Server AI trả lỗi HTTP {status_code}: {detail}"
        ) from exc
    
    except httpx.RequestError as exc:
        logger.error("Lỗi mạng khi gọi API AI: %s", exc)
        raise SummarizationError(
            f"Lỗi mạng khi kết nối tới server AI: {str(exc)[:200]}"
        ) from exc