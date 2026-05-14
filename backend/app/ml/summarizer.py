import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

async def summarize(text: str) -> str:
    """
    Hàm gọi API tóm tắt văn bản từ server AI của đối tác.
    """
    if not text:
        return "Nội dung bài báo trống."
    
    try:
        # Sử dụng httpx để tạo async request
        async with httpx.AsyncClient() as client:
            # Gửi method POST tới URL với JSON body như đối tác yêu cầu
            response = await client.post(
                settings.ai_api_url, 
                json={"text": text}, 
                timeout=200.0 # Timeout 60s chờ model xử lý
            )
            
            # Quăng lỗi nếu HTTP status không phải 200 OK
            response.raise_for_status() 
            
            data = response.json()
            
            # --- QUAN TRỌNG ---
            # Giả định API của đối tác trả về object: {"summary": "nội dung tóm tắt..."}
            # Nếu họ dùng key khác (ví dụ "result", "data"), bạn cần đổi chữ "summary" ở dòng dưới cho khớp.
            return data.get("summary", "Không tìm thấy nội dung tóm tắt từ server.")

    except httpx.RequestError as exc:
        logger.error(f"Lỗi mạng khi gọi API AI: {exc}")
        return f"Lỗi kết nối tới server AI."
    except httpx.HTTPStatusError as exc:
        logger.error(f"Lỗi từ server AI (Status {exc.response.status_code}): {exc.response.text}")
        return f"Server AI gặp lỗi trong quá trình xử lý."