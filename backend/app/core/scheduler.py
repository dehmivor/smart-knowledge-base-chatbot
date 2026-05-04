import logging
import asyncio
from datetime import datetime, timedelta
from typing import Callable, Coroutine, Any
from sqlalchemy.orm import Session
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.models.database import SessionLocal, CronJob, CronJobLog
import functools

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- CẤU HÌNH ---
MAX_RETRIES = 3
LOCK_TIMEOUT_MINUTES = 30 # Tự động giải phóng lock sau 30 phút nếu job bị crash

async def robust_job_wrapper(job_id: str, func: Callable[..., Coroutine[Any, Any, Any]]):
    """
    Wrapper đảm bảo tuân thủ 5 bước xử lý chuẩn:
    1. Kiểm tra Lock
    2. Cập nhật trạng thái sang processing
    3. Thực hiện Logic nghiệp vụ
    4. Cập nhật completed/failed và giải phóng Lock
    5. Ghi log lịch sử
    """
    db: Session = SessionLocal()
    start_time = datetime.utcnow()
    
    try:
        # 1. KIỂM TRA LOCK (Concurrency Control)
        job = db.query(CronJob).filter(CronJob.id == job_id).first()
        
        if not job:
            job = CronJob(id=job_id, status="pending")
            db.add(job)
            db.commit()
            db.refresh(job)

        # Kiểm tra xem có đang bị khóa không (Locker Mechanism)
        if job.status == "processing" and job.lock_until and job.lock_until > datetime.utcnow():
            logger.warning(f"Job {job_id} is already running (Locked until {job.lock_until}). Skipping...")
            return

        # 2. CẬP NHẬT TRẠNG THÁI (Mark as Processing)
        job.status = "processing"
        job.last_run = start_time
        job.lock_until = start_time + timedelta(minutes=LOCK_TIMEOUT_MINUTES)
        db.commit()

        logger.info(f"[{start_time}] Starting job: {job_id}")

        # 3. THỰC HIỆN LOGIC NGHIỆP VỤ
        try:
            await func()
            
            # 4. CẬP NHẬT TRẠNG THÁI THÀNH CÔNG
            job.status = "completed"
            job.retry_count = 0 # Reset retry
            message = "Success"
        except Exception as e:
            # 5. XỬ LÝ LỖI VÀ THỬ LẠI (Retry & Error Handling)
            job.retry_count += 1
            if job.retry_count > MAX_RETRIES:
                job.status = "failed" # Dead Letter Queue (DLQ) logic
                message = f"Failed after {MAX_RETRIES} retries. Error: {str(e)}"
                logger.error(f"Job {job_id} moved to DLQ (failed).")
            else:
                job.status = "pending" # Sẽ chạy lại ở lần sau
                message = f"Error: {str(e)}. Retry count: {job.retry_count}"
                logger.warning(f"Job {job_id} failed, will retry. Error: {str(e)}")
            
            raise e # Re-raise để ghi log ra console

        finally:
            # Giải phóng lock và ghi log
            job.lock_until = None
            end_time = datetime.utcnow()
            
            log = CronJobLog(
                job_id=job_id,
                status=job.status,
                message=message,
                start_time=start_time,
                end_time=end_time
            )
            db.add(log)
            db.commit()
            
            logger.info(f"Job {job_id} finished with status: {job.status}")

    except Exception as e:
        logger.error(f"Critical error in scheduler wrapper for {job_id}: {str(e)}")
    finally:
        db.close()

# --- CÁC TÁC VỤ CỤ THỂ ---

async def build_new_feature_logic():
    """
    Logic thực tế để 'xây thêm chức năng'.
    Ở đây bạn có thể implement lấy dữ liệu theo Batch (Bước 2 trong quy tắc).
    """
    # GIẢ LẬP XỬ LÝ BATCH
    batch_size = 100
    logger.info(f"Processing batch of {batch_size} records...")
    
    # Giả lập thời gian xử lý
    await asyncio.sleep(5) 
    
    # throw error ngẫu nhiên để test retry (optional)
    # import random
    # if random.random() < 0.3: raise Exception("Random logic error!")

# --- KHỞI CHẠY SCHEDULER ---

def start_scheduler():
    scheduler = AsyncIOScheduler(timezone="UTC") # Sử dụng UTC (Quy tắc lưu ý hạ tầng)
    
    # Đăng ký job với wrapper bảo vệ
    scheduler.add_job(
        robust_job_wrapper, 
        'interval', 
        hours=2, 
        args=["build_new_feature", build_new_feature_logic],
        id="build_new_feature_job"
    )
    
    scheduler.start()
    logger.info("Professional Scheduler started with UTC timezone.")
    return scheduler
