# main.py - FastAPI Backend for AI Social Media Generator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
import logging
from datetime import datetime

# Import our AI workflow
from agents.workflow import generate_content, load_models

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Social Media Content Generator",
    description="Professional API for generating AI-powered social media content",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== REQUEST/RESPONSE MODELS ========== #

class ContentRequest(BaseModel):
    """Request model for content generation"""
    user_instruction: str = Field(
        ..., 
        description="Product or campaign description",
        example="Create an Instagram post promoting EcoWave reusable water bottles."
    )
    tone: str = Field(
        ..., 
        description="Desired tone of the content",
        example="fun, friendly, eco-conscious"
    )
    style: str = Field(
        ..., 
        description="Content style and format",
        example="short caption with 3-4 hashtags"
    )

    class Config:
        schema_extra = {
            "example": {
                "user_instruction": "Create an Instagram post promoting EcoWave reusable water bottles.",
                "tone": "fun, friendly, eco-conscious",
                "style": "short caption with 3-4 hashtags"
            }
        }


class ContentResponse(BaseModel):
    """Response model for generated content"""
    success: bool
    reviewed_text: str
    image_prompt: str
    compliance_status: str
    compliance_feedback: str
    iteration: int
    elapsed_time: float
    generated_at: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    details: Optional[str] = None


# ========== STARTUP EVENT ========== #

@app.on_event("startup")
async def startup_event():
    """Load AI models on startup"""
    logger.info("🚀 Starting AI Social Media Generator API...")
    logger.info("⚡ Loading AI models (this may take a few minutes)...")
    try:
        load_models()
        logger.info("✅ All models loaded successfully!")
    except Exception as e:
        logger.error(f"❌ Failed to load models: {e}")
        # Note: In production, you might want to fail the startup here


# ========== API ENDPOINTS ========== #

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - API info"""
    return {
        "status": "online",
        "message": "AI Social Media Content Generator API is running! Visit /docs for API documentation.",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "API is operational",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/generate", response_model=ContentResponse)
async def generate_social_content(request: ContentRequest):
    """
    Generate AI-powered social media content
    
    This endpoint takes a product description, desired tone, and style,
    then uses AI agents to generate optimized social media content with
    compliance checking and iterative refinement.
    
    - **user_instruction**: Description of the product or campaign
    - **tone**: Desired emotional tone (e.g., "fun, friendly, professional")
    - **style**: Content format (e.g., "short caption with hashtags")
    
    Returns generated caption, image prompt, and compliance status.
    """
    try:
        logger.info(f"📝 Generating content for: {request.user_instruction[:50]}...")
        
        # Call the AI workflow
        result = generate_content(
            user_instruction=request.user_instruction,
            tone=request.tone,
            style=request.style
        )
        
        logger.info(f"✅ Content generated successfully in {result['elapsed_time']}s")
        
        return {
            "success": True,
            "reviewed_text": result["reviewed_text"],
            "image_prompt": result["image_prompt"],
            "compliance_status": result["compliance_status"],
            "compliance_feedback": result["compliance_feedback"],
            "iteration": result["iteration"],
            "elapsed_time": result["elapsed_time"],
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating content: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "Content generation failed",
                "details": str(e)
            }
        )


@app.get("/api/models/status")
async def models_status():
    """Check if AI models are loaded"""
    from agents.workflow import _MODELS_LOADED
    return {
        "models_loaded": _MODELS_LOADED,
        "status": "ready" if _MODELS_LOADED else "loading",
        "timestamp": datetime.now().isoformat()
    }


# ========== ERROR HANDLERS ========== #

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return {
        "success": False,
        "error": exc.detail,
        "status_code": exc.status_code
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "success": False,
        "error": "Internal server error",
        "details": str(exc)
    }


# ========== MAIN ========== #

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 AI SOCIAL MEDIA CONTENT GENERATOR API")
    print("=" * 60)
    print("📡 Starting server on http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Alternative Docs: http://localhost:8000/redoc")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
