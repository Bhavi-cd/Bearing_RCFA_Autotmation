"""
API Routes for Bearing Fault Analysis using Gemini AI
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
import io

from app.core.gemini_fault_analyzer import GeminiFaultAnalyzer
from app.models.fault_models import (
    AnalysisResponse, 
    HealthResponse, 
    BearingType
)

# Initialize routers
health_router = APIRouter(tags=["Health"])
analysis_router = APIRouter(tags=["Analysis"])

# Initialize the Gemini fault analyzer
fault_analyzer = GeminiFaultAnalyzer()

@health_router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if fault_analyzer.is_ready() else "unhealthy",
        model_available=fault_analyzer.model is not None,
        api_key_configured=fault_analyzer.api_key_configured
    )

@analysis_router.post("/analyze-image", response_model=AnalysisResponse)
async def analyze_bearing_image(
    image: UploadFile = File(..., description="Bearing image to analyze"),
    bearing_type: Optional[BearingType] = Form(None, description="Type of bearing"),
    application: Optional[str] = Form(None, description="Application context"),
    additional_context: Optional[str] = Form(None, description="Additional context")
):
    """
    Analyze bearing image using Gemini AI for fault diagnosis
    
    Upload a bearing image and get detailed analysis including:
    - Observed damage description
    - Failure mode identification
    - Root cause analysis
    - Technical recommendations
    """
    
    # Validate file type
    if not image.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400, 
            detail="File must be an image (JPEG, PNG, etc.)"
        )
    
    # Check if analyzer is ready
    if not fault_analyzer.is_ready():
        raise HTTPException(
            status_code=503,
            detail="Analysis service not available. Please check API key configuration."
        )
    
    try:
        # Read image data
        image_data = await image.read()
        
        if len(image_data) == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty image file"
            )
        
        # Perform analysis
        result = await fault_analyzer.analyze_bearing_image(
            image_data=image_data,
            bearing_type=bearing_type.value if bearing_type else None,
            application=application,
            additional_context=additional_context
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@analysis_router.get("/status")
async def get_analyzer_status():
    """Get current analyzer status and configuration"""
    return {
        "analyzer_ready": fault_analyzer.is_ready(),
        "api_key_configured": fault_analyzer.api_key_configured,
        "model_available": fault_analyzer.model is not None,
        "model_name": fault_analyzer.model.name if fault_analyzer.model else None
    } 