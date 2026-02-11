# 🚀 Pharma-Safe Lens - Complete Deployment Guide

**Step-by-step instructions to deploy the complete application**

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Repository Setup](#repository-setup)
3. [Kaggle Backend Deployment](#kaggle-backend-deployment)
4. [Frontend Configuration](#frontend-configuration)
5. [Testing the Application](#testing-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance & Updates](#maintenance--updates)
8. [Production Considerations](#production-considerations)

---

## Prerequisites

### Required Accounts
- ✅ **GitHub Account**: To host your code repository
- ✅ **Kaggle Account**: With phone verification (for Internet access)
- ✅ **ngrok Account**: Free tier (https://ngrok.com)

### Required Software (Local Machine)
- ✅ **Node.js 18+**: Download from https://nodejs.org
- ✅ **Git**: Download from https://git-scm.com
- ✅ **Web Browser**: Chrome, Firefox, or Edge (latest version recommended)
- ✅ **Text Editor**: VS Code, Sublime, etc.

### Skills Required
- Basic command line usage (PowerShell/Terminal)
- Basic Git operations (commit, push)
- Basic JavaScript/Python understanding (helpful but optional)

---

## Repository Setup

### Step 1: Initialize Git Repository (if not already done)

```powershell
# Navigate to project root
cd D:\Medgemma\pharma-safe-lens

# Initialize git (skip if already initialized)
git init

# Create .gitignore file
@"
# Python
__pycache__/
*.py[cod]
*.log
*.sqlite3
.env
venv/
env/

# Node
node_modules/
dist/
.DS_Store
package-lock.json

# Kaggle
*.ipynb_checkpoints/
"@ | Out-File -FilePath .gitignore -Encoding utf8

# Add all files
git add .

# Commit
git commit -m "Phase 6 Complete: Full stack implementation"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com
2. Click "New Repository"
3. Repository name: `pharma-safe-lens`
4. Description: "AI-powered drug interaction analyzer with MedGemma"
5. Visibility: Public or Private (your choice)
6. **DON'T** initialize with README (we already have one)
7. Click "Create repository"

### Step 3: Push to GitHub

```powershell
# Add remote origin (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/pharma-safe-lens.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Verify**: Go to your GitHub repository URL and confirm all files are visible.

---

## Kaggle Backend Deployment

### Step 1: Create Kaggle Notebook

1. **Login to Kaggle**: https://www.kaggle.com
2. **Navigate to Notebooks**: Click "Code" in top menu
3. **Create New Notebook**:
   - Click "+ New Notebook" button
   - Title: "Pharma-Safe Lens Backend"
   - Type: Notebook (not Script)
   - Language: Python

### Step 2: Configure Notebook Settings

Click "⚙️" (settings) in right sidebar:

**Essential Settings:**
- ✅ **Internet**: ON (Required!)
- ☑️ **GPU**: None (CPU is fine for Phase 6)
- **Persistence**: Session only
- **Environment**: Python (latest)

**Optional (for future Real MedGemma):**
- GPU: T4 x2
- Accelerator: GPU

### Step 3: Upload Deployment Notebook

**Option A: Upload File**
1. Click "File" → "Upload Notebook"
2. Select `notebooks/kaggle_backend_deployment.ipynb`
3. Wait for upload to complete

**Option B: Copy-Paste Cells** (if upload fails)
1. Open `notebooks/kaggle_backend_deployment.ipynb` locally in text editor
2. Copy each cell's code
3. Create new cells in Kaggle and paste content

### Step 4: Update GitHub Repository URL

Find Cell 2 in the notebook:

```python
# Clone the repository
!git clone https://github.com/YOUR_USERNAME/pharma-safe-lens.git
```

**Replace `YOUR_USERNAME`** with your actual GitHub username!

Example:
```python
!git clone https://github.com/johnsmith/pharma-safe-lens.git
```

### Step 5: Configure ngrok Authentication

**Option A: Using Kaggle Secrets (Recommended)**

1. Get ngrok auth token:
   - Go to https://dashboard.ngrok.com/get-started/your-authtoken
   - Copy your auth token (format: `2a...xyz`)

2. Add to Kaggle Secrets:
   - Click "Add-ons" (right sidebar in Kaggle)
   - Click "+ Add Secret"
   - **Label**: `NGROK_AUTH_TOKEN`
   - **Value**: Paste your ngrok token
   - Click "Add"

3. Notebook will automatically use this secret (Cell 5 is pre-configured)

**Option B: Hardcode Token (Quick but less secure)**

Find Cell 5:

```python
# Get token from Kaggle Secrets
from kaggle_secrets import UserSecretsClient
user_secrets = UserSecretsClient()
ngrok_token = user_secrets.get_secret("NGROK_AUTH_TOKEN")
```

Replace with:

```python
# Hardcoded token (not recommended for public notebooks)
ngrok_token = "YOUR_ACTUAL_NGROK_TOKEN_HERE"
```

### Step 6: Run Backend Deployment

**Execute cells in order:**

1. **Cell 1**: Title/Overview (markdown - just read)
2. **Cell 2**: Install Tesseract (~30 seconds)
   ```
   ✅ Wait for "Processing triggers..." message
   ```

3. **Cell 3**: Clone repository (~10 seconds)
   ```
   ✅ Should see "Cloning into 'pharma-safe-lens'..."
   ```

4. **Cell 4**: Install Python dependencies (~60 seconds)
   ```
   ✅ Wait for all packages to install
   ```

5. **Cell 5**: Verify imports (~5 seconds)
   ```
   ✅ Should show "✅ All imports successful!"
   ```

6. **Cell 6**: Configure ngrok authentication (~2 seconds)
   ```
   ✅ Should show "ngrok authenticated successfully"
   ```

7. **Cell 7**: Start FastAPI + ngrok tunnel (~10 seconds, then runs indefinitely)

**THIS IS THE MOST IMPORTANT CELL!**

Expected output:
```
==================================================================
🎉 BACKEND IS READY!
==================================================================

🌐 Public URL: https://a1b2-c3d4-e5f6.ngrok.io

📋 Frontend Configuration:
   1. Copy the URL above
   2. Open: frontend/src/services/api.js
   3. Replace API_BASE_URL with: 'https://a1b2-c3d4-e5f6.ngrok.io'
   4. Save and restart frontend: npm run dev

==================================================================
📡 Server is running... (Keep this cell executing!)
==================================================================

INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**CRITICAL: Copy the ngrok URL!** You'll need it in the next section.

**DON'T STOP THIS CELL!** It must keep running for the backend to work.

---

## Frontend Configuration

### Step 1: Install Dependencies

```powershell
# Navigate to frontend directory
cd D:\Medgemma\pharma-safe-lens\frontend

# Install Node modules (first time only)
npm install

# Wait for installation (~2-3 minutes)
# Should see "added 200 packages" or similar
```

### Step 2: Update API URL

**Open**: `frontend/src/services/api.js`

**Find** (around line 8):
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

**Replace with your ngrok URL** (copied from Kaggle Cell 7):
```javascript
const API_BASE_URL = 'https://a1b2-c3d4-e5f6.ngrok.io';
```

**Important Notes:**
- ⚠️ URL is case-sensitive
- ⚠️ DO NOT add trailing slash (`/`)
- ⚠️ Use `https://` (not `http://`)
- ⚠️ Entire URL must be in quotes

**Example:**
```javascript
// ✅ CORRECT
const API_BASE_URL = 'https://12ab-34cd-56ef.ngrok.io';

// ❌ WRONG - Has trailing slash
const API_BASE_URL = 'https://12ab-34cd-56ef.ngrok.io/';

// ❌ WRONG - Missing quotes
const API_BASE_URL = https://12ab-34cd-56ef.ngrok.io;

// ❌ WRONG - Using http instead of https
const API_BASE_URL = 'http://12ab-34cd-56ef.ngrok.io';
```

**Save the file!**

### Step 3: Start Frontend Server

```powershell
# Start development server
npm run dev
```

Expected output:
```
  VITE v5.3.1  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Browser should auto-open** to http://localhost:5173

**If browser doesn't open:**
- Manually open http://localhost:5173 in your browser

---

## Testing the Application

### Basic Functionality Test

#### 1. Verify Frontend Loads

**Expected:**
- Pure black background (#000000)
- "PHARMA-SAFE LENS" header with gradient (blue → purple)
- Subheading: "AI-Powered Drug Interaction Analysis"
- "Ready to Analyze" intro card
- 4 feature cards (Real-time OCR, Smart Detection, AI Analysis, Safety First)

**If not:**
- Check browser console (F12) for errors
- Verify frontend is running (`npm run dev`)
- Try clearing browser cache (Ctrl+F5)

#### 2. Test Health Endpoint

Open new browser tab:
```
https://YOUR-NGROK-URL.ngrok.io/health
```

**Expected:**
```json
{"status":"healthy"}
```

**If you see:**
- "This site can't be reached" → Kaggle backend not running or ngrok failed
- CORS error → Check browser console, likely URL mismatch in api.js
- Blank page → Check URL spelling and format

#### 3. Upload Test Image

**Use a sample prescription image:**
- Format: JPG or PNG
- Size: < 2MB
- Content: Text with drug names (e.g., "Aspirin", "Warfarin", "Metformin")

**Steps:**
1. Drag image to upload zone OR click "Browse Files"
2. Image preview should appear
3. File name and size displayed
4. Click "🚀 Analyze Prescription"
5. Loading animation appears (dual-ring spinner + 5 steps)
6. Wait 10-30 seconds
7. Results display appears

**Expected Results:**
- Summary section: Shows drugs detected + interaction count
- Detected Drugs: Cards for each drug with pill icons
- Interactions: Cards for each drug pair
- Risk badges: Color-coded (red=high, yellow=moderate, green=low)
- Basic info: 3-line summary (mechanism, effect, recommendation)
- AI Explanation: "🧠 Detailed AI Analysis" heading
- 5 expandable sections (initially expanded):
  - 🔬 Mechanism of Interaction
  - 🏥 Clinical Manifestations  
  - ⚠️ Risk Factors
  - 📋 Monitoring Recommendations
  - 💡 Alternative Suggestions
- Each section: 7 detailed points (2-3 sentences each)
- Disclaimer section at bottom
- Print Report button
- Analyze Another button

#### 4. Test Interactions

**Click section headers** to collapse/expand:
- Sections should smoothly collapse/expand
- Arrow icon rotates (▼ ↔ ▶)
- Content slides up/down

**Test "Analyze Another":**
- Click button
- Should reset to upload state
- Previous results cleared

**Test Error Handling:**
1. Upload .txt file → Should show "Only JPG, JPEG, and PNG files allowed"
2. Upload 5MB image → Should show "File size must be less than 2MB"

---

## Troubleshooting

### Backend Issues

#### Error: "Repository not found"

**Problem**: GitHub username incorrect in Kaggle Cell 2

**Solution**:
```python
# Verify your GitHub username
# Go to https://github.com/YOUR_USERNAME
# If page loads, username is correct

# Update Cell 2:
!git clone https://github.com/CORRECT_USERNAME/pharma-safe-lens.git
```

#### Error: "Invalid ngrok token"

**Problem**: ngrok authentication failed

**Solutions**:
1. Verify token copied correctly (no spaces)
2. Get new token: https://dashboard.ngrok.com/get-started/your-authtoken
3. Update Kaggle Secret or hardcoded value
4. Re-run Cell 6

#### Error: "Address already in use"

**Problem**: Port 8000 occupied

**Solution**:
1. Restart Kaggle kernel: "Run" → "Restart & Run All"
2. If persists, change port in Cell 7:
   ```python
   public_url = ngrok.connect(8001)  # Use different port
   uvicorn.run(app, host="0.0.0.0", port=8001, ...)
   ```

#### Error: "ModuleNotFoundError"

**Problem**: Python dependencies not installed

**Solution**:
```python
# Re-run Cell 4:
!cd pharma-safe-lens/backend && pip install -r requirements.txt
!pip install pyngrok nest-asyncio

# Then re-run Cell 5 (verify imports)
```

### Frontend Issues

#### Error: "Network Error"

**Problem**: Can't connect to backend

**Solutions**:
1. **Verify ngrok URL** in api.js is correct
2. **Check Kaggle backend is running** (Cell 7 should be executing)
3. **Test health endpoint** in browser: `{ngrok_url}/health`
4. **Restart frontend**:
   ```powershell
   # Stop frontend (Ctrl+C)
   npm run dev
   ```

#### Error: "Failed to compile"

**Problem**: Frontend build error

**Solutions**:
```powershell
# Delete node_modules
Remove-Item -Recurse -Force node_modules

# Delete package-lock.json
Remove-Item package-lock.json

# Reinstall
npm install

# Restart
npm run dev
```

#### Error: "Port 5173 already in use"

**Problem**: Port occupied by previous instance

**Solutions**:
```powershell
# Option 1: Kill process on port 5173
netstat -ano | findstr :5173
# Note the PID (last column)
taskkill /PID <PID> /F

# Option 2: Use different port
# Edit vite.config.js:
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,  // Change port
    open: true
  }
})
```

### Integration Issues

#### Problem: Upload succeeds but no results

**Diagnosis Steps:**

1. **Check Kaggle logs** (Cell 7 output):
   - Look for "POST /analyze-image" requests
   - Check for error tracebacks

2. **Check browser console** (F12):
   - Any JavaScript errors?
   - Check Network tab for API response

3. **Verify API response format**:
   - Response should have `detected_drugs`, `interactions` fields
   - Check if `interactions` array is empty

**Common Causes:**
- OCR failed to extract text
- No drugs detected (check drug_knowledge.json)
- No interactions found (expected for non-interacting drugs)

#### Problem: Results display partially

**Symptoms:**
- Basic info shows but no AI explanation
- Some sections missing points

**Causes:**
- Backend returned wrong format
- Frontend parsing error

**Solutions:**
1. Check backend logs for inference errors
2. Verify `ai_explanation` dict has all 5 keys
3. Check browser console for parsing errors

---

## Maintenance & Updates

### Restarting Backend (Kaggle Session Timeout)

**Kaggle sessions expire after 12 hours**

When backend stops:
1. Go back to Kaggle notebook
2. Click "Run All" (reruns all cells)
3. Wait for new ngrok URL (Cell 7)
4. **Copy new URL**
5. Update frontend api.js with new URL
6. Restart frontend: `npm run dev`

### Updating Code

**After making changes to backend:**

```powershell
# Commit changes locally
git add .
git commit -m "Updated backend feature X"
git push origin main

# On Kaggle:
# 1. Stop Cell 7 (click stop button)
# 2. Re-run Cell 3 (git clone - it will pull latest)
# 3. Re-run Cell 7 (starts server with updated code)
```

**After making changes to frontend:**

```powershell
# No restart needed - Vite hot reload
# Just save file, changes appear instantly
```

### Monitoring Backend

**Watch Kaggle Cell 7 logs:**
- Each API request shows as: `POST /analyze-image`
- Errors appear as tracebacks
- INFO level logging shows processing steps

**Check ngrok dashboard:**
- https://dashboard.ngrok.com/tunnels/agents
- See request count, bandwidth usage
- Free tier: 40 requests/minute

---

## Production Considerations

### Current Limitations (Development Setup)

⚠️ **Security:**
- No authentication
- Public ngrok URL (anyone can access)
- No rate limiting
- No input sanitization beyond basic validation

⚠️ **Reliability:**
- 12-hour Kaggle session limit
- ngrok URL changes on restart
- Single server (no load balancing)
- No data persistence
- No error logging to files

⚠️ **Scalability:**
- Single user only (concurrent requests may conflict)
- No caching
- OCR processes each image individually
- Limited by Kaggle resources

### For Production Deployment

**Required Steps:**

1. **Cloud Hosting:**
   - Deploy backend to AWS/GCP/Azure
   - Use EC2/Compute Engine/VM
   - Install dependencies permanently
   - Use persistent storage

2. **Domain & SSL:**
   - Register domain name (e.g., pharmasafelens.com)
   - Point to backend IP
   - Install SSL certificate (Let's Encrypt)

3. **Frontend Hosting:**
   - Deploy to Vercel/Netlify/Cloudflare Pages
   - Build production bundle: `npm run build`
   - Update API URL to production domain

4. **Security:**
   - Add JWT authentication
   - Implement rate limiting (e.g., 10 requests/hour per user)
   - Use environment variables for secrets
   - Add logging (CloudWatch/Stackdriver)
   - Input validation & sanitization

5. **Database:**
   - PostgreSQL for user data
   - Store upload history
   - Track analytics
   - Implement caching (Redis)

6. **Monitoring:**
   - Error tracking (Sentry)
   - Performance monitoring (New Relic)
   - Uptime monitoring (Pingdom)
   - User analytics (Google Analytics)

7. **Compliance:**
   - HIPAA compliance (if handling PHI)
   - Privacy policy
   - Terms of service
   - Data retention policies
   - User consent forms

**Estimated Cost (Monthly):**
- Cloud hosting: $50-200
- Domain: $10-15/year
- SSL: Free (Let's Encrypt)
- Database: $20-100
- Monitoring: $20-50
- **Total: ~$100-350/month**

---

## Quick Reference Commands

### Backend (Kaggle)

```python
# Check if server is running
# Look for "Uvicorn running" message in Cell 7

# Restart server
# Stop Cell 7 → Click "Run All" button

# Update code from GitHub
!cd pharma-safe-lens && git pull origin main

# Test local imports
from backend.app import main
```

### Frontend (Local)

```powershell
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Clear cache and reinstall
Remove-Item -Recurse -Force node_modules
npm install
```

### Testing

```powershell
# Test backend health endpoint
curl https://YOUR-NGROK-URL.ngrok.io/health

# Test frontend locally
Start-Process "http://localhost:5173"

# Check if ports are in use
netstat -ano | findstr :5173  # Frontend
netstat -ano | findstr :8000  # Backend (if running locally)
```

### Git Commands

```powershell
# Stage all changes
git add .

# Commit with message
git commit -m "Your message here"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main

# Check status
git status

# View commit history
git log --oneline
```

---

## Success Checklist

Before considering deployment complete:

### Backend Deployment
- [ ] Kaggle notebook created and configured
- [ ] Internet enabled in notebook settings
- [ ] GitHub repository URL updated in Cell 2
- [ ] ngrok token configured (Secrets or hardcoded)
- [ ] All cells execute without errors
- [ ] Cell 7 shows "🎉 BACKEND IS READY!" message
- [ ] ngrok URL displayed and copied
- [ ] Health endpoint responds: `{ngrok_url}/health`
- [ ] Kaggle logs show "Application startup complete"

### Frontend Configuration
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Dependencies installed (`npm install` completed)
- [ ] API URL updated in src/services/api.js
- [ ] Frontend starts without errors (`npm run dev`)
- [ ] Browser opens to localhost:5173
- [ ] Pure black theme loads correctly
- [ ] No console errors in browser DevTools

### Integration Testing
- [ ] Image upload works (drag-drop + click)
- [ ] File validation works (size + type)
- [ ] Loading spinner displays during analysis
- [ ] Backend logs show request received
- [ ] Results display after 10-30 seconds
- [ ] All UI sections render correctly
- [ ] Expand/collapse sections work
- [ ] Error handling works (test invalid files)
- [ ] Retry button works after errors

### Documentation
- [ ] README.md updated with deployment info
- [ ] PHASE6_COMPLETE.md reviewed
- [ ] DEPLOYMENT_GUIDE.md (this file) completed
- [ ] TASK_TRACKER.md updated to show Phase 6 complete

---

## 📞 Support & Resources

### Official Documentation
- **React**: https://react.dev
- **Vite**: https://vitejs.dev
- **FastAPI**: https://fastapi.tiangolo.com
- **Kaggle**: https://www.kaggle.com/docs
- **ngrok**: https://ngrok.com/docs

### Community Help
- Stack Overflow (tag: react, fastapi, kaggle)
- GitHub Issues (if using public repo)
- Kaggle Forums
- Reddit (r/reactjs, r/fastapi)

### Project Files
- See `PHASE6_COMPLETE.md` for architecture details
- See `frontend/README.md` for frontend-specific info
- See `KAGGLE_QUICK_START.md` for quick reference
- See `notebooks/kaggle_backend_deployment.ipynb` for deployment cells

---

**🎉 Deployment Guide Complete!**

You now have everything needed to deploy and run Pharma-Safe Lens!

**Next Steps:**
1. Follow the steps above in order
2. Test thoroughly with sample images
3. Share with friends/colleagues for feedback
4. Consider production deployment improvements

**Good luck! 🚀💊🛡️**
