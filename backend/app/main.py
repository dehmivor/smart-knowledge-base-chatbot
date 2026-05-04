import os
import sys

# Thêm thư mục hiện tại vào sys.path để Python tìm thấy package 'app'
sys.path.append(os.getcwd())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import documents, chat
from app.config import settings
from app.core.scheduler import start_scheduler

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# ... (CORS logic giữ nguyên)

# Include các router
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    # Khởi chạy scheduler khi app bắt đầu
    app.state.scheduler = start_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    # Dừng scheduler khi app tắt
    app.state.scheduler.shutdown()

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health", tags=["Root"])
async def health_check():
    return {"status": "healthy", "service": settings.APP_NAME}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


