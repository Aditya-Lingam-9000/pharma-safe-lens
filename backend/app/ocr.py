"""
OCR Module - Extract text from pill strip images.
Uses EasyOCR (primary) and Tesseract (fallback) - CPU-only, no GPU required.

PHASE 1 - Sub-Phase 1.1
"""

from typing import List, Optional
import cv2
import numpy as np
from PIL import Image
import pytesseract
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global EasyOCR reader (lazy loaded)
_easyocr_reader = None


def _get_easyocr_reader():
    """Lazy load EasyOCR reader to avoid import issues."""
    global _easyocr_reader
    if _easyocr_reader is None:
        try:
            import easyocr
            logger.info("Initializing EasyOCR reader (CPU-only)...")
            _easyocr_reader = easyocr.Reader(['en'], gpu=False)
            logger.info("EasyOCR reader initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize EasyOCR: {e}")
            _easyocr_reader = False  # Mark as failed
    return _easyocr_reader if _easyocr_reader is not False else None


def preload_ocr():
    """Pre-initialize OCR engines at startup to avoid first-request delay."""
    logger.info("🔤 Pre-loading OCR engines...")
    reader = _get_easyocr_reader()
    if reader:
        logger.info("✅ EasyOCR pre-loaded successfully")
    else:
        logger.warning("⚠️ EasyOCR not available, will use Tesseract fallback")


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Preprocess image for better OCR accuracy.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Preprocessed image as numpy array
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding for better contrast
    processed = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(processed, None, 10, 7, 21)
    
    return denoised


def extract_text_easyocr(image_path: str) -> Optional[List[str]]:
    """
    Extract text using EasyOCR.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        List of detected text strings, or None if EasyOCR fails
    """
    reader = _get_easyocr_reader()
    if reader is None:
        return None
    
    try:
        # Preprocess image
        processed_img = preprocess_image(image_path)
        
        # Run EasyOCR
        results = reader.readtext(processed_img)
        
        # Extract text from results (format: [(bbox, text, confidence), ...])
        texts = [text.strip() for (bbox, text, conf) in results if text.strip()]
        
        logger.info(f"EasyOCR extracted {len(texts)} text segments")
        return texts
    
    except Exception as e:
        logger.error(f"EasyOCR failed: {e}")
        return None


def extract_text_tesseract(image_path: str) -> List[str]:
    """
    Extract text using Tesseract OCR (fallback).
    
    Args:
        image_path: Path to the image file
        
    Returns:
        List of detected text strings
    """
    try:
        # Preprocess image
        processed_img = preprocess_image(image_path)
        
        # Convert to PIL Image for Tesseract
        pil_img = Image.fromarray(processed_img)
        
        # Run Tesseract
        text = pytesseract.image_to_string(pil_img)
        
        # Split into lines and filter empty
        texts = [line.strip() for line in text.split('\n') if line.strip()]
        
        logger.info(f"Tesseract extracted {len(texts)} text segments")
        return texts
    
    except Exception as e:
        logger.error(f"Tesseract failed: {e}")
        return []


def extract_text(image_path: str) -> List[str]:
    """
    Extract raw text from a pill strip image.
    
    Tries EasyOCR first, falls back to Tesseract if needed.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        List of detected text strings (unprocessed)
        
    Rules:
        - CPU-only execution
        - No interpretation of text
        - Returns raw OCR output only
        
    Example:
        >>> texts = extract_text("pill_strip.jpg")
        >>> print(texts)
        ['ASPIRIN 100MG', 'MFG: 2024', 'EXP: 2026']
    """
    logger.info(f"Extracting text from: {image_path}")
    
    # Try EasyOCR first
    texts = extract_text_easyocr(image_path)
    
    # Fallback to Tesseract if EasyOCR fails
    if texts is None:
        logger.info("Falling back to Tesseract OCR")
        texts = extract_text_tesseract(image_path)
    
    logger.info(f"Total extracted text segments: {len(texts)}")
    return texts
