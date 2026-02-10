"""
Data schemas and contracts for the application.
Defines input/output structures for all modules.
"""

from typing import List, Dict, Optional
from pydantic import BaseModel


class DrugInfo(BaseModel):
    """Information about a detected drug."""
    generic_name: str
    brand_names: List[str]
    confidence: float


class InteractionRisk(BaseModel):
    """Drug interaction risk information."""
    drug_pair: tuple[str, str]
    risk_level: str  # "high", "moderate", "low", "unknown"
    reason: str
    source: str  # "knowledge_base" or "insufficient_data"


class AnalysisResponse(BaseModel):
    """Complete analysis response structure."""
    drugs: List[DrugInfo]
    interactions: List[InteractionRisk]
    explanation: str
    language_versions: Optional[Dict[str, str]] = None
    disclaimer: str
