from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api.routes import health_router, analysis_router
from app.core.config import settings

app = FastAPI(
    title="Bearing Fault Analysis API",
    description="Specialist-level bearing fault diagnosis using Google's Gemini AI",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Bearing Fault Analysis API using Gemini AI",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
        "analyze": "/api/v1/analyze-image"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    ) 