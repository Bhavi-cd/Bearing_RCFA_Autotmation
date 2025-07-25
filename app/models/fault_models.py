from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class BearingType(str, Enum):
    BALL_BEARING = "ball_bearing"
    ROLLER_BEARING = "roller_bearing"
    THRUST_BEARING = "thrust_bearing"
    NEEDLE_BEARING = "needle_bearing"
    SPHERICAL_BEARING = "spherical_bearing"
    TAPERED_ROLLER = "tapered_roller"

class ImageAnalysisRequest(BaseModel):
    """Request model for image analysis"""
    bearing_type: Optional[BearingType] = None
    application: Optional[str] = None
    additional_context: Optional[str] = None
    operating_conditions: Optional[Dict[str, Any]] = None

class BearingAnalysisResult(BaseModel):
    """Results from Gemini-based bearing analysis"""
    observed_damage: str
    failure_mode: str
    root_cause_analysis: List[str]
    confidence_score: float = Field(ge=0.0, le=1.0)
    technical_notes: Optional[str] = None
    recommendations: List[str] = []

class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    analysis: BearingAnalysisResult
    processing_time: float
    model_used: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    model_config = {
        "protected_namespaces": ()
    }

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_available: bool
    api_key_configured: bool
    timestamp: datetime = Field(default_factory=datetime.now)
    
    model_config = {
        "protected_namespaces": ()
    } 