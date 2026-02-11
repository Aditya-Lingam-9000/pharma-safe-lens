# Phase 6: React Frontend + Kaggle Backend Integration - IMPLEMENTATION PLAN

## 🎯 Objective
Build a complete, production-ready application with:
- **Frontend**: React + Vite running on local machine (pure black theme, plain CSS)
- **Backend**: FastAPI running on Kaggle with GPU-enabled MedGemma
- **Real Functionality**: Actual image upload, OCR, interaction detection, AI explanation
- **Enhanced Output**: Lengthy, structured, point-wise explanations from MedGemma

---

## 📋 Architecture Overview

```
┌─────────────────────────────────────┐
│  LOCAL MACHINE (Windows)            │
│  ┌───────────────────────────┐     │
│  │  React + Vite Frontend    │     │
│  │  - Image Upload UI        │     │
│  │  - Results Display        │     │
│  │  - Pure Black Theme       │     │
│  └───────────┬───────────────┘     │
│              │ HTTP Requests       │
└──────────────┼─────────────────────┘
               │
               │ (via ngrok tunnel)
               ▼
┌─────────────────────────────────────┐
│  KAGGLE NOTEBOOK (GPU T4 x2)        │
│  ┌───────────────────────────┐     │
│  │  FastAPI Backend          │     │
│  │  - OCR (EasyOCR)          │     │
│  │  - Drug Normalization     │     │
│  │  - Interaction Checking   │     │
│  │  - Real MedGemma Model    │     │
│  │  - Safety Validation      │     │
│  └───────────────────────────┘     │
└─────────────────────────────────────┘
```

---

## 🗂️ Phase 6 Sub-Plans

### **Phase 6.1: Frontend Project Setup** ✅ Ready to Implement

**Goal**: Initialize React + Vite project with proper structure

**Steps**:
1. Create `frontend/` directory structure
2. Initialize Vite project with React template
3. Set up project dependencies (axios for API calls)
4. Create component folder structure
5. Set up routing (React Router - optional for single page)

**Deliverables**:
- `frontend/package.json`
- `frontend/vite.config.js`
- `frontend/src/` folder with components
- `frontend/public/` for assets

**Files to Create**:
```
frontend/
├── package.json
├── vite.config.js
├── index.html
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   ├── App.css (pure black theme)
│   ├── components/
│   │   ├── ImageUpload.jsx
│   │   ├── ResultsDisplay.jsx
│   │   ├── LoadingSpinner.jsx
│   │   └── ErrorMessage.jsx
│   └── services/
│       └── api.js (axios config)
└── public/
    └── pharma-logo.svg (optional)
```

**Time**: 15 minutes

---

### **Phase 6.2: Pure Black Theme UI Design** ✅ Ready to Implement

**Goal**: Create beautiful, attractive UI with pure black theme

**Design Specifications**:
- **Background**: Pure black (#000000)
- **Primary Color**: Electric blue (#00D9FF) for CTAs
- **Secondary Color**: Neon purple (#B829FF) for highlights
- **Text**: Pure white (#FFFFFF) with opacity variations
- **Cards**: Dark gray (#0A0A0A) with subtle borders
- **Shadows**: Blue/purple glows for depth
- **Fonts**: Modern sans-serif (Inter/System UI)

**Components**:

1. **ImageUpload Component**:
   - Drag-and-drop zone with glowing border
   - File preview thumbnail
   - Upload button with gradient glow
   - File size/type validation

2. **ResultsDisplay Component**:
   - Detected drugs section (cards with icons)
   - Interaction risk badges (color-coded)
   - AI explanation section (structured points)
   - Expand/collapse sections

3. **LoadingSpinner Component**:
   - Animated pulse/spinner
   - "Analyzing prescription..." text

4. **ErrorMessage Component**:
   - Red-themed error card
   - Retry button

**CSS Features**:
- Smooth animations (fade-in, slide-up)
- Glassmorphism effect on cards
- Gradient text for headers
- Responsive design (mobile-friendly)

**Time**: 30 minutes

---

### **Phase 6.3: Frontend Components Implementation** ✅ Ready to Implement

**Goal**: Build all React components with state management

**1. App.jsx (Main Component)**:
```jsx
State:
- selectedImage: File | null
- uploadedImageUrl: string | null
- loading: boolean
- error: string | null
- results: AnalysisResult | null

Functions:
- handleImageSelect(file)
- handleUpload()
- handleReset()
```

**2. ImageUpload.jsx**:
```jsx
Props:
- onImageSelect: (file: File) => void
- selectedImage: File | null
- loading: boolean

Features:
- Drag-and-drop zone
- Click to browse
- Image preview
- File validation (2MB max, jpg/png only)
```

**3. ResultsDisplay.jsx**:
```jsx
Props:
- results: AnalysisResult

Sections:
- Detected Drugs (with icons)
- Interaction Summary (risk badges)
- Detailed Explanation (point-wise)
- Disclaimer section
```

**Time**: 45 minutes

---

### **Phase 6.4: Enhanced MedGemma Output Formatting** ✅ Ready to Implement

**Goal**: Update backend to generate lengthy, structured, point-wise explanations

**Update Files**:
1. `backend/app/prompts.py`:
   - Add DETAILED_EXPLANATION_FORMAT constant
   - Update system prompt to request structured output

2. `backend/app/inference.py`:
   - Update mock to return structured format
   - Prepare for real MedGemma integration
   - Add formatting function for point-wise output

**New Output Format**:
```json
{
  "explanation": {
    "summary": {
      "risk_level": "HIGH/MODERATE/LOW",
      "affected_drugs": ["warfarin", "aspirin"],
      "recommendation": "Avoid combination if possible"
    },
    "detailed_analysis": {
      "mechanism_of_interaction": [
        "Point 1: Warfarin is an anticoagulant...",
        "Point 2: Aspirin inhibits platelet aggregation...",
        "Point 3: Combined effect significantly increases bleeding risk..."
      ],
      "clinical_manifestations": [
        "Point 1: Increased bleeding time...",
        "Point 2: Risk of internal hemorrhage...",
        "Point 3: Bruising and petechiae..."
      ],
      "risk_factors": [
        "Point 1: Elderly patients (>65 years)...",
        "Point 2: History of GI bleeding...",
        "Point 3: Concurrent use of NSAIDs..."
      ],
      "monitoring_recommendations": [
        "Point 1: Regular INR monitoring (every 1-2 weeks)...",
        "Point 2: Watch for signs of bleeding...",
        "Point 3: Report unusual bruising immediately..."
      ],
      "alternative_suggestions": [
        "Point 1: Consider acetaminophen for pain relief...",
        "Point 2: Discuss with healthcare provider about dose adjustment...",
        "Point 3: Evaluate need for gastroprotective agents..."
      ]
    },
    "disclaimer": "This analysis is for informational purposes only. Always consult qualified healthcare professionals before making medication decisions."
  }
}
```

**Time**: 30 minutes

---

### **Phase 6.5: Kaggle Backend Deployment** ✅ Ready to Implement

**Goal**: Deploy FastAPI backend on Kaggle with real MedGemma model

**New Notebook**: `notebooks/kaggle_backend_deployment.ipynb`

**Cells**:

1. **System Setup**:
   - Install dependencies
   - Clone repository
   - Install ngrok

2. **Real MedGemma Setup**:
   - Download model weights (if not cached)
   - Load model on GPU
   - Test inference

3. **Update Inference**:
   - Replace mock with real model inference
   - Add structured output formatting

4. **Start FastAPI Server**:
   - Run uvicorn on port 8000
   - Enable CORS for external access

5. **Expose with ngrok**:
   - Create ngrok tunnel
   - Get public URL
   - Print URL for frontend connection

6. **Keep Alive**:
   - Run server indefinitely
   - Monitor logs

**Commands**:
```python
# Install ngrok
!pip install pyngrok
!ngrok authtoken YOUR_NGROK_TOKEN

# Start FastAPI
import uvicorn
from pyngrok import ngrok

# Open ngrok tunnel
public_url = ngrok.connect(8000)
print(f"🚀 Backend running at: {public_url}")

# Run server
uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Time**: 20 minutes

---

### **Phase 6.6: Frontend-Backend Integration** ✅ Ready to Implement

**Goal**: Connect local frontend to Kaggle backend

**Update Files**:
1. `frontend/src/services/api.js`:
   - Set API base URL (ngrok URL from Kaggle)
   - Create axios instance with timeout
   - Add uploadImage() function

2. `frontend/src/App.jsx`:
   - Implement handleUpload() with API call
   - Handle response and update state
   - Error handling with retry logic

**API Service**:
```javascript
// api.js
import axios from 'axios';

// UPDATE THIS with your ngrok URL from Kaggle
const API_BASE_URL = 'https://YOUR-NGROK-URL.ngrok.io';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for MedGemma inference
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});

export const uploadImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await api.post('/analyze-image', formData);
  return response.data;
};
```

**Configuration Steps**:
1. Run Kaggle notebook → get ngrok URL
2. Update `frontend/src/services/api.js` with URL
3. Run frontend: `npm run dev`
4. Test image upload

**Time**: 15 minutes

---

### **Phase 6.7: Real MedGemma Integration** ✅ Ready to Implement

**Goal**: Replace mock inference with real MedGemma model

**Create New File**: `backend/app/medgemma_integration.py`

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class MedGemmaInference:
    def __init__(self):
        self.model_name = "google/medgemma-7b"  # or appropriate model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = None
        self.model = None
    
    def load_model(self):
        """Load MedGemma model (call this in Kaggle)"""
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
    
    def generate_explanation(self, interaction_data, system_prompt):
        """Generate structured explanation using real MedGemma"""
        # Format prompt with interaction data
        # Call model inference
        # Parse output into structured format
        # Return formatted explanation
```

**Update**: `backend/app/dependencies.py` to switch between mock and real

**Time**: 25 minutes

---

### **Phase 6.8: Testing & Documentation** ✅ Ready to Implement

**Goal**: Complete end-to-end testing and create comprehensive documentation

**Testing Steps**:
1. Start Kaggle backend (get ngrok URL)
2. Update frontend API URL
3. Start frontend (`npm run dev`)
4. Test with sample prescription images
5. Verify complete flow:
   - Image upload → OCR → normalization → interaction checking → AI explanation → safety validation → display results

**Documentation Files**:
1. `PHASE6_COMPLETE.md`:
   - Complete flow explanation
   - Architecture diagram
   - Setup instructions
   - Troubleshooting guide

2. `FRONTEND_README.md`:
   - How to run frontend locally
   - How to configure API URL
   - UI component documentation

3. `DEPLOYMENT_GUIDE.md`:
   - How to deploy backend on Kaggle
   - How to get ngrok token
   - How to connect frontend to backend

**Time**: 30 minutes

---

## 📊 Implementation Timeline

| Phase | Task | Time | Status |
|-------|------|------|--------|
| 6.1 | Frontend Setup | 15 min | Not Started |
| 6.2 | UI Design (Black Theme) | 30 min | Not Started |
| 6.3 | Components Implementation | 45 min | Not Started |
| 6.4 | Enhanced MedGemma Output | 30 min | Not Started |
| 6.5 | Kaggle Backend Deployment | 20 min | Not Started |
| 6.6 | Frontend-Backend Integration | 15 min | Not Started |
| 6.7 | Real MedGemma Integration | 25 min | Not Started |
| 6.8 | Testing & Documentation | 30 min | Not Started |
| **TOTAL** | **Complete Phase 6** | **~3.5 hours** | **0% Complete** |

---

## 🎨 UI Mockup (Text Description)

```
┌────────────────────────────────────────────────────────────┐
│  [Pure Black Background #000000]                           │
│                                                            │
│     ████████╗ ████╗ PHARMA-SAFE LENS                      │
│     ╚══██╔══╝ ██╔═╝ Drug Interaction Analyzer             │
│        ██║    ██║    [gradient text: blue→purple]         │
│        ██║    ██║                                          │
│                                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │ [Dark Card #0A0A0A with blue glow border]       │     │
│  │                                                  │     │
│  │     📷  Drag & Drop Prescription Image          │     │
│  │         or click to browse                      │     │
│  │                                                  │     │
│  │     [Preview thumbnail if selected]             │     │
│  │                                                  │     │
│  │  [  🚀 Analyze Prescription  ] [gradient btn]   │     │
│  └──────────────────────────────────────────────────┘     │
│                                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  🔍 DETECTED DRUGS                               │     │
│  │  ┌──────┐  ┌──────┐  ┌──────┐                  │     │
│  │  │ 💊  │  │ 💊  │  │ 💊  │                  │     │
│  │  │ War- │  │ Asp- │  │ Met- │                  │     │
│  │  │farin │  │irin  │  │formin│                  │     │
│  │  └──────┘  └──────┘  └──────┘                  │     │
│  └──────────────────────────────────────────────────┘     │
│                                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  ⚠️  INTERACTION ANALYSIS                        │     │
│  │                                                  │     │
│  │  🔴 HIGH RISK: Warfarin + Aspirin               │     │
│  │                                                  │     │
│  │  📋 MECHANISM OF INTERACTION:                   │     │
│  │  • Point 1: Both drugs affect blood clotting... │     │
│  │  • Point 2: Warfarin is an anticoagulant that...│     │
│  │  • Point 3: Aspirin inhibits platelet...        │     │
│  │                                                  │     │
│  │  🏥 CLINICAL MANIFESTATIONS:                    │     │
│  │  • Point 1: Increased bleeding time by 2-3x...  │     │
│  │  • Point 2: Risk of spontaneous hemorrhage...   │     │
│  │                                                  │     │
│  │  [... more sections ...]                        │     │
│  │                                                  │     │
│  │  ℹ️  Disclaimer: Consult healthcare provider... │     │
│  └──────────────────────────────────────────────────┘     │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🔧 Technical Requirements

### Frontend
- Node.js >= 18.x
- React 18.x
- Vite 5.x
- Axios for HTTP requests
- Plain CSS (no Tailwind/Bootstrap)

### Backend (Kaggle)
- Python 3.10+
- FastAPI 0.115+
- Uvicorn 0.30+
- PyTorch 2.x with CUDA
- Transformers (Hugging Face)
- ngrok for tunneling
- GPU: T4 x2 (16GB VRAM)

### Development
- VS Code
- PowerShell terminal
- Git
- Kaggle account with phone verification

---

## ⚠️ Important Notes

1. **ngrok Setup**:
   - Create free account at ngrok.com
   - Get auth token from dashboard
   - 2GB data transfer limit on free tier

2. **Kaggle Session**:
   - Maximum 12 hours runtime (then restart)
   - Need to re-run notebook after timeout
   - Frontend needs URL update if backend restarts

3. **CORS Configuration**:
   - Backend must allow frontend origin
   - Update CORS settings if frontend URL changes

4. **Image Size**:
   - Limit to 2MB for faster uploads
   - Backend validates file type (jpg/png only)

5. **MedGemma Model**:
   - ~14GB model size (downloads on first run)
   - Cached in Kaggle for subsequent runs
   - Inference takes ~5-15 seconds per image

---

## 🚀 Quick Start Commands

### Frontend (Local):
```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:5173
```

### Backend (Kaggle):
1. Upload `kaggle_backend_deployment.ipynb`
2. Enable GPU (T4 x2)
3. Enable Internet
4. Run all cells
5. Copy ngrok URL
6. Update frontend `api.js` with URL

### Testing:
1. Upload prescription image
2. Click "Analyze Prescription"
3. Wait 10-20 seconds
4. See detailed results

---

## 📈 Success Criteria

✅ Frontend runs on `http://localhost:5173`  
✅ Backend runs on Kaggle with ngrok tunnel  
✅ Real image upload works (not mock)  
✅ OCR correctly extracts drug names  
✅ Interaction detection is accurate  
✅ MedGemma generates lengthy, structured explanation  
✅ Safety validation blocks dangerous content  
✅ UI is beautiful with pure black theme  
✅ Complete E2E flow works without errors  
✅ Results display is clean and attractive  

---

## 📝 Next Steps After Phase 6

1. **Production Deployment**:
   - Deploy backend on cloud (AWS/GCP/Azure)
   - Deploy frontend on Vercel/Netlify
   - Remove ngrok dependency

2. **Enhancements**:
   - Add user authentication
   - Save prescription history
   - PDF report generation
   - Multi-language support

3. **Testing**:
   - Unit tests (Jest for frontend)
   - Integration tests
   - Load testing

---

**Let's implement Phase 6 step by step!** 🚀
