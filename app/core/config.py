from pydantic_settings import BaseSettings

from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    APP_NAME: str = "Digital Pet World"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    ENV: str = "prod"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "myapp_db"
    DATABASE_URL: str
    
    APPWRITE_ENDPOINT: str
    APPWRITE_PROJECT_ID: str
    APPWRITE_API_KEY: str
    APPWRITE_DATABASE_ID: str
    APPWRITE_USER_COLLECTION_ID: str
    APPWRITE_PAIR_COLLECTION_ID: str
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
config = Config()