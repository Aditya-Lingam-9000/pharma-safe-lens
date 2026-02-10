# Phase 2 Implementation Plan - Interaction Knowledge Grounding

## Goal

Create a **deterministic** drug interaction checker using verified medical data. **NO LLM** - pure lookup and logic.

## Why This Phase is Critical

**Problem**: LLMs can hallucinate drug interactions. We need hard facts.

**Solution**: Build a knowledge base from FDA/WHO data that MedGemma will use for grounding in Phase 3.

---

## Sub-Phase 2.1: Drug Interaction Knowledge Base

### Objective

Create a JSON database of verified drug-drug interactions.

### Data Structure

```json
{
  "aspirin+warfarin": {
    "risk_level": "high",
    "severity": "major",
    "mechanism": "Both drugs affect blood clotting",
    "clinical_effect": "Increased risk of bleeding",
    "recommendation": "Monitor closely, may need dose adjustment",
    "source": "FDA Drug Interactions Database",
    "evidence_level": "well-documented"
  }
}
```

### Implementation

**File**: `backend/app/data/interactions.json`

**Initial Drug Pairs** (15 drugs = ~105 possible pairs):

- Focus on **high-risk** and **moderate-risk** interactions
- Include **no interaction** for safe combinations
- Mark **unknown** for insufficient data

### Data Sources

1. **FDA Drug Interactions**: https://www.fda.gov/drugs/drug-interactions-labeling
2. **Drugs.com Interaction Checker**: https://www.drugs.com/drug_interactions.html
3. **Medscape Drug Interaction Checker**: https://reference.medscape.com/drug-interactionchecker

### Risk Levels

- **high**: Serious/life-threatening (e.g., aspirin + warfarin)
- **moderate**: Significant but manageable (e.g., ibuprofen + lisinopril)
- **low**: Minor, usually not clinically significant
- **none**: No known interaction
- **unknown**: Insufficient data

---

## Sub-Phase 2.2: Deterministic Interaction Resolver

### Objective

Implement logic to check interactions without any AI/LLM.

### Implementation

**File**: `backend/app/interaction_logic.py`

### Key Functions

#### 1. `check_interaction(drug_a, drug_b) -> dict`

**Logic**:

```python
def check_interaction(drug_a, drug_b):
    # Normalize order (aspirin+warfarin == warfarin+aspirin)
    pair_key = "+".join(sorted([drug_a, drug_b]))

    # Look up in knowledge base
    if pair_key in interactions_db:
        return interactions_db[pair_key]
    else:
        return {
            "risk_level": "unknown",
            "reason": "Insufficient data for this combination",
            "source": "insufficient_data"
        }
```

**Rules**:

- ✅ Works without LLM
- ✅ Returns structured facts only
- ✅ Unknown pairs return "insufficient data" (not guesses)

#### 2. `check_multiple(drugs: list) -> list`

**Logic**:

```python
def check_multiple(drugs):
    interactions = []

    # Check all pairs
    for i in range(len(drugs)):
        for j in range(i+1, len(drugs)):
            result = check_interaction(drugs[i], drugs[j])
            if result['risk_level'] != 'none':
                interactions.append(result)

    return interactions
```

**Example**:

```python
drugs = ["aspirin", "warfarin", "metformin"]

# Checks:
# - aspirin + warfarin → HIGH risk
# - aspirin + metformin → LOW risk
# - warfarin + metformin → NONE

# Returns: [high_risk_interaction, low_risk_interaction]
```

---

## Testing Strategy

### Unit Tests

**File**: `backend/tests/test_interaction_logic.py`

**Test Cases**:

1. Known high-risk pair (aspirin + warfarin)
2. Known low-risk pair
3. No interaction pair
4. Unknown pair (returns "insufficient data")
5. Multiple drugs (all pairwise combinations)
6. Same drug twice (should handle gracefully)
7. Order independence (aspirin+warfarin == warfarin+aspirin)

### Manual Testing

**File**: `backend/test_interactions_manual.py`

```python
from backend.app.interaction_logic import InteractionChecker

checker = InteractionChecker()

# Test known dangerous pair
result = checker.check_interaction("aspirin", "warfarin")
print(f"Aspirin + Warfarin: {result['risk_level']}")

# Test multiple drugs
drugs = ["aspirin", "warfarin", "metformin"]
interactions = checker.check_multiple(drugs)
print(f"Found {len(interactions)} interactions")
```

---

## Deliverables

### Files to Create

1. **`backend/app/data/interactions.json`**
   - Drug interaction knowledge base
   - ~20-30 high/moderate risk pairs initially
   - Expandable

2. **`backend/app/interaction_logic.py`** (implement existing contract)
   - `InteractionChecker` class
   - `check_interaction()` method
   - `check_multiple()` method
   - `_normalize_pair_key()` helper

3. **`backend/tests/test_interaction_logic.py`**
   - Comprehensive unit tests
   - All edge cases covered

4. **`backend/test_interactions_manual.py`**
   - Quick manual validation script

---

## Success Criteria

Phase 2 is complete when:

- ✅ Interaction knowledge base created (JSON)
- ✅ `InteractionChecker` class implemented
- ✅ Known dangerous pairs detected correctly
- ✅ Unknown pairs return "insufficient data"
- ✅ All unit tests pass
- ✅ Manual testing confirms functionality
- ✅ No LLM/AI used (pure lookup)
- ✅ Code pushed to GitHub
- ✅ Validated on Kaggle (CPU)

---

## Timeline Estimate

- **Sub-Phase 2.1** (Knowledge Base): 1-2 hours (research + data entry)
- **Sub-Phase 2.2** (Implementation): 1-2 hours (coding + testing)
- **Testing & Validation**: 30 minutes

**Total**: ~3-4 hours

---

## Ready to Start?

Let's begin with Sub-Phase 2.1: Creating the drug interaction knowledge base.
