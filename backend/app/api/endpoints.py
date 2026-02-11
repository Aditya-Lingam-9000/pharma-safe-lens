from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from typing import List, Dict
import shutil
import os
import uuid
import logging

# Dependencies
from backend.app.dependencies import get_drug_db, get_interaction_checker
from backend.app.ocr import extract_text
from backend.app.inference import AIInference
from backend.app.safety import SafetyGuard

# Router initialization
router = APIRouter()
logger = logging.getLogger(__name__)

# Temporary directory for uploads
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze-image", response_model=Dict)
async def analyze_image(
    file: UploadFile = File(...),
    db = Depends(get_drug_db),
    checker = Depends(get_interaction_checker)
):
    """
    Analyze an uploaded image for drug interactions.
    
    Steps:
    1. OCR Extraction
    2. Drug Name Normalization
    3. Interaction Check
    4. AI Explanation Generation (Mock/API)
    5. Safety Validation
    """
    
    # 1. Save Uploaded File
    file_extension = file.filename.split(".")[-1]
    temp_filename = f"{uuid.uuid4()}.{file_extension}"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.info(f"File saved to {temp_path}")
        
        # 2. OCR Extraction
        extracted_text = extract_text(temp_path)
        logger.info(f"OCR Result: {extracted_text}")
        
        if not extracted_text:
            return {
                "status": "warning",
                "message": "No text detected in the image.",
                "detected_drugs": [],
                "interactions": []
            }

        # 3. Drug Name Normalization
        normalized_drugs = db.normalize(extracted_text)
        logger.info(f"Normalized Drugs: {normalized_drugs}")
        
        if len(normalized_drugs) < 2:
            return {
                "status": "success",
                "message": "Fewer than 2 drugs detected. No interactions check possible.",
                "detected_drugs": normalized_drugs,
                "interactions": []
            }

        # 4. Interaction Check
        interactions = checker.check_multiple(normalized_drugs)
        logger.info(f"Interactions Found: {len(interactions)}")
        
        results = []
        for interaction in interactions:
            # 5. AI Explanation Generation (Mock/API)
            explanation = AIInference.generate_explanation(interaction)
            
            # 6. Safety Validation
            is_safe, validated_explanation = SafetyGuard.validate_output(explanation)
            
            interaction_result = {
                "drug_pair": interaction['drug_pair'],
                "risk_level": interaction['risk_level'],
                "clinical_effect": interaction['clinical_effect'],
                "recommendation": interaction['recommendation'],
                "ai_explanation": validated_explanation,
                "safety_alert": not is_safe
            }
            results.append(interaction_result)
            
        return {
            "status": "success",
            "detected_drugs": normalized_drugs,
            "interaction_count": len(results),
            "interactions": results
        }

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup: Remove temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            logger.info(f"Cleaned up {temp_path}")
