from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    debug: bool = True

    @property
    def database_url(self):
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )

    class Config:
        env_file = os.getenv("ENV_FILE", ".env.dev")


settings = Settings()
