"""
Gemini-based Bearing Fault Analyzer
Uses Google's Gemini 1.5 Flash for specialist-level bearing failure analysis
"""

import asyncio
import time
from typing import Optional, Dict, Any
import google.generativeai as genai
from PIL import Image
import io
import base64
import re

from app.core.config import settings
from app.models.fault_models import BearingAnalysisResult, AnalysisResponse

class GeminiFaultAnalyzer:
    """Bearing fault analyzer using Google's Gemini AI"""
    
    def __init__(self):
        self.model = None
        self.api_key_configured = False
        self._initialize_gemini()
    
    def _initialize_gemini(self):
        """Initialize Gemini with API key"""
        try:
            if settings.GOOGLE_API_KEY:
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.model = genai.GenerativeModel(model_name=settings.GEMINI_MODEL)
                self.api_key_configured = True
                print("✅ Gemini AI initialized successfully")
            else:
                print("⚠️  Google API key not configured. Set GOOGLE_API_KEY in environment.")
        except Exception as e:
            print(f"❌ Failed to initialize Gemini: {e}")
    
    def _create_expert_prompt(self, bearing_type: Optional[str] = None, 
                             mounted_on_motor: Optional[bool] = None,
                             application: Optional[str] = None,
                             additional_context: Optional[str] = None) -> str:
        """Create the expert prompt for bearing analysis"""

        context_info = ""
        if bearing_type:
            context_info += f"\nBearing Type: {bearing_type.upper()} (analyze all findings in the context of this bearing type)"
        if mounted_on_motor is not None:
            motor_status = "MOUNTED ON A MOTOR" if mounted_on_motor else "NOT MOUNTED ON A MOTOR"
            context_info += f"\nMotor Mounting: {motor_status} (consider this in your analysis)"
        if application:
            context_info += f"\nApplication: {application}"
        if additional_context:
            context_info += f"\nAdditional Context: {additional_context}"
        
        # Electrical erosion logic
        electrical_note = ""
        if mounted_on_motor is not None:
            if mounted_on_motor:
                electrical_note = """
- Evaluate electrical erosion (e.g., fluting, arc pitting, EDM marks).
- Look for Evenly spaced axial fluting and Arc-shaped pits or EDM-like craters across raceway
- Only consider if patterns are symmetric and consistent with electrical discharge."""
            else:
                electrical_note = """
- Do NOT consider electrical erosion or current-related damage.
- This bearing is not mounted on a motor."""
        
        prompt = f"""
You are a Bearing Failure Analysis Expert.

**IMPORTANT:**  
- First, check if the uploaded image actually contains a bearing or a bearing component.  
- If you are not sure there is a bearing in the image, or the image is unclear, respond with:  
  "No bearing detected or image unclear. Please upload a clear bearing image."  
  and do not attempt further analysis.

If a bearing is present, analyze the attached image of a bearing ring (inner or outer) using only visible surface evidence.  
**Always consider the bearing type and motor mounting status in your analysis and conclusions.**

{context_info}

🔍 1. Observed Damage:
- Describe surface damage precisely: type, shape, distribution, size, and location (e.g., raceway, shoulder, chamfer).
- Focus on visible features only: pitting, smearing, fluting, false brinelling, scoring, etc.
- Use bullets. No speculation.

⚙️ 2. Failure Mode:
- Identify most likely failure mechanism based on damage patterns:
  * fatigue, abrasion, lubrication failure, contamination, electrical erosion, improper mounting, misalignment, etc.
- Do NOT over-prioritize electrical erosion unless clearly supported (e.g., axial fluting, EDM pits). Only consider if patterns are symmetrical, repeated, and consistent.
{electrical_note}
- Give equal or more focus to mounting damage signs: false brinelling, ring creep, rotated wear bands, shoulder polishing, fretting.

🧠 3. Root Cause Analysis:
- State the **most likely** root cause (or 2 max if equal).
- Justify based ONLY on image evidence.
- Stay objective. Do not assume lubrication/electrical/misalignment unless visible.
- Examples of causes: contamination ingress, misfit mounting, uneven loading, loose fits, thermal expansion, vibration, motor grounding failure, etc.
{electrical_note}

🔢 4. Confidence Score:
- Provide as: Confidence: XX%
- Base it on clarity of visible damage.
- Avoid high confidence unless patterns are distinctive.

💡 5. Brief Recommendations:
- Give exactly 3 short, actionable recommendations. Each should be:
  * Under 8 words
  * Direct and specific (no explanations)

📏 Constraints:
- Stick to 1-2 causes only.
- All reasoning must trace back to image.
- Be concise. Avoid repetition or generic advice.
- Stick to relevant fault mode and root cause only.
- Avoid long paragraphs. Bullet points or tight sentences.
- Use consistent terminology for similar patterns across cases.
- Avoid electrical erosion bias. Focus only if visually supported.
"""
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> BearingAnalysisResult:
        """Parse Gemini response into structured format"""
        try:
            # Print raw response for debugging
            print(f"\n🔍 RAW GEMINI RESPONSE:")
            print(response_text)
            print("="*60)
            
            # Initialize variables
            observed_damage = ""
            failure_mode = ""
            root_cause_analysis = []
            recommendations = []
            confidence_score = 0.8  # Default confidence
            
            # Split response into lines and process
            lines = response_text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect section headers (more flexible matching)
                if "🔍" in line and ("Observed Damage" in line or "1." in line):
                    current_section = "damage"
                    continue
                elif "⚙️" in line and ("Failure Mode" in line or "2." in line):
                    current_section = "mode"
                    continue
                elif "🧠" in line and ("Root Cause Analysis" in line or "3." in line):
                    current_section = "cause"
                    continue
                elif "🔢" in line and ("Confidence Score" in line or "4." in line):
                    current_section = "confidence"
                    continue
                elif "💡" in line and ("Specific Recommendations" in line or "5." in line):
                    current_section = "recommendations"
                    continue
                elif "📏" in line and "Constraints" in line:
                    current_section = None
                    continue
                
                # Process content based on current section
                if current_section == "damage":
                    # Clean up asterisks and formatting
                    cleaned_line = self._clean_text_line(line)
                    if cleaned_line:
                        if observed_damage:
                            observed_damage += " " + cleaned_line
                        else:
                            observed_damage = cleaned_line
                elif current_section == "mode":
                    # Clean up asterisks and formatting
                    cleaned_line = self._clean_text_line(line)
                    if cleaned_line:
                        if failure_mode:
                            failure_mode += " " + cleaned_line
                        else:
                            failure_mode = cleaned_line
                elif current_section == "cause":
                    # Handle numbered lists and bullet points - focus on 1-2 most likely causes
                    if line.startswith("*") or line.startswith("•") or line.startswith("-"):
                        # Remove bullet point and clean
                        cleaned_line = self._clean_text_line(line.lstrip("*•- "))
                        if cleaned_line and len(root_cause_analysis) < 2:  # Limit to 2 causes
                            root_cause_analysis.append(cleaned_line)
                    elif line and not line.startswith("📏"):
                        # Handle numbered items (e.g., "1. Overload:**")
                        if re.match(r'^\d+\.', line):
                            # Remove number and clean
                            cleaned_line = self._clean_text_line(re.sub(r'^\d+\.\s*', '', line))
                            if cleaned_line and len(root_cause_analysis) < 2:  # Limit to 2 causes
                                root_cause_analysis.append(cleaned_line)
                        else:
                            # Regular text line
                            cleaned_line = self._clean_text_line(line)
                            if cleaned_line and len(root_cause_analysis) < 2:  # Limit to 2 causes
                                root_cause_analysis.append(cleaned_line)
                elif current_section == "confidence":
                    # Extract confidence percentage from the line
                    if "confidence" in line.lower() or "%" in line:
                        percentage_match = re.search(r'(\d+)%', line)
                        if percentage_match:
                            confidence_score = float(percentage_match.group(1)) / 100.0
                elif current_section == "recommendations":
                    # Parse brief recommendations
                    if line.startswith("*") or line.startswith("•") or line.startswith("-"):
                        # Remove bullet point and clean
                        cleaned_line = self._clean_text_line(line.lstrip("*•- "))
                        if cleaned_line and len(cleaned_line) > 2 and len(cleaned_line) < 50:  # Length validation
                            recommendations.append(cleaned_line)
                    elif line and not line.startswith("📏") and not line.startswith("Constraints"):
                        # Handle numbered items
                        if re.match(r'^\d+\.', line):
                            # Remove number and clean
                            cleaned_line = self._clean_text_line(re.sub(r'^\d+\.\s*', '', line))
                            if cleaned_line and len(cleaned_line) > 2 and len(cleaned_line) < 50:
                                recommendations.append(cleaned_line)
                        elif len(line) > 3 and len(line) < 50 and not any(keyword in line.lower() for keyword in ["constraints", "recommendations", "brief", "specific"]):
                            # Regular text line that's not a header
                            cleaned_line = self._clean_text_line(line)
                            if cleaned_line and len(cleaned_line) > 2:
                                recommendations.append(cleaned_line)
            
            # Clean up and validate recommendations
            recommendations = [item.strip() for item in recommendations if item.strip()]
            recommendations = [item for item in recommendations if len(item) > 2 and len(item) < 50]  # Length validation
            recommendations = [item for item in recommendations if not item.startswith("📏")]
            recommendations = [item for item in recommendations if not any(keyword in item.lower() for keyword in ["constraints", "recommendations", "brief", "specific"])]

            # Limit to 4 recommendations maximum and ensure brevity
            if len(recommendations) > 4:
                recommendations = recommendations[:4]

            # Further shorten recommendations if they're too long
            final_recommendations = []
            for rec in recommendations:
                if len(rec) > 40:  # If longer than 40 chars, take first part
                    rec = rec[:40].rsplit(' ', 1)[0] + "..."
                final_recommendations.append(rec)
            
            # Debug output
            print(f"\n PARSED RESULTS:")
            print(f"Observed Damage: '{observed_damage}'")
            print(f"Failure Mode: '{failure_mode}'")
            print(f"Root Causes: {root_cause_analysis}")
            print(f"Recommendations: {final_recommendations}")
            print(f"Confidence Score: {confidence_score:.1%}")
            print("="*60)
            
            # Validate confidence score
            if confidence_score < 0.0 or confidence_score > 1.0:
                confidence_score = 0.8  # Default if invalid
            
            # Use dynamic recommendations if available, otherwise fallback to defaults
            if final_recommendations:
                final_recommendations = final_recommendations
            else:
                final_recommendations = [
                    "Conduct additional visual inspection",
                    "Perform vibration analysis if possible",
                    "Check operating conditions and maintenance history"
                ]
            
            return BearingAnalysisResult(
                observed_damage=observed_damage or "No visible damage detected",
                failure_mode=failure_mode or "Unable to determine failure mode",
                root_cause_analysis=root_cause_analysis or ["Insufficient visual evidence"],
                confidence_score=confidence_score,
                technical_notes="Analysis performed using Gemini vision model",
                recommendations=final_recommendations
            )
            
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            import traceback
            traceback.print_exc()
            return BearingAnalysisResult(
                observed_damage="Error parsing analysis results",
                failure_mode="Analysis failed",
                root_cause_analysis=["Technical error in analysis"],
                confidence_score=0.0,
                technical_notes=f"Parsing error: {str(e)}",
                recommendations=[
                    "Check system configuration",
                    "Verify API key and model access",
                    "Review image quality and format"
                ]
            )
    
    def _clean_text_line(self, line: str) -> str:
        """Clean up text line by removing asterisks and formatting"""
        # Remove leading/trailing whitespace
        line = line.strip()
        
        # Remove asterisks at the beginning and end
        line = re.sub(r'^\*+\s*', '', line)  # Remove leading asterisks
        line = re.sub(r'\s*\*+$', '', line)  # Remove trailing asterisks
        
        # Remove double asterisks (markdown bold formatting)
        line = re.sub(r'\*\*', '', line)
        
        # Remove single asterisks that are not part of words
        line = re.sub(r'\s\*\s', ' ', line)  # Remove isolated asterisks
        
        # Clean up extra whitespace
        line = re.sub(r'\s+', ' ', line)
        
        return line.strip()
    
    async def analyze_bearing_image(self, 
                                  image_data: bytes,
                                  bearing_type: Optional[str] = None,
                                  mounted_on_motor: Optional[bool] = None,
                                  application: Optional[str] = None,
                                  additional_context: Optional[str] = None) -> AnalysisResponse:
        """
        Analyze bearing image using Gemini AI
        
        Args:
            image_data: Raw image bytes
            bearing_type: Type of bearing (optional)
            mounted_on_motor: Whether bearing is mounted on motor (optional)
            application: Application context (optional)
            additional_context: Additional context (optional)
            
        Returns:
            AnalysisResponse with detailed results
        """
        start_time = time.time()
        
        if not self.api_key_configured:
            raise ValueError("Google API key not configured")
        
        if not self.model:
            raise ValueError("Gemini model not initialized")
        
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Create expert prompt
            prompt = self._create_expert_prompt(bearing_type, mounted_on_motor, application, additional_context)
            
            # Generate analysis using Gemini
            response = self.model.generate_content([prompt, image])
            
            # Parse the response
            analysis_result = self._parse_gemini_response(response.text)
            
            processing_time = time.time() - start_time
            
            return AnalysisResponse(
                analysis=analysis_result,
                processing_time=processing_time,
                model_used=settings.GEMINI_MODEL
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"Error in bearing analysis: {e}")
            
            # Return error response
            error_result = BearingAnalysisResult(
                observed_damage="Analysis failed due to technical error",
                failure_mode="Unable to determine",
                root_cause_analysis=["Technical error occurred during analysis"],
                confidence_score=0.0,
                technical_notes=f"Error: {str(e)}",
                recommendations=[
                    "Check system connectivity",
                    "Verify image format and size",
                    "Ensure API key is valid and has sufficient quota"
                ]
            )
            
            return AnalysisResponse(
                analysis=error_result,
                processing_time=processing_time,
                model_used=settings.GEMINI_MODEL
            )
    
    def is_ready(self) -> bool:
        """Check if the analyzer is ready for use"""
        return self.api_key_configured and self.model is not None 