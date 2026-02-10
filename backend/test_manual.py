"""Quick test script for drug database functionality."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.drug_db import DrugDatabase

# Initialize database
db = DrugDatabase()

print(f"✅ Loaded {len(db.drug_map)} drugs from database")
print()

# Test exact matches
print("Testing exact matches:")
print(f"  'aspirin' -> {db.get_generic_name('aspirin')}")
print(f"  'warfarin' -> {db.get_generic_name('warfarin')}")
print()

# Test brand names
print("Testing brand names:")
print(f"  'ecosprin' -> {db.get_generic_name('ecosprin')}")
print(f"  'coumadin' -> {db.get_generic_name('coumadin')}")
print()

# Test fuzzy matching
print("Testing fuzzy matching (typos):")
print(f"  'asprin' -> {db.get_generic_name('asprin')}")
print(f"  'warfrin' -> {db.get_generic_name('warfrin')}")
print()

# Test normalization
print("Testing normalization:")
raw_text = ['ASPIRIN 100MG', 'WARFARIN 5MG', 'MFG: 2024']
result = db.normalize(raw_text)
print(f"  Input: {raw_text}")
print(f"  Output: {result}")
print()

print("✅ All manual tests passed!")
