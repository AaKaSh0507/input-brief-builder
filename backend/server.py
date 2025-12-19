from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from pathlib import Path

# Import database
from database import Base, engine

# Import routes
from routes import brief_routes, section_routes, document_routes, ai_routes

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created")

# Create FastAPI app
app = FastAPI(
    title="GPJ Input Brief Assistant API",
    description="AI-powered event input brief generation system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "GPJ Input Brief Assistant"}

# Include routers with /api prefix
app.include_router(brief_routes.router, prefix="/api")
app.include_router(section_routes.router, prefix="/api")
app.include_router(document_routes.router, prefix="/api")
app.include_router(ai_routes.router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    return {"message": "GPJ Input Brief Assistant API", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
