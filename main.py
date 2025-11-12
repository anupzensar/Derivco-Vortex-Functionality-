"""
FastAPI Server for Canvas Queue API Integration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from routes import incidents, extraction

# Initialize FastAPI app
app = FastAPI(
    title="Canvas Queue API Integration",
    description="FastAPI server to interact with Canvas Queue API",
    version="1.0.0"
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
app.include_router(incidents.router, prefix="/api", tags=["incidents"])
app.include_router(extraction.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Canvas Queue API Integration Server",
        "status": "running",
        "canvas_api_url": settings.CANVAS_API_BASE_URL
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
