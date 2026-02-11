from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.drug_db import DrugDatabase
from backend.app.interaction_logic import InteractionChecker

# Initialize App
app = FastAPI(title="Pharma-Safe Lens API", version="0.5.0")

# CORS (Allow Frontend React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State (Loaded on Startup)
# We can load these once and reuse them across requests
db = DrugDatabase()
checker = InteractionChecker()

@app.on_event("startup")
async def startup_event():
    print("✅ Drug Database Loaded")
    print("✅ Interaction Logic Loaded")

@app.get("/")
def read_root():
    return {"status": "Pharma-Safe Lens API is running 🚀"}

@app.get("/health")
def health_check():
    return {
        "drugs_loaded": len(db.drug_map),
        "interactions_loaded": len(checker.interactions)
    }

# Include Routers
from backend.app.api import endpoints
app.include_router(endpoints.router, prefix="/api/v1")
