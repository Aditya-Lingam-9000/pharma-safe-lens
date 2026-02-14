from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import List, Dict
import shutil
import os
import uuid
import logging
import json
import asyncio

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
print("📦 Attempting to load TxGemma 9B Chat model...")
print("   🏥 Model: google/txgemma-9b-chat (Health AI collection)")
# Load TxGemma 9B Chat - conversational model for drug-interaction explanations
model_loaded = real_inference.load_model("google/txgemma-9b-chat")

if not model_loaded:
    print("⚠️  WARNING: Failed to load TxGemma, falling back to MOCK inference")
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
    print("✅ SUCCESS: TxGemma model loaded and warmed up!")
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


@router.post("/analyze-image-stream")
async def analyze_image_stream(
    file: UploadFile = File(...),
    db = Depends(get_drug_db),
    checker = Depends(get_interaction_checker)
):
    """
    Streaming version of analyze-image.
    Uses Server-Sent Events (SSE) to progressively send each interaction
    result as the AI generates it, so the frontend can display them one-by-one.
    
    Event types:
      - init:        {detected_drugs, interaction_count, interactions_basic}
      - interaction:  {index, interaction}   (one per interaction, with ai_explanation)
      - done:        {}
      - error:       {detail}
    """
    
    # 1. Save uploaded file
    file_extension = file.filename.split(".")[-1]
    temp_filename = f"{uuid.uuid4()}.{file_extension}"
    temp_path = os.path.join(UPLOAD_DIR, temp_filename)
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    logger.info(f"[stream] File saved to {temp_path}")

    async def event_generator():
        try:
            # 2. OCR
            extracted_text = extract_text(temp_path)
            logger.info(f"[stream] OCR: {extracted_text}")

            if not extracted_text:
                yield _sse("init", {
                    "detected_drugs": [],
                    "interaction_count": 0,
                    "interactions_basic": [],
                    "message": "No text detected in the image."
                })
                yield _sse("done", {})
                return

            # 3. Drug normalization
            normalized_drugs = db.normalize(extracted_text)
            logger.info(f"[stream] Drugs: {normalized_drugs}")

            if len(normalized_drugs) < 2:
                yield _sse("init", {
                    "detected_drugs": normalized_drugs,
                    "interaction_count": 0,
                    "interactions_basic": [],
                    "message": "Fewer than 2 drugs detected."
                })
                yield _sse("done", {})
                return

            # 4. Interaction check (fast — no AI yet)
            interactions = checker.check_multiple(normalized_drugs)
            logger.info(f"[stream] Interactions found: {len(interactions)}")

            # Build basic info list (without AI explanations)
            interactions_basic = []
            for ix in interactions:
                interactions_basic.append({
                    "drug_pair": ix['drug_pair'],
                    "risk_level": ix['risk_level'],
                    "basic_info": {
                        "mechanism": ix.get('mechanism', 'Unknown'),
                        "clinical_effect": ix.get('clinical_effect', 'Unknown'),
                        "recommendation": ix.get('recommendation', 'Consult healthcare provider')
                    },
                    "ai_explanation": None,
                    "safety_alert": False
                })

            # Send init event immediately — frontend can start rendering
            yield _sse("init", {
                "detected_drugs": normalized_drugs,
                "interaction_count": len(interactions),
                "interactions_basic": interactions_basic
            })

            # Small delay so frontend can process the init event
            await asyncio.sleep(0.05)

            # 5. Generate AI explanations one-by-one
            for idx, interaction in enumerate(interactions):
                try:
                    if real_inference is not None:
                        from backend.app.prompts import PromptTemplates
                        prompt = PromptTemplates.format_explanation_prompt(interaction)
                        explanation_dict = real_inference.generate_explanation(interaction, prompt)
                    else:
                        explanation_dict = AIInference.generate_explanation(interaction)

                    # Safety check
                    explanation_text = "\n".join([
                        f"Mechanism: {' '.join(explanation_dict.get('mechanism_of_interaction', [])[:2])}",
                        f"Clinical: {' '.join(explanation_dict.get('clinical_manifestations', [])[:2])}"
                    ])
                    is_safe, _ = SafetyGuard.validate_output(explanation_text)

                    result = {
                        "drug_pair": interaction['drug_pair'],
                        "risk_level": interaction['risk_level'],
                        "basic_info": {
                            "mechanism": interaction.get('mechanism', 'Unknown'),
                            "clinical_effect": interaction.get('clinical_effect', 'Unknown'),
                            "recommendation": interaction.get('recommendation', 'Consult healthcare provider')
                        },
                        "ai_explanation": explanation_dict,
                        "safety_alert": not is_safe
                    }

                    yield _sse("interaction", {"index": idx, "interaction": result})
                    logger.info(f"[stream] Sent interaction {idx+1}/{len(interactions)}")

                    # Small yield between interactions
                    await asyncio.sleep(0.05)

                except Exception as ix_err:
                    logger.error(f"[stream] Interaction {idx} failed: {ix_err}")
                    yield _sse("interaction", {
                        "index": idx,
                        "interaction": interactions_basic[idx],
                        "error": str(ix_err)
                    })

            yield _sse("done", {})

        except Exception as e:
            logger.error(f"[stream] Fatal error: {e}")
            yield _sse("error", {"detail": str(e)})

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
                logger.info(f"[stream] Cleaned up {temp_path}")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
        }
    )


def _sse(event: str, data: dict) -> str:
    """Format a Server-Sent Event string."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"
