import httpx

async def summarize(text: str) -> str:
    """
    Hàm gọi API tóm tắt văn bản.
    Hiện tại là Mock. Khi nhóm AI làm xong API, chỉ cần thay đổi cấu hình URL ở đây.
    """
    if not text:
        return "Nội dung bài báo trống."
    
    # === [MẪU CODE GỌI API THẬT SAU NÀY] ===
    # AI_API_URL = "http://ai-team-server.com/api/summarize"
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(AI_API_URL, json={"text": text}, timeout=60.0)
    #     response.raise_for_status()
    #     return response.json().get("summary")
    
    # Mock return hiện tại
    snippet = text[:100].replace("\n", " ") + "..." if len(text) > 100 else text
    return f"[MOCK API SUMMARY] Đây là tóm tắt nhận được từ API giả lập. Trích đoạn: {snippet}"

