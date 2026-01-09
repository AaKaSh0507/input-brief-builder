from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv
load_dotenv()

from database import Base, engine
from routes import brief_routes, section_routes, document_routes, ai_routes

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="GPJ Input Brief Assistant API",
    version="1.0.0"
)

origins = os.getenv("CORS_ORIGINS", "").split(",")
origins = [o.strip() for o in origins if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Safe DB initialization
@app.on_event("startup")
def on_startup():
    logger.info("Initializing database")
    Base.metadata.create_all(bind=engine)

# Health check
@app.get("/api/health")
def health():
    return {"status": "healthy"}

# Routes
app.include_router(brief_routes.router, prefix="/api")
app.include_router(section_routes.router, prefix="/api")
app.include_router(document_routes.router, prefix="/api")
app.include_router(ai_routes.router, prefix="/api")

# Root
@app.get("/")
def root():
    return {"message": "GPJ Input Brief Assistant API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)

