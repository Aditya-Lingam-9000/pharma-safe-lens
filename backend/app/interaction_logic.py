"""
Drug Interaction Logic - Deterministic interaction checking.
Uses FDA/WHO data, NO LLM required.

PHASE 2 - Sub-Phase 2.1 & 2.2
"""

from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InteractionChecker:
    """
    Checks for drug-drug interactions using verified knowledge base.
    This is the grounding layer - prevents hallucination.
    """
    
    def __init__(self, kb_path: Optional[str] = None):
        """
        Initialize the interaction checker.
        
        Args:
            kb_path: Path to the interaction knowledge base JSON
        """
        if kb_path is None:
            kb_path = Path(__file__).parent / "data" / "interactions.json"
        else:
            kb_path = Path(kb_path)
            
        self.kb_path = kb_path
        self.interactions: Dict[str, Dict] = {}
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load the interaction knowledge base from JSON."""
        try:
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                self.interactions = json.load(f)
            logger.info(f"Loaded {len(self.interactions)} drug interactions from knowledge base")
        except FileNotFoundError:
            logger.error(f"Interaction knowledge base not found: {self.kb_path}")
            self.interactions = {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse interaction knowledge base: {e}")
            self.interactions = {}
    
    def _normalize_pair_key(self, drug_a: str, drug_b: str) -> str:
        """
        Create normalized key for drug pair.
        Ensures aspirin+warfarin == warfarin+aspirin.
        
        Args:
            drug_a: First drug name
            drug_b: Second drug name
            
        Returns:
            Normalized key (alphabetically sorted, lowercase)
        """
        # Normalize to lowercase and sort alphabetically
        drugs = sorted([drug_a.lower().strip(), drug_b.lower().strip()])
        return "+".join(drugs)
    
    def check_interaction(self, drug_a: str, drug_b: str) -> Dict:
        """
        Check for interaction between two drugs.
        
        Args:
            drug_a: First drug (generic name)
            drug_b: Second drug (generic name)
            
        Returns:
            Dictionary with:
                - risk_level: "high", "moderate", "low", "none", or "unknown"
                - severity: Clinical severity
                - mechanism: How the interaction occurs
                - clinical_effect: What happens clinically
                - recommendation: What to do
                - source: Data source
                - evidence_level: Quality of evidence
                
        Rules:
            - Works without LLM
            - Returns structured facts only
            - Unknown pairs return "insufficient data"
        """
        # Handle same drug
        if drug_a.lower() == drug_b.lower():
            logger.debug(f"Same drug provided twice: {drug_a}")
            return {
                "drug_pair": (drug_a, drug_b),
                "risk_level": "none",
                "severity": "none",
                "mechanism": "Same drug",
                "clinical_effect": "No interaction (same medication)",
                "recommendation": "Standard monitoring for this medication",
                "source": "logical",
                "evidence_level": "n/a"
            }
        
        # Create normalized key
        pair_key = self._normalize_pair_key(drug_a, drug_b)
        
        # Look up in knowledge base
        if pair_key in self.interactions:
            interaction = self.interactions[pair_key].copy()
            interaction["drug_pair"] = (drug_a, drug_b)
            logger.debug(f"Found interaction: {pair_key} -> {interaction['risk_level']}")
            return interaction
        else:
            logger.debug(f"No data for pair: {pair_key}")
            return {
                "drug_pair": (drug_a, drug_b),
                "risk_level": "unknown",
                "severity": "unknown",
                "mechanism": "Insufficient data available",
                "clinical_effect": "Interaction profile not well-characterized",
                "recommendation": "Consult healthcare provider or pharmacist for guidance on this specific combination",
                "source": "insufficient_data",
                "evidence_level": "unknown"
            }
    
    def check_multiple(self, drugs: List[str]) -> List[Dict]:
        """
        Check all pairwise interactions in a list of drugs.
        
        Args:
            drugs: List of drug names (generic)
            
        Returns:
            List of interaction dictionaries for all pairs
            Only returns interactions with risk_level != "none"
        """
        if not drugs:
            logger.debug("Empty drug list provided")
            return []
        
        if len(drugs) == 1:
            logger.debug("Only one drug provided, no interactions to check")
            return []
        
        logger.info(f"Checking interactions for {len(drugs)} drugs")
        
        interactions = []
        checked_pairs = set()
        
        # Check all unique pairs
        for i in range(len(drugs)):
            for j in range(i + 1, len(drugs)):
                drug_a = drugs[i]
                drug_b = drugs[j]
                
                # Create normalized key to avoid duplicate checks
                pair_key = self._normalize_pair_key(drug_a, drug_b)
                
                if pair_key in checked_pairs:
                    continue
                
                checked_pairs.add(pair_key)
                
                # Check interaction
                result = self.check_interaction(drug_a, drug_b)
                
                # Only include if there's a potential concern
                # (exclude "none" risk level)
                if result['risk_level'] != 'none':
                    interactions.append(result)
        
        logger.info(f"Found {len(interactions)} potential interactions")
        return interactions
    
    def get_highest_risk(self, interactions: List[Dict]) -> Optional[str]:
        """
        Get the highest risk level from a list of interactions.
        
        Args:
            interactions: List of interaction dictionaries
            
        Returns:
            Highest risk level: "high", "moderate", "low", "unknown", or None
        """
        if not interactions:
            return None
        
        risk_priority = {
            "high": 4,
            "moderate": 3,
            "low": 2,
            "unknown": 1,
            "none": 0
        }
        
        highest = max(interactions, key=lambda x: risk_priority.get(x['risk_level'], 0))
        return highest['risk_level']
