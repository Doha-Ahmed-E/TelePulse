from fastapi import FastAPI

from routes.upload import router as upload_router


app = FastAPI(
    title="TelePulse API",
    description="API for uploading TelePulse data files.",
)

app.include_router(upload_router)