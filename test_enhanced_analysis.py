#!/usr/bin/env python3
"""
Enhanced Test script for Gemini-based Bearing Fault Analysis
Demonstrates the improved analysis with dynamic recommendations and better confidence
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

async def test_enhanced_analysis():
    print("🔍 TESTING ENHANCED GEMINI-BASED BEARING ANALYSIS")
    print("="*70)
    print("✨ New Features:")
    print("   • Dynamic recommendations based on fault analysis")
    print("   • Focused root cause analysis (1-2 causes max)")
    print("   • Improved confidence scoring")
    print("   • Specific, actionable recommendations")
    print("="*70)
    
    try:
        from app.core.gemini_fault_analyzer import GeminiFaultAnalyzer
        
        # Initialize analyzer
        analyzer = GeminiFaultAnalyzer()
        
        if not analyzer.is_ready():
            print("❌ Analyzer not ready. Please set GOOGLE_API_KEY environment variable.")
            print("   Example: export GOOGLE_API_KEY='your-api-key-here'")
            return
        
        print("✅ Enhanced Gemini analyzer initialized successfully")
        
        # Test with a bearing image
        image_path = "/home/cimcom/Desktop/RCFA/Top 5 Reasons for Premature Bearing Failure _ ACORN®.png"
        
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            print("   Please update the image_path variable with a valid bearing image")
            return
        
        print(f"📸 Analyzing: {image_path}")
        
        # Read image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        print(f"   Image size: {len(image_data):,} bytes")
        
        # Perform enhanced analysis
        print("\n🔍 Performing enhanced Gemini-based analysis...")
        result = await analyzer.analyze_bearing_image(
            image_data=image_data,
            bearing_type="ball_bearing",
            application="Industrial machinery",
            additional_context="High-speed operation, 24/7 usage"
        )
        
        # Display enhanced results
        print(f"\n📊 ENHANCED ANALYSIS RESULTS:")
        print(f"   Processing time: {result.processing_time:.2f} seconds")
        print(f"   Model used: {result.model_used}")
        print(f"   Confidence: {result.analysis.confidence_score:.1%}")
        
        print(f"\n📷 OBSERVED DAMAGE:")
        print(f"   {result.analysis.observed_damage}")
        
        print(f"\n⚙️ FAILURE MODE:")
        print(f"   {result.analysis.failure_mode}")
        
        print(f"\n🧠 ROOT CAUSE ANALYSIS (Focused):")
        if len(result.analysis.root_cause_analysis) == 1:
            print(f"   Primary Cause: {result.analysis.root_cause_analysis[0]}")
        else:
            for i, cause in enumerate(result.analysis.root_cause_analysis, 1):
                priority = "Primary" if i == 1 else "Secondary"
                print(f"   {priority} Cause {i}: {cause}")
        
        if result.analysis.technical_notes:
            print(f"\n📝 TECHNICAL NOTES:")
            print(f"   {result.analysis.technical_notes}")
        
        print(f"\n💡 DYNAMIC RECOMMENDATIONS:")
        print("   (Generated based on specific fault and root cause)")
        for i, rec in enumerate(result.analysis.recommendations, 1):
            print(f"   {i}. {rec}")
        
        print(f"\n✅ Enhanced analysis completed successfully!")
        print(f"   Key improvements:")
        print(f"   • Root causes limited to 1-2 most likely")
        print(f"   • Recommendations tailored to specific fault")
        print(f"   • Improved confidence assessment")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the Prototype directory and dependencies are installed")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_enhanced_analysis()) 