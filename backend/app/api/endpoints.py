from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from typing import List, Dict
import shutil
import os
import uuid
import logging

# Dependencies
from backend.app.dependencies import get_drug_db, get_interaction_checker
from backend.app.ocr import extract_text, preload_ocr
from backend.app.safety import SafetyGuard

from backend.app.inference import AIInference, RealMedGemmaInference

# Initialize real MedGemma model (do this at module level, before endpoint)
print("\n" + "="*70)
print("🚀 INITIALIZING PHARMA-SAFE LENS BACKEND")
print("="*70)

# Pre-load OCR engines to avoid first-request timeout
preload_ocr()

real_inference = RealMedGemmaInference()
print("📦 Attempting to load MedGemma 1.5 model...")
print("   🏥 Model: google/medgemma-1.5-4b-it (Latest MedGemma release)")
print("   🔐 This is a gated model - requires HuggingFace authentication")
# Load MedGemma 1.5 4B - the latest and best model for medical tasks
model_loaded = real_inference.load_model("google/medgemma-1.5-4b-it")

if not model_loaded:
    print("⚠️  WARNING: Failed to load MedGemma, falling back to MOCK inference")
    print("   Possible reasons:")
    print("   - Missing packages: torch, transformers")
    print("   - No GPU available")
    print("   - Model download failed")
    print("   → Install: pip install torch transformers accelerate")
    print("="*70)
    real_inference = None
else:
    # Warmup model for faster first inference
    real_inference.warmup()
    print("✅ SUCCESS: MedGemma model loaded and warmed up!")
    print("="*70)

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
            # 5. AI Explanation Generation (Mock/API) - Returns structured dict
            # Use real MedGemma if loaded, otherwise fallback to mock
            if real_inference is not None:
                # Format prompt for MedGemma
                from backend.app.prompts import PromptTemplates
                prompt = PromptTemplates.format_explanation_prompt(interaction)
                explanation_dict = real_inference.generate_explanation(interaction, prompt)
            else:
                explanation_dict = AIInference.generate_explanation(interaction)
            
            # 6. Safety Validation on explanation text
            # Convert structured explanation to text for safety check
            explanation_text = "\n".join([
                f"Mechanism: {' '.join(explanation_dict.get('mechanism_of_interaction', [])[:2])}",
                f"Clinical: {' '.join(explanation_dict.get('clinical_manifestations', [])[:2])}"
            ])
            is_safe,  _ = SafetyGuard.validate_output(explanation_text)
            
            interaction_result = {
                "drug_pair": interaction['drug_pair'],
                "risk_level": interaction['risk_level'],
                "basic_info": {
                    "mechanism": interaction.get('mechanism', 'Unknown'),
                    "clinical_effect": interaction.get('clinical_effect', 'Unknown'),
                    "recommendation": interaction.get('recommendation', 'Consult healthcare provider')
                },
                "ai_explanation": explanation_dict,  # Structured detailed explanation
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
