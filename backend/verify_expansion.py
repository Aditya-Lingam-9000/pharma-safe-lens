"""
Verification script for expanded drug & interaction database.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.drug_db import DrugDatabase
from backend.app.interaction_logic import InteractionChecker

def verify_expansion():
    print("🔄 Verifying Database Expansion...")
    
    # 1. Verify Drug DB
    db = DrugDatabase()
    print(f"✅ Drug DB Loaded: {len(db.drug_map)} drugs (Expected ~40+)")
    
    # Test new drugs
    new_drugs = ["amoxicillin", "fluoxetine", "alprazolam", "oxycodone", "furosemide"]
    print("\n💊 Checking new drug recognition:")
    for drug in new_drugs:
        normalized = db.get_generic_name(drug)
        status = "✅ Found" if normalized == drug else "❌ Missing"
        print(f"  - {drug.title()}: {status}")

    # 2. Verify Interaction Logic
    checker = InteractionChecker()
    print(f"\n✅ Interaction DB Loaded: {len(checker.interactions)} interactions")
    
    # Test new critical interactions
    print("\n⚠️ Checking critical interactions:")
    critical_pairs = [
        ("fluoxetine", "tramadol"),   # Serotonin Syndrome
        ("alprazolam", "oxycodone"),  # Respiratory Depression
        ("spironolactone", "lisinopril"), # Hyperkalemia
        ("ciprofloxacin", "warfarin") # Bleeding
    ]
    
    for d1, d2 in critical_pairs:
        result = checker.check_interaction(d1, d2)
        print(f"  - {d1.title()} + {d2.title()} -> Risk: {result['risk_level'].upper()}")
        if result['risk_level'] == 'unknown':
            print(f"    ❌ FAILED: Interaction not found!")

if __name__ == "__main__":
    verify_expansion()
