# 🔧 Industrial Bearing Fault Analysis Chatbot 🖼️

**Advanced Image-Based and Text-Based Bearing Fault Diagnosis System**

A specialized AI-powered chatbot for industrial bearing fault analysis that provides expert-level diagnosis using both textual descriptions and visual image analysis. This system combines traditional symptom-based analysis with cutting-edge computer vision for comprehensive bearing fault detection.

## 🌟 **Key Features**

### 📝 **Text-Based Analysis**
- Expert-level bearing fault diagnosis from symptom descriptions
- 9 major fault categories with industry statistics
- ML-powered pattern matching using TF-IDF vectorization
- Confidence scoring and severity assessment
- Actionable maintenance recommendations

### 🖼️ **Image-Based Analysis** (NEW!)
- **Visual Defect Detection**: Spalling, pitting, cracks, corrosion
- **Wear Pattern Analysis**: Misalignment indicators, edge loading
- **Contamination Detection**: Foreign particles, debris identification
- **Thermal Damage Assessment**: Heat discoloration, material softening
- **Surface Condition Evaluation**: Roughness, uniformity analysis
- **Crack Detection**: Linear crack features, stress fractures

### 🏭 **Industry Expertise**
- 150+ fault patterns from real-world industrial experience
- Support for 6 bearing types (ball, roller, thrust, needle, spherical, tapered)
- Industry-specific knowledge (steel mills, paper mills, mining, power generation)
- Root cause analysis with immediate actions and long-term solutions

## 🚀 **Quick Start**

### **Prerequisites**
```bash
Python 3.8+
pip install -r requirements.txt
```

### **Installation**
```bash
git clone <repository>
cd Prototype
pip install -r requirements.txt
```

### **Start the Server**
```bash
python3 -m app.main
```

### **Text Analysis - Terminal Chat**
```bash
python3 chat_client.py
```

### **Image Analysis - Upload Images**
```bash
# Interactive mode with image support
python3 chat_client.py

# Direct image analysis
python3 chat_client.py --image bearing_damage.jpg

# Direct text analysis  
python3 chat_client.py --text "High vibration and temperature"
```

## 📊 **Supported Analysis Types**

### **Fault Categories (9 Types)**
1. **Lubrication** (30-40% of failures) - Inadequate lubrication, contamination
2. **Misalignment** (10-20% of failures) - Angular/parallel misalignment
3. **Contamination** (20-30% of failures) - Solid particles, debris
4. **Overloading** (10-15% of failures) - Static/dynamic overload
5. **Installation** (8-12% of failures) - Improper mounting, fit issues
6. **Thermal** (5-10% of failures) - Temperature-related degradation
7. **Vibration** (3-8% of failures) - False brinelling, resonance
8. **Electrical** (2-5% of failures) - Current damage, VFD issues
9. **Corrosion** (2-15% of failures) - Moisture, chemical attack

### **Bearing Types (6 Types)**
- Ball Bearings
- Roller Bearings  
- Thrust Bearings
- Needle Bearings
- Spherical Bearings
- Tapered Roller Bearings

### **Image Analysis Capabilities**
- **Visual Defect Patterns**: 8 specialized patterns for image matching
- **Supported Formats**: JPEG, PNG, TIFF, BMP (max 10MB)
- **Color Analysis**: HSV-based defect detection
- **Morphological Operations**: Crack and pitting detection
- **Edge Detection**: Surface irregularity analysis
- **Regional Analysis**: Damage location identification

## 🖼️ **Image Analysis Usage**

### **Interactive Chat Client**
```bash
python3 chat_client.py

# Commands in chat:
🖼️ Image> upload bearing_damage.jpg
🖼️ Image> upload motor_bearing.png bearing_type:ball_bearing application:pump
📝 Text> High vibration and grinding noise
```

### **API Endpoints**

#### **Image Upload**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/image" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@bearing_photo.jpg" \
  -F "bearing_type=ball_bearing" \
  -F "application=motor" \
  -F "additional_context=High temperature operation"
```

#### **Text Analysis**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Bearing making grinding noise with high temperature", "bearing_type": "roller_bearing"}'
```

## 📋 **API Reference**

### **Chat Endpoints**
- `POST /api/v1/chat` - Text-based bearing analysis
- `POST /api/v1/chat/image` - **Image-based bearing analysis** 🆕
- `POST /api/v1/chat/quick` - Quick text diagnosis
- `GET /api/v1/chat/capabilities` - System capabilities

### **Analysis Endpoints**
- `POST /api/v1/analysis/detailed` - Detailed text analysis
- `POST /api/v1/analysis/image-detailed` - **Detailed image analysis** 🆕
- `GET /api/v1/analysis/fault-patterns` - Available fault patterns
- `POST /api/v1/analysis/symptom-match` - Symptom matching
- `POST /api/v1/analysis/batch` - Batch analysis (text only)

### **Health Endpoints**
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed system status
- `GET /api/v1/analysis/statistics` - System statistics

## 🧪 **Example Analyses**

### **Text-Based Analysis Example**
```json
{
  "message": "Motor bearing running hot with grinding noise and metal particles in oil",
  "bearing_type": "ball_bearing",
  "application": "electric_motor"
}
```

**Response:**
```json
{
  "response": "## Bearing Fault Analysis\n**Primary Diagnosis:** Lubrication Fault\n**Confidence Level:** 87.3%\n**Severity:** High\n\n**Analysis:** Lubrication-related bearing failure characterized by inadequate or degraded lubricant performance. Manifesting symptoms include: lubrication, temperature, noise, contamination\n\n**Root Cause:** Insufficient lubrication quantity\n\n**Immediate Actions Required:**\n• Check lubricant level and quality\n• Verify lubrication system operation\n• Increase monitoring frequency",
  "confidence_score": 0.873,
  "analysis": {
    "primary_diagnosis": {
      "fault_category": "lubrication",
      "confidence": 0.873,
      "severity": "high"
    }
  }
}
```

### **Image-Based Analysis Example**
```bash
# Upload bearing image with context
curl -X POST "http://localhost:8000/api/v1/chat/image" \
  -F "image=@damaged_bearing.jpg" \
  -F "bearing_type=roller_bearing" \
  -F "additional_context=Found in steel mill conveyor system"
```

**Response:**
```json
{
  "response": "## Image-Based Bearing Fault Analysis\n\n**Image Analysis Confidence:** 78.5%\n**Surface Condition:** Poor\n\n**Visual Defects Detected:**\n• Corrosion Rust\n• Surface Irregularities\n• Pitting\n\n**Primary Diagnosis:** Corrosion Fault\n**Diagnostic Confidence:** 82.1%\n**Severity Assessment:** High\n\n**Visual Evidence:**\n• Corrosion Rust\n• Surface Irregularities\n• Pitting\n\n**Immediate Actions Required:**\n• Immediately shut down equipment to prevent catastrophic failure\n• Implement safety lockout procedures",
  "confidence_score": 0.821,
  "image_processed": true,
  "image_analysis_time": 2.34
}
```

## 🔧 **Advanced Configuration**

### **Environment Variables**
```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=1

# Analysis Configuration  
ANALYSIS_CONFIDENCE_THRESHOLD=0.3
ANALYSIS_MAX_PATTERNS=10

# Image Analysis Configuration
IMAGE_MAX_SIZE_MB=10
IMAGE_ANALYSIS_TIMEOUT=30
```

### **Custom Knowledge Base**
The system uses a comprehensive knowledge base with 150+ fault patterns. You can extend it by modifying `app/core/knowledge_base.py`.

### **Image Analysis Customization**
Adjust image analysis parameters in `app/core/image_analyzer.py`:
- Color ranges for defect detection
- Morphological kernels for crack detection
- Threshold values for damage assessment

## 📊 **System Statistics**

```bash
curl http://localhost:8000/api/v1/analysis/statistics
```

**Example Response:**
```json
{
  "knowledge_base": {
    "total_patterns": 150,
    "categories_covered": 9,
    "visual_defect_patterns": 8,
    "bearing_type_coverage": {
      "ball_bearing": 145,
      "roller_bearing": 142,
      "thrust_bearing": 89
    }
  },
  "system_capabilities": {
    "image_analysis_enabled": true,
    "supported_visual_defects": 8,
    "average_symptoms_per_pattern": 4.2
  }
}
```

## 🏗️ **Project Structure**

```
Prototype/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── fault_analyzer.py   # Main analysis engine with image support
│   │   ├── image_analyzer.py   # 🆕 Image analysis engine
│   │   ├── knowledge_base.py   # Enhanced with visual indicators
│   │   ├── diagnostic_rules.py # Expert rules engine
│   │   └── config.py          # Configuration management
│   ├── models/
│   │   └── fault_models.py    # Enhanced data models with image support
│   └── api/
│       └── routes.py          # Enhanced API routes with image endpoints
├── chat_client.py             # 🆕 Image-capable chat client
├── requirements.txt           # Updated with CV libraries
└── README.md                  # This file
```

## 🧬 **Technical Implementation**

### **Image Analysis Pipeline**
1. **Image Preprocessing**: Resize, enhance contrast/sharpness
2. **Computer Vision Analysis**:
   - HSV color space analysis for corrosion/thermal damage
   - Edge detection for surface irregularities
   - Morphological operations for pitting/cracks
   - Regional analysis for damage location
3. **Pattern Matching**: Match visual findings to fault patterns
4. **Confidence Scoring**: Multi-factor confidence assessment
5. **Diagnosis Generation**: Integrate with existing fault analysis

### **Machine Learning Components**
- **TF-IDF Vectorization**: Text-based symptom analysis
- **Cosine Similarity**: Pattern matching algorithm
- **Computer Vision**: OpenCV-based image analysis
- **Confidence Algorithms**: Multi-modal confidence scoring

### **Performance Optimizations**
- Asynchronous image processing
- Concurrent analysis pipelines
- Image size optimization
- Memory-efficient CV operations

## 🎯 **Use Cases**

### **Maintenance Teams**
- **Text Mode**: Quick diagnosis from verbal descriptions
- **Image Mode**: Visual inspection documentation and analysis
- **Batch Processing**: Multiple bearing assessments

### **Condition Monitoring**
- **Vibration Analysis Integration**: Combine with sensor data
- **Thermal Imaging**: Supplement with temperature analysis  
- **Oil Analysis**: Correlate with lubricant testing

### **Training & Education**
- **Visual Learning**: Image-based fault identification
- **Expert Knowledge Transfer**: Systematic diagnosis methodology
- **Case Studies**: Real-world failure analysis examples

## 🔗 **Integration Examples**

### **Python Integration**
```python
import requests

# Text analysis
response = requests.post("http://localhost:8000/api/v1/chat", 
    json={"message": "High vibration detected"})

# Image analysis
with open("bearing.jpg", "rb") as f:
    response = requests.post("http://localhost:8000/api/v1/chat/image",
        files={"image": f},
        data={"bearing_type": "ball_bearing"})
```

### **JavaScript Integration**
```javascript
// Image upload with fetch
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('bearing_type', 'roller_bearing');

fetch('/api/v1/chat/image', {
    method: 'POST',
    body: formData
}).then(response => response.json());
```

## 🛡️ **Security & Production Deployment**

### **Security Considerations**
- File upload validation and size limits
- Image format verification
- Input sanitization
- Rate limiting recommendations

### **Production Setup**
```bash
# Use production ASGI server
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📝 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 **Contributing**

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 **Support**

For support and questions:
- Create an issue in the repository
- Check the API documentation at `http://localhost:8000/docs`
- Review the comprehensive examples above

---

**🔧 Built for Industrial Excellence 🖼️**

*Combining traditional bearing expertise with modern AI and computer vision for comprehensive fault analysis.* 