"""
Drug Interaction Logic - Deterministic interaction checking.
Uses FDA/WHO data, NO LLM required.

PHASE 2 - Sub-Phase 2.1 & 2.2
"""

from typing import Dict, Optional
from pathlib import Path
import json


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
        self.kb_path = kb_path or Path(__file__).parent / "data" / "interactions.json"
        self.interactions: Dict[str, Dict] = {}
        # TODO: Load knowledge base in Phase 2, Sub-Phase 2.1
    
    def check_interaction(self, drug_a: str, drug_b: str) -> Dict:
        """
        Check for interaction between two drugs.
        
        Args:
            drug_a: First drug (generic name)
            drug_b: Second drug (generic name)
            
        Returns:
            Dictionary with:
                - risk: "high", "moderate", "low", or "unknown"
                - reason: Explanation of the interaction
                - source: "knowledge_base" or "insufficient_data"
                
        Rules:
            - Works without LLM
            - Returns structured facts only
            - Unknown pairs return "insufficient data"
        """
        # TODO: Implement in Phase 2, Sub-Phase 2.2
        raise NotImplementedError("Interaction checking not yet implemented")
    
    def check_multiple(self, drugs: list[str]) -> list[Dict]:
        """
        Check all pairwise interactions in a list of drugs.
        
        Args:
            drugs: List of drug names (generic)
            
        Returns:
            List of interaction dictionaries for all pairs
        """
        # TODO: Implement in Phase 2, Sub-Phase 2.2
        raise NotImplementedError("Multiple interaction checking not yet implemented")
