# 🚀 Quick Start: Testing on Kaggle (Phases 0-5)

**For Full Details:** See [COMPLETE_KAGGLE_TESTING_GUIDE.md](COMPLETE_KAGGLE_TESTING_GUIDE.md)

---

## ⚡ Fast Track (30 Minutes Total)

### 1️⃣ Push to GitHub (5 minutes)

```powershell
# In PowerShell, navigate to project
cd D:\Medgemma\pharma-safe-lens

# Initialize git (if not done)
git init
git add .
git commit -m "Phase 5 Complete: All backend phases"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/pharma-safe-lens.git

# Push
git branch -M main
git push -u origin main
```

**✅ Verify:** Go to https://github.com/YOUR_USERNAME/pharma-safe-lens and confirm files are there

---

### 2️⃣ Set Up Kaggle (3 minutes)

1. Go to https://www.kaggle.com
2. Create notebook: "Create" → "New Notebook"
3. Name it: "Pharma-Safe Lens - Complete Validation"
4. **Enable Internet:** Settings → Add-ons → Internet → ON
5. **Keep CPU** for now (GPU needed only for Phase 3 real MedGemma)

---

### 3️⃣ Run Setup Cells (5 minutes)

**Cell 1: System Dependencies**
```python
!apt-get update -y
!apt-get install -y tesseract-ocr
!tesseract --version
```

**Cell 2: Clone Repository**
```python
# REPLACE YOUR_USERNAME!
!git clone https://github.com/YOUR_USERNAME/pharma-safe-lens.git
%cd pharma-safe-lens
!ls
```

**Cell 3: Install Python Packages**
```python
%cd backend
!pip install -r requirements.txt
```
⏱️ Takes 3-5 minutes

**Cell 4: Import & Verify**
```python
import sys
sys.path.insert(0, '/kaggle/working/pharma-safe-lens')

from backend.app.drug_db import DrugDatabase
from backend.app.interaction_logic import InteractionChecker
from backend.app.prompts import PromptTemplates
from backend.app.safety import SafetyGuard
from backend.app.inference import AIInference

print("✅ All imports successful!")
```

---

### 4️⃣ Test All Phases (15 minutes)

**Copy remaining cells from:** `notebooks/kaggle_runner.ipynb`

Or run these quick tests:

**Phase 1-2 Test:**
```python
db = DrugDatabase()
checker = InteractionChecker()

# Test
drugs = db.normalize(['ECOSPRIN 75MG', 'WARFARIN 5MG'])
interactions = checker.check_multiple(drugs)

print(f"✅ Detected: {drugs}")
print(f"✅ Found {len(interactions)} interaction(s)")
```

**Phase 4 Test:**
```python
# Test safety guard
safe_text = "This may increase risk. Consult your doctor."
dangerous_text = "Take 500mg of aspirin daily."

is_safe1, _ = SafetyGuard.validate_output(safe_text)
is_safe2, _ = SafetyGuard.validate_output(dangerous_text)

print(f"✅ Safe text: {is_safe1} (should be True)")
print(f"✅ Dangerous blocked: {not is_safe2} (should be True)")
```

**Phase 5 Test:**
```python
# Complete pipeline
interaction = interactions[0]
explanation = AIInference.generate_explanation(interaction)
is_safe, validated = SafetyGuard.validate_output(explanation)

print(f"✅ Generated explanation: {len(explanation)} chars")
print(f"✅ Safety validated: {is_safe}")
```

---

### 5️⃣ Save Your Work (2 minutes)

1. File → Save Version
2. Add note: "Phase 5 Complete - All Backend Validated"
3. ✅ Done!

---

## 📋 Success Checklist

After running all cells, you should see:

- ✅ Tesseract installed (version shown)
- ✅ Repository cloned successfully
- ✅ All dependencies installed (~3-5 min)
- ✅ 15 drugs loaded from database
- ✅ 40+ interactions loaded
- ✅ Drug normalization works (exact, brand, fuzzy)
- ✅ Interaction checking accurate
- ✅ Safety guardrails block dangerous content
- ✅ Mock inference generates explanations
- ✅ Complete pipeline works end-to-end

---

## 🔧 Common Issues & Quick Fixes

| Issue | Solution |
|-------|----------|
| "ModuleNotFoundError: backend" | Add to top of cell: `sys.path.insert(0, '/kaggle/working/pharma-safe-lens')` |
| "git clone failed" | Ensure repo is PUBLIC on GitHub |
| "Levenshtein not found" | Check requirements.txt has `levenshtein>=0.21.1` (lowercase) |
| "No GPU" | Not needed for Phase 1-2-4-5! Only Phase 3 real MedGemma needs GPU |

---

## 🎯 What's Tested

| Phase | What's Validated | Time |
|-------|------------------|------|
| **Phase 0** | Repository structure | Implicit |
| **Phase 1** | OCR + Drug normalization (15 drugs) | 2 min |
| **Phase 2** | Interaction checking (40+ pairs) | 2 min |
| **Phase 3** | Prompt engineering templates | 1 min |
| **Phase 4** | Safety guardrails (6 patterns) | 2 min |
| **Phase 5** | Complete pipeline + API structure | 3 min |
| **Total** | **All backend validated** | **~10 min** |

---

## 🚀 Next Steps

Once Kaggle tests pass:

1. **Phase 6: Frontend** - Build React UI
2. **Real MedGemma** - Replace mock with actual model (optional)
3. **Deploy** - Cloud deployment for production

---

## 📚 Resources

- **Full Guide:** [COMPLETE_KAGGLE_TESTING_GUIDE.md](COMPLETE_KAGGLE_TESTING_GUIDE.md) (detailed 200+ line guide)
- **Your Notebook:** [notebooks/kaggle_runner.ipynb](notebooks/kaggle_runner.ipynb) (ready to use)
- **Phase 5 Docs:** [PHASE5_COMPLETE.md](PHASE5_COMPLETE.md) (complete documentation)

---

**⚡ You're 83% Done! Only Frontend Remains! ⚡**
