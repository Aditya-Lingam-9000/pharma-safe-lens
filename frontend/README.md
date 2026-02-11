# 🎨 Pharma-Safe Lens - Frontend

**React + Vite Frontend with Pure Black Theme**

Beautiful, responsive UI for drug interaction analysis with real-time backend integration.

---

## 🎯 Quick Start

### Prerequisites
- Node.js 18+ installed
- Backend running on Kaggle (see [Kaggle Backend Deployment](../notebooks/kaggle_backend_deployment.ipynb))
- ngrok URL from backend

### Installation & Setup

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies (first time only)
npm install

# 3. Configure API URL (see below)
# Edit src/services/api.js

# 4. Start development server
npm run dev

# Frontend opens at: http://localhost:5173
```

---

## ⚙️ Configuration

### Step 1: Get Backend URL

1. Run the Kaggle backend deployment notebook
2. Copy the ngrok URL displayed (format: `https://xxxx-xxxx-xxxx.ngrok.io`)

Example output from Kaggle:
```
🌐 Public URL: https://a1b2-c3d4-e5f6.ngrok.io
```

### Step 2: Update API Configuration

Open `src/services/api.js` and replace the API_BASE_URL:

```javascript
// Before:
const API_BASE_URL = 'http://localhost:8000';

// After (use your actual ngrok URL):
const API_BASE_URL = 'https://a1b2-c3d4-e5f6.ngrok.io';
```

### Step 3: Save & Restart

```bash
# If server is already running, stop it (Ctrl+C) and restart:
npm run dev
```

---

## 🎨 Features

### Pure Black Theme UI
- **Background**: Pure black (#000000)
- **Primary**: Electric blue (#00D9FF)
- **Secondary**: Neon purple (#B829FF)
- **Accent**: Cyber pink (#FF007A)
- **Animations**: Smooth transitions, glowing effects, pulses
- **Responsive**: Mobile-friendly design

### Components

#### 1. ImageUpload Component
- Drag-and-drop zone with hover effects
- File validation (JPG/PNG, max 2MB)
- Image preview with remove option
- Upload button with loading animation
- Step-by-step instructions

#### 2. LoadingSpinner Component
- Animated dual-ring spinner
- Progressive step indicators
- Estimated time display
- Pulsating effects

#### 3. ResultsDisplay Component
- Summary cards (drugs detected, interactions found, analysis time)
- Drug cards grid with icons
- Interaction risk badges (color-coded)
- Expandable/collapsible sections:
  - 🔬 Mechanism of Interaction (7 points)
  - 🏥 Clinical Manifestations (7 points)
  - ⚠️ Risk Factors (7 points)
  - 📋 Monitoring Recommendations (7 points)
  - 💡 Alternative Suggestions (7 points)
- Print-friendly format
- Comprehensive disclaimer

#### 4. ErrorMessage Component
- User-friendly error display
- Retry button
- Troubleshooting tips
- Animated error indication

---

## 📁 Project Structure

```
frontend/
├── index.html              # HTML entry point
├── package.json            # Dependencies
├── vite.config.js          # Vite configuration
├── src/
│   ├── main.jsx           # React entry point
│   ├── App.jsx            # Main application component
│   ├── App.css            # Pure black theme styles
│   ├── components/
│   │   ├── ImageUpload.jsx
│   │   ├── ImageUpload.css
│   │   ├── LoadingSpinner.jsx
│   │   ├── LoadingSpinner.css
│   │   ├── ResultsDisplay.jsx
│   │   ├── ResultsDisplay.css
│   │   ├── ErrorMessage.jsx
│   │   └── ErrorMessage.css
│   └── services/
│       └── api.js         # API integration (Axios)
```

---

## 🔧 API Integration

### API Service (`src/services/api.js`)

```javascript
import axios from 'axios';

const API_BASE_URL = 'YOUR_NGROK_URL_HERE';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 90000, // 90 seconds
  headers: {
    'Accept': 'application/json'
  }
});

export const uploadImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await api.post('/analyze-image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  return response.data;
};
```

### Expected Backend Response

```json
{
  "status": "success",
  "detected_drugs": ["warfarin", "aspirin", "metformin"],
  "interaction_count": 1,
  "interactions": [
    {
      "drug_pair": ["warfarin", "aspirin"],
      "risk_level": "high",
      "basic_info": {
        "mechanism": "Both drugs affect blood clotting",
        "clinical_effect": "Increased bleeding risk",
        "recommendation": "Avoid combination if possible"
      },
      "ai_explanation": {
        "mechanism_of_interaction": ["Point 1: ...", "Point 2: ...", ...],
        "clinical_manifestations": ["Point 1: ...", "Point 2: ...", ...],
        "risk_factors": ["Point 1: ...", ..],
        "monitoring_recommendations": ["Point 1: ...", ...],
        "alternative_suggestions": ["Point 1: ...", ...]
      },
      "safety_alert": false
    }
  ]
}
```

---

## 🧪 Testing

### Manual Testing Flow

1. **Start frontend**: `npm run dev`
2. **Open browser**: http://localhost:5173
3. **Upload image**: Drag & drop or click to browse
4. **Verify upload**: Preview should appear
5. **Click "Analyze"**: Loading animation shows
6. **Wait**: 10-30 seconds for backend processing
7. **View results**: Detailed analysis displayed

### Test Images

Use prescription images with:
- ✅ Clear, legible text
- ✅ Standard drug names (aspirin, warfarin, metformin, etc.)
- ✅ JPG or PNG format
- ✅ < 2MB file size

---

## ⚠️ Troubleshooting

### Common Issues

#### 1. Network Error / No Response from Server

**Problem**: Frontend can't reach backend

**Solutions**:
- ✅ Check backend is running on Kaggle (cell should be executing)
- ✅ Verify ngrok URL in `api.js` is correct and complete
- ✅ Ensure URL doesn't have trailing slash
- ✅ Check Kaggle notebook has "Internet: ON"
- ✅ Restart frontend after updating URL

```bash
# Stop frontend (Ctrl+C)
npm run dev  # Restart
```

#### 2. CORS Error

**Problem**: Cross-Origin Request Blocked

**Solutions**:
- ✅ Backend CORS is pre-configured for all origins
- ✅ Double-check ngrok URL matches exactly
- ✅ Verify URL includes `https://` (not `http://`)
- ✅ Clear browser cache and reload

#### 3. Upload Fails / File Too Large

**Problem**: Image validation error

**Solutions**:
- ✅ Check file is JPG or PNG
- ✅ Verify file size is < 2MB
- ✅ Try different image
- ✅ Compress image if needed

#### 4. Slow Response / Timeout

**Problem**: Request takes too long or times out

**Causes**:
- Normal: OCR + AI takes 10-30 seconds
- Slow: Kaggle backend may be under load
- Timeout: 90 seconds max (configured)

**Solutions**:
- ✅ Wait patiently (first request may be slower)
- ✅ Check Kaggle logs for errors
- ✅ Restart Kaggle notebook if needed
- ✅ Try smaller/simpler image

#### 5. Module Not Found Errors

**Problem**: Missing dependencies

**Solution**:
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

#### 6. Port Already in Use

**Problem**: Port 5173 is occupied

**Solutions**:
```bash
# Option 1: Kill process on port 5173
# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5173 | xargs kill -9

# Option 2: Use different port
# Edit vite.config.js:
server: {
  port: 3000  # Use different port
}
```

---

## 📊 Performance

### Expected Timings

| Operation | Duration | Notes |
|-----------|----------|-------|
| Page Load | < 1s | Initial render |
| Image Select | Instant | File validation |
| Upload | 0.5-2s | Network transfer |
| OCR Processing | 2-5s | Tesseract on Kaggle |
| Drug Normalization | < 1s | Fuzzy matching |
| Interaction Check | < 1s | Database lookup |
| AI Explanation | 5-15s | Mock inference (instant) |
| Safety Validation | < 1s | Regex patterns |
| **Total E2E** | **10-30s** | Complete flow |

### Optimization Tips

- Use compressed images (JPEG 80% quality)
- Keep file sizes under 500KB for faster upload
- Clear, well-lit prescription images improve OCR speed
- First request may cache model, subsequent faster

---

## 🎭 UI Components Demo

### Color Palette

```css
/* Pure Black Theme */
--color-black: #000000;
--color-dark-gray: #0A0A0A;
--color-electric-blue: #00D9FF;
--color-neon-purple: #B829FF;
--color-cyber-pink: #FF007A;
--color-success: #00FF88;
--color-warning: #FFB800;
--color-danger: #FF3366;
```

### Typography

- **Headers**: Bold, gradient text (blue → purple)
- **Body**: White with opacity variants (80%, 60%, 40%)
- **Monospace**: Courier New for technical info

### Animations

- **Fade In**: Smooth entry (0.5s)
- **Slide Up**: Results appearance (0.6s)
- **Pulse**: Icons and badges (2s loop)
- **Glow**: Hover effects on cards
- **Spin**: Loading spinner (0.8s loop)

---

## 🚀 Production Build

### Build for Production

```bash
# Create optimized production build
npm run build

# Output: dist/ folder

# Preview production build
npm run preview
```

### Deploy Options

#### Option 1: Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

#### Option 2: Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod
```

#### Option 3: GitHub Pages
```bash
# Add to package.json:
"homepage": "https://username.github.io/pharma-safe-lens"

npm run build
# Deploy dist/ folder to gh-pages branch
```

---

## 📝 Development

### Hot Reload

Vite provides instant hot module replacement (HMR):
- Save any file → changes appear immediately
- CSS changes → instant update
- Component changes → state preserved
- Fast refresh for React components

### Code Style

```javascript
// Use functional components with hooks
const MyComponent = () => {
  const [state, setState] = useState(initial);
  
  const handleAction = () => {
    // Handler logic
  };
  
  return (
    <div className="my-component">
      {/* JSX */}
    </div>
  );
};
```

### CSS Guidelines

- Use CSS variables for theming
- Module-level CSS files per component
- Mobile-first responsive design
- Smooth transitions (0.2s - 0.5s)
- Accessible color contrast (WCAG AA)

---

## 🔐 Security Notes

### Important Reminders

1. **ngrok URLs are public**: Anyone with the URL can access your backend
2. **Session-based**: URL changes when Kaggle notebook restarts
3. **12-hour limit**: Kaggle max runtime, then restart needed
4. **No authentication**: Current version has no auth layer
5. **Development mode**: Not production-ready without security hardening

### For Production

- [ ] Add authentication (JWT tokens)
- [ ] Implement rate limiting
- [ ] Use proper cloud deployment (AWS/GCP/Azure)
- [ ] Add HTTPS with valid certificates
- [ ] Implement API key management
- [ ] Add user sessions and history
- [ ] Enable logging and monitoring

---

## 📚 Dependencies

```json
{
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "axios": "^1.7.2"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "vite": "^5.3.1"
  }
}
```

**Total Size**: ~150 MB (node_modules)  
**Build Size**: ~450 KB (optimized)

---

## 🎉 Success Checklist

Before considering frontend complete, verify:

- [x] Frontend starts without errors: `npm run dev`
- [x] Browser opens at localhost:5173
- [x] Pure black theme loads correctly
- [x] Image upload works (drag & drop + click)
- [x] File validation shows errors for invalid files
- [x] Preview displays selected image
- [x] Loading animation shows during analysis
- [x] Results display with all sections
- [x] Expand/collapse sections work
- [x] Risk badges show correct colors
- [x] Disclaimer is visible
- [x] Error handling works (try without backend)
- [x] Responsive on mobile (resize browser)
- [x] Print layout works (Ctrl+P)
- [x] No console errors in browser DevTools

---

## 📞 Support

### Need Help?

1. **Check Troubleshooting** section above
2. **Verify Backend** is running on Kaggle
3. **Test API URL** directly: `https://your-ngrok-url.ngrok.io/health`
4. **Browser DevTools**: F12 → Console tab for errors
5. **Network Tab**: See actual API requests/responses

### Common Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Clear cache and reinstall
rm -rf node_modules package-lock.json && npm install
```

---

**🎨 Enjoy the beautiful pure black theme interface!** 🚀
