from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    APP_NAME: str = "Smart Knowledge Base Chatbot"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/sql_app.db"
    
    # OpenAI (Sẽ dùng ở Phase 2 & 3)
    OPENAI_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHAT_MODEL: str = "gpt-4o-mini"
    
    # Vector DB (Milvus)
    MILVUS_URI: str = os.path.join(os.getcwd(), "milvus_demo.db")
    COLLECTION_NAME: str = "document_chunks"
    
    # Storage
    UPLOAD_DIR: str = "uploads"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# Đảm bảo các thư mục tồn tại
os.makedirs("data", exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
