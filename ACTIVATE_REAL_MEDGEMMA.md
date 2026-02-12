# 🤖 Activating Real MedGemma Model

**Current Status**: Application uses MOCK inference (fast, no GPU)  
**This Guide**: How to switch to REAL MedGemma AI model (GPU required)

---

## 📊 What Changes When You Activate Real MedGemma

### Before (Mock - Current):
- ✅ Instant responses (<1 second)
- ✅ Works on CPU (0% GPU usage)
- ✅ No model download needed
- ❌ Same responses for same drug pairs
- ❌ Not using actual AI model

### After (Real MedGemma):
- ✅ True AI-generated explanations
- ✅ Unique responses each time
- ✅ Uses medical knowledge from MedGemma training
- ❌ Slower (5-15 seconds per request)
- ❌ Requires GPU T4 x2 on Kaggle
- ❌ Downloads ~13GB model first time

---

## 🔧 Step-by-Step Activation Guide

### Step 1: Update Kaggle Notebook Settings

**In your Kaggle notebook:**
1. Click ⚙️ Settings (right sidebar)
2. **Accelerator** → Change from "None/CPU" to **"GPU T4 x2"**
3. **Persistence** → Keep as "Session only"
4. **Internet** → Keep "ON"

### Step 2: Modify Backend Code (endpoints.py)

**Open:** `backend/app/api/endpoints.py`

**Find (around line 11):**
```python
from backend.app.inference import AIInference
```

**Replace with:**
```python
from backend.app.inference import AIInference, RealMedGemmaInference

# Initialize real MedGemma model (do this at module level, before endpoint)
real_inference = RealMedGemmaInference()
model_loaded = real_inference.load_model("google/medgemma-7b")

if not model_loaded:
    print("⚠️ Failed to load MedGemma, falling back to mock")
    real_inference = None
```

**Find (around line 81):**
```python
explanation_dict = AIInference.generate_explanation(interaction)
```

**Replace with:**
```python
# Use real MedGemma if loaded, otherwise fallback to mock
if real_inference is not None:
    # Format prompt for MedGemma
    from backend.app.prompts import PromptTemplates
    prompt = PromptTemplates.format_explanation_prompt(interaction)
    explanation_dict = real_inference.generate_explanation(interaction, prompt)
else:
    explanation_dict = AIInference.generate_explanation(interaction)
```

### Step 3: Push Changes to GitHub

```bash
cd D:\Medgemma\pharma-safe-lens
git add backend/app/api/endpoints.py
git commit -m "Activate real MedGemma inference"
git push origin main
```

### Step 4: Restart Kaggle Backend

**In Kaggle notebook:**
1. Stop Cell 7 (FastAPI server) - Click stop button
2. Re-run Cell 3: `!git clone...` → This pulls latest code
3. **Wait for model download** (~5-10 minutes first time):
   ```
   Downloading (…)lve/main/config.json: 100%|██| 571/571 [00:00<00:00]
   Downloading model.safetensors: 13.2GB [05:32<00:00, 39.7MB/s]
   Downloading (…)okenizer_config.json: 100%|██| 2.54k/2.54k
   Downloading (…)cial_tokens_map.json: 100%|██| 636/636
   ```
4. See confirmation:
   ```
   ✅ MedGemma model loaded successfully on cuda
   ```
5. Re-run Cell 7: Start FastAPI + ngrok
6. Copy new ngrok URL
7. Update frontend `api.js` with new URL (if it changed)

### Step 5: Test with Real Model

**First request will be slower:**
- Model warmup: ~2-5 seconds
- Inference: ~5-15 seconds
- **Total**: ~10-20 seconds

**Subsequent requests:**
- ~5-15 seconds (model already warm)

---

## 🧪 Verification Tests

### Test 1: Check GPU Usage

**In Kaggle notebook:**
- After starting server, GPU usage should show **60-80%** when processing requests
- Memory usage: ~12-16GB

### Test 2: Check Model Loading Logs

**Look for in Kaggle logs:**
```
🔧 Loading MedGemma model on cuda...
Downloading (…)lve/main/config.json: 100%
Downloading model.safetensors: 13.2GB
✅ MedGemma model loaded successfully on cuda
```

### Test 3: Compare Responses

**Upload same image twice:**
- Mock: Identical responses every time
- Real MedGemma: Slightly different wording each time

---

## ⚠️ Important Considerations

### Resource Requirements

**Kaggle Free Tier Limits:**
- **GPU quota**: 30 hours/week
- **Session length**: Max 12 hours
- **Internet**: Required for model download

**Model Download:**
- **First time**: Downloads ~13GB (5-10 minutes)
- **Cached**: Subsequent sessions reuse downloaded model (if persistence enabled)
- **Storage**: Consider enabling "Persistence: Files only" to cache model

### Performance Trade-offs

**Pros of Real MedGemma:**
- ✅ Actual AI-generated medical explanations
- ✅ Leverages medical knowledge from training
- ✅ More contextual and nuanced responses
- ✅ Can adapt to different interaction types better

**Cons of Real MedGemma:**
- ❌ Slower response times (5-15s vs <1s)
- ❌ GPU quota consumption
- ❌ Initial setup time (model download)
- ❌ Potential for unexpected outputs (needs more safety testing)

### Safety Considerations

**Even with Real MedGemma:**
- ✅ Safety guardrails still active (safety.py)
- ✅ Regex filters block dangerous patterns
- ✅ Mandatory disclaimers added
- ⚠️ Monitor outputs for hallucinations
- ⚠️ Test thoroughly before public deployment

---

## 🐛 Troubleshooting

### Issue 1: Model Download Fails

**Error:** `HTTPError: 403 Client Error`

**Solution:**
- Check Kaggle Internet is ON
- Verify Hugging Face is accessible
- Try alternative model: `google/medgemma-2b` (smaller, 5GB)

### Issue 2: Out of Memory Error

**Error:** `torch.cuda.OutOfMemoryError`

**Solutions:**
1. Use smaller model: `google/medgemma-2b`
2. Reduce `max_new_tokens` in generation (line ~207):
   ```python
   max_new_tokens=1024,  # Reduced from 2048
   ```
3. Ensure GPU T4 x2 is selected (not T4 x1)

### Issue 3: Slow Inference

**Problem:** Takes >30 seconds per request

**Solutions:**
1. Reduce `max_new_tokens`:
   ```python
   max_new_tokens=512,  # Faster but shorter responses
   ```
2. Adjust temperature (faster but less creative):
   ```python
   temperature=0.5,  # Reduced from 0.7
   ```
3. Use smaller model: `medgemma-2b`

### Issue 4: Model Not Loading

**Error:** `ModuleNotFoundError: No module named 'transformers'`

**Solution:**
```python
# In Kaggle Cell 4, add:
!pip install torch transformers accelerate
```

---

## 📊 Performance Benchmarks

### Mock Inference (Current):
- **Latency**: <1 second
- **GPU Usage**: 0%
- **Memory**: ~2GB RAM
- **Throughput**: 100+ requests/minute

### Real MedGemma (After Activation):
- **Latency**: 5-15 seconds
- **GPU Usage**: 60-80%
- **Memory**: ~14GB GPU RAM
- **Throughput**: 4-6 requests/minute

---

## 🎯 Recommended Approach

### For Development & Testing:
- ✅ Keep using Mock (fast iteration)
- Test UI/UX changes quickly
- No GPU quota usage

### For Demo & Validation:
- ✅ Activate Real MedGemma
- Show actual AI capabilities
- Limited testing (save GPU quota)

### For Production:
- ✅ Use Real MedGemma
- Deploy on cloud with dedicated GPU
- Implement caching for common queries
- Add rate limiting

---

## 🚀 Quick Activation Checklist

- [ ] Change Kaggle setting to GPU T4 x2
- [ ] Modify `endpoints.py` to import and use `RealMedGemmaInference`
- [ ] Push changes to GitHub
- [ ] Stop Kaggle server (Cell 7)
- [ ] Re-clone repository (Cell 3) to get latest code
- [ ] Wait for model download (~10 minutes first time)
- [ ] Restart server (Cell 7)
- [ ] Update frontend ngrok URL if changed
- [ ] Test with sample image
- [ ] Verify GPU usage shows 60-80%
- [ ] Compare response times (should be 5-15 seconds)
- [ ] Check responses are unique each time

---

## 📚 Additional Resources

- **MedGemma Documentation**: https://huggingface.co/google/medgemma-7b
- **Kaggle GPU Documentation**: https://www.kaggle.com/docs/notebooks#gpu-usage
- **Transformers Library**: https://huggingface.co/docs/transformers

---

**🎉 Once activated, you'll be using the actual MedGemma medical AI model!**

**Note**: Model responses may need additional parsing logic (in `_parse_output_to_structure` method) to extract the 5-section structured format. Current implementation falls back to mock structure if parsing fails.
