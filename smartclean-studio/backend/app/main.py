from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import cleaning

app = FastAPI(title="SmartClean Studio API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cleaning.router, prefix="/api", tags=["cleaning"])


@app.get("/")
async def root():
    return {
        "name": "SmartClean Studio API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "POST /api/upload",
            "configure": "POST /api/configure",
            "clean": "POST /api/clean",
            "report": "GET /api/report/{session_id}",
            "preview": "GET /api/preview/{session_id}",
            "download": "POST /api/download/{session_id}/{format}"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
