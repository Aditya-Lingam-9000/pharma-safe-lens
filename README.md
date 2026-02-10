# 🏥 Pharma-Safe Lens

**Visual Drug Interaction Guardian** - A multimodal AI system for detecting drug interactions from pill strip images.

## 🎯 Project Overview

Pharma-Safe Lens uses computer vision and medical AI to help patients identify potential drug interactions by simply photographing their medication strips. The system:

- 📸 Extracts drug names from images using OCR
- 🔍 Checks interactions against verified medical databases
- 🤖 Generates patient-friendly explanations using Google's MedGemma
- 🌐 Supports multiple languages (English, Hindi, Telugu)
- ⚠️ Maintains strict safety guardrails (no diagnosis, no prescriptions)

## 🚨 Important Disclaimers

**This is an informational tool only.** Always consult a qualified healthcare professional before making any decisions about your medications.

**Not for medical diagnosis or treatment.** This system provides educational information about known drug interactions.

## 🏗️ Architecture

### Development Workflow

```
Local (CPU) → GitHub → Kaggle (GPU) → Validation → Next Phase
```

### Technology Stack

- **OCR**: PaddleOCR / Tesseract (CPU-only)
- **AI Model**: Google MedGemma-2B (Kaggle GPU only)
- **Backend**: FastAPI + Python 3.10+
- **Frontend**: React (Phase 6)
- **Data**: FDA/WHO drug interaction databases

## 📁 Repository Structure

```
pharma-safe-lens/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── schemas.py          # Data contracts
│   │   ├── ocr.py              # Image → Text extraction
│   │   ├── drug_db.py          # Drug name normalization
│   │   ├── interaction_logic.py # Deterministic interaction checking
│   │   ├── prompts.py          # MedGemma prompt templates
│   │   └── safety.py           # Safety guardrails
│   │
│   ├── tests/                  # Unit tests
│   └── requirements.txt        # Python dependencies
│
├── notebooks/
│   └── kaggle_runner.ipynb     # Kaggle GPU execution notebook
│
├── frontend/                   # React app (Phase 6)
│
├── README.md
└── .gitignore
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git
- Kaggle account (for GPU/model work)

### Local Setup (Phase 0)

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/pharma-safe-lens.git
   cd pharma-safe-lens
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies (CPU-only)**

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import fastapi, paddleocr; print('Setup successful!')"
   ```

### Kaggle Setup (Phase 3+)

1. Fork this repository on GitHub
2. Create a new Kaggle notebook
3. Add the GitHub repository as a data source
4. Enable GPU accelerator
5. Run `kaggle_runner.ipynb`

## 📋 Development Phases

- [x] **Phase 0**: Repository & Contract Setup ✅
- [ ] **Phase 1**: Drug ID Extraction (OCR)
- [ ] **Phase 2**: Interaction Knowledge Grounding
- [ ] **Phase 3**: MedGemma Reasoning Layer
- [ ] **Phase 4**: Safety & Language Layer
- [ ] **Phase 5**: Backend API
- [ ] **Phase 6**: React Frontend

## 🔒 Safety & Compliance

### Hard Constraints

- ❌ No medical diagnosis
- ❌ No prescription advice
- ❌ No dosage recommendations
- ✅ Mandatory disclaimers on all outputs
- ✅ Grounded in verified medical databases
- ✅ Explainability required

### Competition Compliance

- Built for Kaggle competition
- Reproducible on Kaggle platform
- Uses only `google/medgemma-2b` or `9b`
- No external closed APIs

## 🧪 Testing

```bash
# Run unit tests (local CPU)
cd backend
pytest tests/

# Run integration tests (Kaggle)
# See notebooks/kaggle_runner.ipynb
```

## 📊 Data Sources

- FDA Drug Interaction Database
- WHO Essential Medicines List
- Verified medical literature

## 🤝 Contributing

This is a competition project. Contributions are not currently accepted.

## 📄 License

[To be determined based on competition rules]

## 👥 Team

[Your team information]

## 🙏 Acknowledgments

- Google MedGemma team
- Kaggle competition organizers
- FDA and WHO for public health data

---

**Remember**: This tool is for educational purposes only. Always consult healthcare professionals for medical decisions.
