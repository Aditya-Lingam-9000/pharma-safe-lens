"""Quick test script for interaction checking functionality."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.interaction_logic import InteractionChecker

# Initialize checker
checker = InteractionChecker()

print(f"✅ Loaded {len(checker.interactions)} drug interactions from knowledge base")
print()

# Test 1: High-risk interaction
print("=" * 60)
print("Test 1: High-Risk Interaction (Aspirin + Warfarin)")
print("=" * 60)
result = checker.check_interaction("aspirin", "warfarin")
print(f"Risk Level: {result['risk_level'].upper()}")
print(f"Severity: {result['severity']}")
print(f"Mechanism: {result['mechanism']}")
print(f"Clinical Effect: {result['clinical_effect']}")
print(f"Recommendation: {result['recommendation']}")
print()

# Test 2: Moderate-risk interaction
print("=" * 60)
print("Test 2: Moderate-Risk Interaction (Lisinopril + Ibuprofen)")
print("=" * 60)
result = checker.check_interaction("lisinopril", "ibuprofen")
print(f"Risk Level: {result['risk_level'].upper()}")
print(f"Clinical Effect: {result['clinical_effect']}")
print()

# Test 3: Low-risk interaction
print("=" * 60)
print("Test 3: Low-Risk Interaction (Metformin + Atorvastatin)")
print("=" * 60)
result = checker.check_interaction("metformin", "atorvastatin")
print(f"Risk Level: {result['risk_level'].upper()}")
print(f"Clinical Effect: {result['clinical_effect']}")
print()

# Test 4: No interaction
print("=" * 60)
print("Test 4: No Interaction (Aspirin + Metformin)")
print("=" * 60)
result = checker.check_interaction("aspirin", "metformin")
print(f"Risk Level: {result['risk_level'].upper()}")
print(f"Clinical Effect: {result['clinical_effect']}")
print()

# Test 5: Unknown interaction
print("=" * 60)
print("Test 5: Unknown Interaction (Aspirin + Unknown Drug)")
print("=" * 60)
result = checker.check_interaction("aspirin", "unknown_drug")
print(f"Risk Level: {result['risk_level'].upper()}")
print(f"Recommendation: {result['recommendation']}")
print()

# Test 6: Multiple drugs
print("=" * 60)
print("Test 6: Multiple Drugs (Aspirin, Warfarin, Metformin)")
print("=" * 60)
drugs = ["aspirin", "warfarin", "metformin"]
interactions = checker.check_multiple(drugs)
print(f"Checking {len(drugs)} drugs...")
print(f"Found {len(interactions)} potential interactions:")
print()
for i, interaction in enumerate(interactions, 1):
    drug_a, drug_b = interaction['drug_pair']
    print(f"{i}. {drug_a.title()} + {drug_b.title()}")
    print(f"   Risk: {interaction['risk_level'].upper()}")
    print(f"   Effect: {interaction['clinical_effect']}")
    print()

# Test 7: Highest risk
if interactions:
    highest = checker.get_highest_risk(interactions)
    print(f"Highest Risk Level: {highest.upper()}")
    print()

print("=" * 60)
print("✅ All manual tests completed!")
print("=" * 60)
