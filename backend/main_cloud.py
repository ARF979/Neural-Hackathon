"""
AI Social Media Content Generator API - CLOUD VERSION
Uses Hugging Face Inference API instead of local models
Perfect for MacBooks with limited RAM/storage
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import cloud-based workflow
from agents.workflow_cloud import generate_content

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="AI Social Media Generator (Cloud)",
    description="Generate social media content using cloud-based AI models",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== REQUEST/RESPONSE MODELS ========== #

class ContentRequest(BaseModel):
    user_instruction: str = Field(
        ..., 
        json_schema_extra={"example": "Create an Instagram post promoting eco-friendly water bottles"}
    )
    tone: str = Field(
        default="Professional",
        json_schema_extra={"example": "Fun and Playful"}
    )
    style: str = Field(
        default="Short caption with hashtags",
        json_schema_extra={"example": "Short caption with 3-4 hashtags"}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "user_instruction": "Create an Instagram post promoting eco-friendly water bottles",
                "tone": "Fun and Playful",
                "style": "Short caption with 3-4 hashtags"
            }
        }

class ContentResponse(BaseModel):
    success: bool
    content: Optional[str] = None
    image_prompt: Optional[str] = None
    compliance_status: Optional[str] = None
    compliance_feedback: Optional[str] = None
    metadata: Optional[dict] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    model_type: str
    api_configured: bool

class ErrorResponse(BaseModel):
    detail: str

# ========== API ENDPOINTS ========== #

@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "AI Social Media Content Generator API (Cloud Version)",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "model_type": "cloud"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    
    return {
        "status": "healthy",
        "version": "2.0.0",
        "model_type": "cloud",
        "api_configured": bool(hf_token)
    }

@app.get("/api/models/status")
async def models_status():
    """Check cloud API configuration status"""
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    
    if not hf_token:
        return {
            "configured": False,
            "message": "Hugging Face API token not configured",
            "instructions": "Get free token from https://huggingface.co/settings/tokens and set HUGGINGFACE_API_TOKEN in .env file"
        }
    
    return {
        "configured": True,
        "model_type": "cloud",
        "provider": "Hugging Face Inference API",
        "models": {
            "writer": "mistralai/Mistral-7B-Instruct-v0.2",
            "reviewer": "mistralai/Mistral-7B-Instruct-v0.2"
        },
        "status": "ready"
    }

@app.post("/api/generate", response_model=ContentResponse)
async def generate_content_api(request: ContentRequest):
    """
    Generate social media content using cloud-based AI agents
    
    - **user_instruction**: Description of content to create
    - **tone**: Desired tone (Professional, Casual, Fun, etc.)
    - **style**: Content style (Short caption, Story, etc.)
    """
    try:
        logger.info(f"🚀 Generating content: {request.user_instruction[:50]}...")
        
        # Check if API token is configured
        hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
        if not hf_token:
            raise HTTPException(
                status_code=500,
                detail="Hugging Face API token not configured. Get free token from https://huggingface.co/settings/tokens"
            )
        
        # Generate content using cloud models
        result = generate_content(
            user_instruction=request.user_instruction,
            tone=request.tone,
            style=request.style,
            hf_token=hf_token
        )
        
        if result.get("success"):
            logger.info("✅ Content generated successfully")
            return ContentResponse(**result)
        else:
            logger.error(f"❌ Generation failed: {result.get('error')}")
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Content generation failed")
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# ========== ERROR HANDLERS ========== #

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "detail": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return {
        "detail": "Internal server error",
        "error": str(exc)
    }

# ========== STARTUP ========== #

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("☁️ AI SOCIAL MEDIA CONTENT GENERATOR API (CLOUD)")
    print("=" * 60)
    print("📡 Starting server on http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Alternative Docs: http://localhost:8000/redoc")
    print()
    print("💡 Using Hugging Face Inference API (No local models needed!)")
    print("🔑 Make sure HUGGINGFACE_API_TOKEN is set in .env file")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
