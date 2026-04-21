from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import documents # Thêm dòng này
app = FastAPI(title="Smart Knowledge Base Chatbot API")

# Cấu hình CORS để Frontend (Vue) có thể gọi được Backend (FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Trong thực tế sẽ giới hạn domain, nhưng demo thì để * cho tiện
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to Smart Knowledge Base Chatbot API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    import os
    import sys
    
    # Ép Python nhận diện thư mục hiện tại là gốc để tìm module 'app'
    sys.path.append(os.getcwd())
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
