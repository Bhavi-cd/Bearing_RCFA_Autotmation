#!/usr/bin/env python3
"""
Simple client for Gemini-based Bearing Fault Analysis API
Demonstrates how to use the new simplified API
"""

import asyncio
import aiohttp
import json
import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

async def test_api_analysis():
    """Test the API with a bearing image"""
    
    # API endpoint
    api_url = "http://localhost:8001/api/v1/analyze-image"
    
    # Test image path
    image_path = "/home/cimcom/Desktop/RCFA/testing_samples/image2.jpeg"
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        print("   Please update the image_path variable with a valid bearing image")
        return
    
    print("🔍 TESTING GEMINI-BASED API")
    print("="*60)
    print(f"📸 Analyzing: {image_path}")
    
    try:
        # Prepare form data
        data = aiohttp.FormData()
        data.add_field('image', 
                      open(image_path, 'rb'),
                      filename=os.path.basename(image_path),
                      content_type='image/png')
        data.add_field('bearing_type', 'roller_bearing')
        data.add_field('mounted_on_motor', 'false')  # NEW FIELD
        data.add_field('application', 'Industrial machinery')
        data.add_field('additional_context', 'High-speed operation, 24/7 usage')
        
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    print(f"\n✅ API Analysis Successful!")
                    print(f"   Processing time: {result['processing_time']:.2f} seconds")
                    print(f"   Model used: {result['model_used']}")
                    print(f"   Confidence: {result['analysis']['confidence_score']:.1%}")
                    
                    print(f"\n📷 OBSERVED DAMAGE:")
                    print(f"   {result['analysis']['observed_damage']}")
                    
                    print(f"\n⚙️ FAILURE MODE:")
                    print(f"   {result['analysis']['failure_mode']}")
                    
                    print(f"\n🧠 ROOT CAUSE ANALYSIS (Focused):")
                    if len(result['analysis']['root_cause_analysis']) == 1:
                        print(f"   Primary Cause: {result['analysis']['root_cause_analysis'][0]}")
                    else:
                        for i, cause in enumerate(result['analysis']['root_cause_analysis'], 1):
                            priority = "Primary" if i == 1 else "Secondary"
                            print(f"   {priority} Cause {i}: {cause}")
                    
                    if result['analysis']['technical_notes']:
                        print(f"\n📝 TECHNICAL NOTES:")
                        print(f"   {result['analysis']['technical_notes']}")
                    
                    if result['analysis']['recommendations']:
                        print(f"\n💡 DYNAMIC RECOMMENDATIONS:")
                        print("   (Generated based on specific fault and root cause)")
                        for i, rec in enumerate(result['analysis']['recommendations'], 1):
                            print(f"   {i}. {rec}")
                    
                else:
                    error_text = await response.text()
                    print(f"❌ API Error: {response.status}")
                    print(f"   {error_text}")
                    
    except aiohttp.ClientConnectorError:
        print("❌ Could not connect to API server")
        print("   Make sure the server is running: python -m app.main")
    except Exception as e:
        print(f"❌ Error: {e}")

async def check_api_health():
    """Check if the API is healthy"""
    
    health_url = "http://localhost:8001/api/v1/health"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(health_url) as response:
                if response.status == 200:
                    health = await response.json()
                    print(f"🏥 API Health: {health['status']}")
                    print(f"   Model available: {health['model_available']}")
                    print(f"   API key configured: {health['api_key_configured']}")
                    return health['status'] == 'healthy'
                else:
                    print(f"❌ Health check failed: {response.status}")
                    return False
    except aiohttp.ClientConnectorError:
        print("❌ Could not connect to API server")
        return False

async def main():
    """Main function to test the API"""
    
    print("🚀 GEMINI-BASED BEARING ANALYSIS API CLIENT")
    print("="*60)
    
    # Check API health first
    print("🔍 Checking API health...")
    if not await check_api_health():
        print("\n❌ API is not healthy. Please:")
        print("   1. Start the server: python -m app.main")
        print("   2. Set GOOGLE_API_KEY environment variable")
        print("   3. Try again")
        return
    
    print("\n✅ API is healthy, proceeding with analysis...")
    
    # Test the analysis
    await test_api_analysis()

if __name__ == "__main__":
    asyncio.run(main()) 