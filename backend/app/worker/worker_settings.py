"""ARQ Worker settings — chạy bằng: arq app.worker.worker_settings.WorkerSettings

Worker này listen trên Redis queue và xử lý các background tasks
(text extraction, AI summarization) mà KHÔNG block HTTP request.
"""
from arq.connections import RedisSettings

from app.core.config import settings
from app.worker.tasks import process_paper_task


def _parse_redis_url(url: str) -> RedisSettings:
    """Parse redis:// URL thành RedisSettings."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    
    # Kiểm tra xem URL có yêu cầu bảo mật SSL/TLS không (Upstash hoặc External Redis)
    use_ssl = parsed.scheme == "rediss"
    
    return RedisSettings(
        host=parsed.hostname or "localhost",
        port=parsed.port or 6379,
        password=parsed.password,
        database=int(parsed.path.lstrip("/") or 0),
        ssl=use_ssl,
    )


class WorkerSettings:
    """ARQ Worker Configuration."""

    # Danh sách functions mà worker sẽ xử lý
    functions = [process_paper_task]

    # Redis connection
    redis_settings = _parse_redis_url(settings.redis_url)

    # Retry config
    max_tries = 3                # Tối đa 3 lần retry
    job_timeout = 600            # Timeout 10 phút cho mỗi job
    health_check_interval = 30   # Health check mỗi 30s

    # Queue name
    queue_name = "paper_processing"
