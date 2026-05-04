import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# Đảm bảo thư mục data tồn tại để chứa file SQLite
os.makedirs("data", exist_ok=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DocumentMetadata(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    file_type = Column(String)
    chunk_count = Column(Integer)
    upload_date = Column(DateTime, default=datetime.datetime.utcnow)

class CronJob(Base):
    __tablename__ = "cron_jobs"
    id = Column(String, primary_key=True)
    status = Column(String, default="pending") # pending, processing, completed, failed
    last_run = Column(DateTime)
    lock_until = Column(DateTime)
    retry_count = Column(Integer, default=0)

class CronJobLog(Base):
    __tablename__ = "cron_job_logs"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String)
    status = Column(String)
    message = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

# Tạo bảng trong database
Base.metadata.create_all(bind=engine)

# Dependency để lấy DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
