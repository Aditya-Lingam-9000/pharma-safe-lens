# Kaggle Setup Instructions

## Important Notes for Kaggle Environment

### System Dependencies (Kaggle Only)

Tesseract OCR engine must be installed on Kaggle. Add this cell at the beginning of your Kaggle notebook:

```python
# Install Tesseract OCR engine (required for pytesseract)
!apt-get update -y
!apt-get install -y tesseract-ocr
```

### Python Dependencies

The `requirements.txt` is configured for Kaggle compatibility:

- **Pillow**: Version locked to `<10.0.0` for EasyOCR compatibility
- **Levenshtein**: Uses `levenshtein>=0.21.1` (not `python-Levenshtein`)

### Installation Order

```python
# Cell 1: System dependencies
!apt-get update -y
!apt-get install -y tesseract-ocr

# Cell 2: Clone repository
!git clone https://github.com/YOUR_USERNAME/pharma-safe-lens.git
%cd pharma-safe-lens/backend

# Cell 3: Python dependencies
!pip install -r requirements.txt
```

## Troubleshooting

### Issue: EasyOCR/Pillow Compatibility Error

**Solution**: Pillow version is locked to `<10.0.0` in requirements.txt

### Issue: Tesseract not found

**Solution**: Install tesseract-ocr system package (see Cell 1 above)

### Issue: Levenshtein import error

**Solution**: Use `levenshtein` package (not `python-Levenshtein`)

## Validation Checklist

After installation, verify:

```python
# Test imports
import easyocr
import pytesseract
import cv2
from backend.app.drug_db import DrugDatabase
from backend.app.ocr import extract_text

print("✅ All imports successful!")
```
