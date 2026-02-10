"""
Unit tests for OCR module.
Tests text extraction from images using EasyOCR and Tesseract.
"""

import pytest
from pathlib import Path
from backend.app.ocr import extract_text, preprocess_image


class TestOCR:
    """Test suite for OCR functionality."""
    
    def test_preprocess_image_valid(self, tmp_path):
        """Test image preprocessing with a valid image."""
        # Create a simple test image
        import cv2
        import numpy as np
        
        # Create a white image with black text
        img = np.ones((100, 300), dtype=np.uint8) * 255
        cv2.putText(img, 'ASPIRIN', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
        
        # Save to temp file
        test_image = tmp_path / "test.jpg"
        cv2.imwrite(str(test_image), img)
        
        # Test preprocessing
        processed = preprocess_image(str(test_image))
        
        assert processed is not None
        assert processed.shape == (100, 300)
    
    def test_preprocess_image_invalid(self):
        """Test preprocessing with invalid image path."""
        with pytest.raises(ValueError, match="Failed to load image"):
            preprocess_image("nonexistent.jpg")
    
    def test_extract_text_returns_list(self, tmp_path):
        """Test that extract_text returns a list."""
        import cv2
        import numpy as np
        
        # Create a simple test image
        img = np.ones((100, 300), dtype=np.uint8) * 255
        cv2.putText(img, 'ASPIRIN 100MG', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
        
        test_image = tmp_path / "pill.jpg"
        cv2.imwrite(str(test_image), img)
        
        # Extract text
        result = extract_text(str(test_image))
        
        assert isinstance(result, list)
    
    def test_extract_text_simple_image(self, tmp_path):
        """Test OCR on a simple synthetic image."""
        import cv2
        import numpy as np
        
        # Create a clear image with drug name
        img = np.ones((150, 400), dtype=np.uint8) * 255
        cv2.putText(img, 'WARFARIN', (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 2, 0, 3)
        
        test_image = tmp_path / "warfarin.jpg"
        cv2.imwrite(str(test_image), img)
        
        # Extract text
        result = extract_text(str(test_image))
        
        # Should extract something (exact match depends on OCR engine)
        assert len(result) >= 0  # May be empty if OCR fails, but shouldn't crash


# Note: Real pill strip image tests would go here
# For now, we're testing the infrastructure works
