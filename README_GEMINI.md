# Bearing Fault Analysis with Google Gemini AI

A simplified, powerful bearing fault analysis system using Google's Gemini 1.5 Flash vision model for specialist-level diagnosis.

## 🚀 Features

- **Direct Image Analysis**: Upload bearing images and get instant expert analysis
- **Gemini AI Powered**: Uses Google's latest Gemini 1.5 Flash model for accurate diagnosis
- **Structured Output**: Clear, professional analysis with observed damage, failure mode, and root cause
- **Fast API**: Simple REST API for easy integration
- **No Complex Setup**: Minimal dependencies and straightforward configuration

## 📋 Requirements

- Python 3.8+
- Google Generative AI API key
- Bearing images (JPEG, PNG, etc.)

## 🛠️ Installation

1. **Clone and install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up your Google API key:**
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
GOOGLE_API_KEY=your-api-key-here
```

## 🚀 Quick Start

### 1. Start the API Server
```bash
python -m app.main
```

The server will start at `http://localhost:8000`

### 2. Test with Direct Script
```bash
python test_gemini_analysis.py
```

### 3. Test with API Client
```bash
python gemini_client.py
```

## 📡 API Usage

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Analyze Bearing Image
```bash
curl -X POST "http://localhost:8000/api/v1/analyze-image" \
  -F "image=@your_bearing_image.jpg" \
  -F "bearing_type=ball_bearing" \
  -F "application=Industrial machinery" \
  -F "additional_context=High-speed operation"
```

## 📊 Analysis Output

The system provides structured analysis including:

- **📷 Observed Damage**: Detailed description of visible surface changes
- **⚙️ Failure Mode**: Identified failure mechanism with justification
- **🧠 Root Cause Analysis**: Probable root causes in bullet points
- **💡 Recommendations**: Technical recommendations for prevention

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Generative AI API key
- `HOST`: API server host (default: 0.0.0.0)
- `PORT`: API server port (default: 8000)
- `DEBUG`: Debug mode (default: True)

### Model Configuration
- `GEMINI_MODEL`: Gemini model to use (default: models/gemini-1.5-flash)

## 📁 Project Structure

```
Prototype/
├── app/
│   ├── core/
│   │   ├── config.py              # Configuration settings
│   │   └── gemini_fault_analyzer.py # Main Gemini analyzer
│   ├── models/
│   │   └── fault_models.py        # Pydantic models
│   ├── api/
│   │   └── routes.py              # API endpoints
│   └── main.py                    # FastAPI application
├── test_gemini_analysis.py        # Direct test script
├── gemini_client.py               # API client example
├── requirements.txt               # Dependencies
└── README_GEMINI.md              # This file
```

## 🎯 Example Analysis

**Input**: Bearing image showing surface damage

**Output**:
```json
{
  "analysis": {
    "observed_damage": "Visible spalling on the inner race surface with pitting in multiple locations",
    "failure_mode": "Fatigue failure due to cyclic loading exceeding material endurance limit",
    "root_cause_analysis": [
      "Insufficient lubrication leading to metal-to-metal contact",
      "Overloading conditions causing stress concentration",
      "Contamination ingress accelerating wear processes"
    ],
    "confidence_score": 0.9,
    "recommendations": [
      "Implement proper lubrication schedule",
      "Monitor load conditions and reduce if possible",
      "Improve sealing to prevent contamination"
    ]
  },
  "processing_time": 2.34,
  "model_used": "models/gemini-1.5-flash"
}
```

## 🔍 How It Works

1. **Image Upload**: User uploads bearing image via API
2. **Gemini Analysis**: Image is sent to Gemini 1.5 Flash with expert prompt
3. **Response Parsing**: Structured response is parsed into analysis components
4. **Result Delivery**: Clean, professional analysis is returned to user

## 🆚 Comparison with Previous Approach

| Feature | Previous Approach | Gemini Approach |
|---------|------------------|-----------------|
| **Complexity** | High (multiple analyzers, rules, knowledge base) | Low (single AI model) |
| **Accuracy** | Rule-based with limited AI | Advanced vision AI |
| **Setup** | Complex initialization | Simple API key |
| **Maintenance** | Multiple components | Single model |
| **Performance** | Slower (multiple steps) | Faster (direct analysis) |
| **Flexibility** | Limited to predefined patterns | Adapts to any visible damage |

## 🚨 Troubleshooting

### API Key Issues
- Ensure `GOOGLE_API_KEY` is set correctly
- Check API key permissions and quotas
- Verify the key is valid in Google AI Studio

### Image Issues
- Supported formats: JPEG, PNG, WebP
- Maximum size: 20MB
- Ensure image shows bearing surface clearly

### Server Issues
- Check if port 8000 is available
- Ensure all dependencies are installed
- Check logs for detailed error messages

## 📈 Performance

- **Typical response time**: 2-5 seconds
- **Image size limit**: 20MB
- **Concurrent requests**: Limited by Gemini API quotas
- **Accuracy**: High (based on Gemini 1.5 Flash capabilities)

## 🔮 Future Enhancements

- Batch processing for multiple images
- Historical analysis tracking
- Integration with maintenance systems
- Custom model fine-tuning
- Multi-language support

## 📄 License

This project is for educational and research purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note**: This simplified approach focuses on leveraging Gemini's advanced vision capabilities for direct, accurate bearing analysis without the complexity of multiple specialized components. 