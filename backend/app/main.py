from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import psycopg
import io
from app.routers import auth, agreements, utils
from app.services.storage_service import storage_service

app = FastAPI(
    title="Agreemate API",
    description="Legal document automation platform with eSign/eStamp integration",
    version="1.0.0"
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth.router)
app.include_router(agreements.router)
app.include_router(utils.router)

@app.get("/healthz")
async def healthz():
    return {"status": "ok", "message": "Agreemate API is running"}

@app.get("/files/{file_key}")
async def download_file(file_key: str):
    file_content = storage_service.get_file(file_key)
    if not file_content:
        return {"error": "File not found"}
    
    metadata = storage_service.get_file_metadata(file_key)
    content_type = metadata.get("content_type", "application/octet-stream") if metadata else "application/octet-stream"
    filename = metadata.get("filename", file_key) if metadata else file_key
    
    return StreamingResponse(
        io.BytesIO(file_content),
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
