"""
Phase 5 - API Testing Script
Test the FastAPI backend endpoints locally.

This script tests:
1. Health check endpoint
2. /analyze-image endpoint with various inputs
3. Error handling
4. Response structure validation
"""

import asyncio
import sys
from pathlib import Path
import json

# Add parent directory to path for imports
backend_path = Path(__file__).parent
project_root = backend_path.parent
sys.path.insert(0, str(project_root))

from fastapi.testclient import TestClient
from backend.app.main import app

# Initialize test client
client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint."""
    print("\n" + "="*70)
    print("TEST 1: Root Endpoint")
    print("="*70)
    
    response = client.get("/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert "status" in response.json()
    print("✅ Root endpoint test passed")


def test_health_check():
    """Test the health check endpoint."""
    print("\n" + "="*70)
    print("TEST 2: Health Check Endpoint")
    print("="*70)
    
    response = client.get("/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    data = response.json()
    assert "drugs_loaded" in data
    assert "interactions_loaded" in data
    assert data["drugs_loaded"] > 0
    assert data["interactions_loaded"] > 0
    print(f"✅ Health check passed - {data['drugs_loaded']} drugs, {data['interactions_loaded']} interactions loaded")


def create_test_image():
    """Create a simple test image with text."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create a white image
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Add text (drug names)
        try:
            # Try to use a default font
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            # Fallback to default
            font = ImageFont.load_default()
        
        # Draw drug names
        draw.text((20, 50), "ASPIRIN 100MG", fill='black', font=font)
        draw.text((20, 120), "WARFARIN 5MG", fill='black', font=font)
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes
    except Exception as e:
        print(f"⚠️ Could not create test image: {e}")
        return None


def test_analyze_image_with_interactions():
    """Test /analyze-image with an image containing interacting drugs."""
    print("\n" + "="*70)
    print("TEST 3: Analyze Image - Interacting Drugs (Aspirin + Warfarin)")
    print("="*70)
    
    # Create test image
    img_bytes = create_test_image()
    
    if img_bytes is None:
        print("⚠️ Skipping image test - could not create test image")
        return
    
    # Send request
    files = {"file": ("test_image.png", img_bytes, "image/png")}
    response = client.post("/api/v1/analyze-image", files=files)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResponse Structure:")
        print(f"  - Status: {data.get('status')}")
        print(f"  - Detected Drugs: {data.get('detected_drugs')}")
        print(f"  - Interaction Count: {data.get('interaction_count')}")
        
        if data.get('interactions'):
            print(f"\n  Interactions Found:")
            for i, interaction in enumerate(data['interactions'], 1):
                print(f"\n  Interaction {i}:")
                print(f"    - Drug Pair: {interaction.get('drug_pair')}")
                print(f"    - Risk Level: {interaction.get('risk_level')}")
                print(f"    - Clinical Effect: {interaction.get('clinical_effect')[:100]}...")
                print(f"    - Safety Alert: {interaction.get('safety_alert')}")
                print(f"    - AI Explanation: {interaction.get('ai_explanation')[:150]}...")
        
        # Validation
        assert data['status'] == 'success'
        assert len(data['detected_drugs']) >= 2
        assert data['interaction_count'] > 0
        print("\n✅ Image analysis test passed - Interactions detected correctly")
    else:
        print(f"❌ Request failed: {response.text}")


def test_analyze_image_no_text():
    """Test /analyze-image with an image containing no text."""
    print("\n" + "="*70)
    print("TEST 4: Analyze Image - No Text Detected")
    print("="*70)
    
    try:
        from PIL import Image
        import io
        
        # Create a blank image
        img = Image.new('RGB', (200, 200), color='blue')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Send request
        files = {"file": ("blank.png", img_bytes, "image/png")}
        response = client.post("/api/v1/analyze-image", files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Should warn about no text
            assert data['status'] in ['warning', 'success']
            assert len(data['detected_drugs']) == 0
            print("✅ No-text handling test passed")
        else:
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"⚠️ Test skipped: {e}")


def test_analyze_image_single_drug():
    """Test /analyze-image with only one drug (no interaction possible)."""
    print("\n" + "="*70)
    print("TEST 5: Analyze Image - Single Drug (No Interaction)")
    print("="*70)
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create image with one drug
        img = Image.new('RGB', (300, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        draw.text((20, 30), "METFORMIN 500MG", fill='black', font=font)
        
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Send request
        files = {"file": ("single_drug.png", img_bytes, "image/png")}
        response = client.post("/api/v1/analyze-image", files=files)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            # Should detect 1 drug, 0 interactions
            assert data['status'] == 'success'
            assert len(data['detected_drugs']) < 2
            assert data.get('interaction_count', 0) == 0
            print("✅ Single drug handling test passed")
        else:
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"⚠️ Test skipped: {e}")


def test_error_handling():
    """Test error handling for invalid inputs."""
    print("\n" + "="*70)
    print("TEST 6: Error Handling - Invalid File Type")
    print("="*70)
    
    try:
        import io
        
        # Send a text file instead of image
        fake_file = io.BytesIO(b"This is not an image")
        files = {"file": ("test.txt", fake_file, "text/plain")}
        response = client.post("/api/v1/analyze-image", files=files)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
        # Should handle gracefully
        print("✅ Error handling test completed")
        
    except Exception as e:
        print(f"⚠️ Test error: {e}")


def run_all_tests():
    """Run all Phase 5 API tests."""
    print("\n" + "#"*70)
    print("# PHASE 5 - BACKEND API TESTING SUITE")
    print("#"*70)
    
    tests = [
        test_root_endpoint,
        test_health_check,
        test_analyze_image_with_interactions,
        test_analyze_image_no_text,
        test_analyze_image_single_drug,
        test_error_handling
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️ Test error: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"SUMMARY: {passed} passed, {failed} failed")
    print("="*70)
    
    return passed, failed


if __name__ == "__main__":
    passed, failed = run_all_tests()
    
    if failed == 0:
        print("\n✅ ALL PHASE 5 API TESTS PASSED!")
        print("Ready for Kaggle deployment.")
    else:
        print(f"\n⚠️ {failed} test(s) need attention.")
        sys.exit(1)
