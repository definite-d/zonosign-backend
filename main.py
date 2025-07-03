# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
from database import engine
from models import Base
from routers import auth, users, curriculum, dictionary, progress, transcription
from scalar_fastapi import get_scalar_api_reference

# Create database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting ZonoSign API...")
    yield
    # Shutdown
    print("Shutting down ZonoSign API...")


app = FastAPI(
    title="ZonoSign API",
    description="Backend API for ZonoSign sign language learning platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/v1/users", tags=["Users"])
app.include_router(curriculum.router, prefix="/v1/curriculum", tags=["Curriculum"])
app.include_router(dictionary.router, prefix="/v1/dictionary", tags=["Dictionary"])
app.include_router(progress.router, prefix="/v1/progress", tags=["Progress"])
app.include_router(
    transcription.router, prefix="/v1/transcription", tags=["Transcription"]
)


@app.get("/")
async def root():
    return {"message": "ZonoSign API v1.0.0", "status": "active"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "zonosign-api"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    # noinspection PyUnresolvedReferences
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8024)
