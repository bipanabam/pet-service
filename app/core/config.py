from pydantic_settings import BaseSettings

from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    APP_NAME: str = "Digital Pet World"
    DEBUG: bool = False
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "myapp_db"
    DATABASE_URL: str
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
config = Config()