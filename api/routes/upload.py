from fastapi import APIRouter, UploadFile, File

from services.uploader import save_upload


router = APIRouter()


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    destination = save_upload(file, file.filename)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "path": str(destination),
    }