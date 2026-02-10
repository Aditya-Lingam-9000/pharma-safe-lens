"""
Drug Database Module - Normalize OCR output to known drug names.

PHASE 1 - Sub-Phase 1.2
"""

from typing import List, Dict, Optional
import json
from pathlib import Path
import Levenshtein
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DrugDatabase:
    """
    Manages drug name normalization and lookup.
    Maps brand names and misspellings to generic drug names.
    """
    
    # Fuzzy matching threshold (0-100, higher = stricter)
    SIMILARITY_THRESHOLD = 80
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the drug database.
        
        Args:
            db_path: Path to the drug knowledge JSON file
        """
        if db_path is None:
            db_path = Path(__file__).parent / "data" / "drug_knowledge.json"
        else:
            db_path = Path(db_path)
            
        self.db_path = db_path
        self.drug_map: Dict[str, Dict] = {}
        self._load_database()
    
    def _load_database(self):
        """Load the drug knowledge database from JSON."""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self.drug_map = json.load(f)
            logger.info(f"Loaded {len(self.drug_map)} drugs from database")
        except FileNotFoundError:
            logger.error(f"Drug database not found: {self.db_path}")
            self.drug_map = {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse drug database: {e}")
            self.drug_map = {}
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two strings using Levenshtein distance.
        
        Args:
            text1: First string
            text2: Second string
            
        Returns:
            Similarity score (0-100)
        """
        text1 = text1.lower().strip()
        text2 = text2.lower().strip()
        
        if text1 == text2:
            return 100.0
        
        # Calculate Levenshtein ratio (0-1)
        ratio = Levenshtein.ratio(text1, text2)
        
        # Convert to percentage
        return ratio * 100.0
    
    def _extract_drug_words(self, text: str) -> List[str]:
        """
        Extract potential drug names from text.
        Filters out numbers, dosages, and common non-drug words.
        
        Args:
            text: Raw text string
            
        Returns:
            List of potential drug name words
        """
        import re
        
        # Remove common non-drug patterns
        text = re.sub(r'\d+\s*(mg|ml|mcg|g|tablets?|pills?|caps?)', '', text, flags=re.IGNORECASE)
        text = re.sub(r'(mfg|exp|batch|lot|strip|pack)[:.]?\s*\S+', '', text, flags=re.IGNORECASE)
        
        # Split into words
        words = text.split()
        
        # Filter out short words and numbers
        words = [w.strip('.,;:()[]{}') for w in words]
        words = [w for w in words if len(w) >= 3 and not w.isdigit()]
        
        return words
    
    def get_generic_name(self, text: str) -> Optional[str]:
        """
        Get the generic name for a drug (from brand name or alias).
        
        Args:
            text: Drug name (brand or generic)
            
        Returns:
            Generic drug name if found, None otherwise
        """
        text_lower = text.lower().strip()
        
        # First, try exact match with generic names
        if text_lower in self.drug_map:
            logger.debug(f"Exact match: '{text}' -> '{text_lower}'")
            return text_lower
        
        # Try exact match with brand names
        for generic_name, data in self.drug_map.items():
            brand_names = [b.lower() for b in data.get('brand_names', [])]
            if text_lower in brand_names:
                logger.debug(f"Brand name match: '{text}' -> '{generic_name}'")
                return generic_name
        
        # Try fuzzy matching with generic names
        best_match = None
        best_score = 0.0
        
        for generic_name in self.drug_map.keys():
            score = self._calculate_similarity(text, generic_name)
            if score >= self.SIMILARITY_THRESHOLD and score > best_score:
                best_score = score
                best_match = generic_name
        
        if best_match:
            logger.debug(f"Fuzzy match: '{text}' -> '{best_match}' (score: {best_score:.1f})")
            return best_match
        
        # Try fuzzy matching with brand names and misspellings
        for generic_name, data in self.drug_map.items():
            all_variants = (
                data.get('brand_names', []) + 
                data.get('common_misspellings', [])
            )
            
            for variant in all_variants:
                score = self._calculate_similarity(text, variant)
                if score >= self.SIMILARITY_THRESHOLD and score > best_score:
                    best_score = score
                    best_match = generic_name
        
        if best_match:
            logger.debug(f"Fuzzy variant match: '{text}' -> '{best_match}' (score: {best_score:.1f})")
            return best_match
        
        logger.debug(f"No match found for: '{text}'")
        return None
    
    def normalize(self, raw_text: List[str]) -> List[str]:
        """
        Normalize OCR output to known drug names.
        
        Args:
            raw_text: List of raw text strings from OCR
            
        Returns:
            List of normalized generic drug names (duplicates removed)
        """
        logger.info(f"Normalizing {len(raw_text)} text segments")
        
        found_drugs = set()
        
        for text in raw_text:
            # Extract potential drug words from text
            words = self._extract_drug_words(text)
            
            # Try to match each word
            for word in words:
                generic_name = self.get_generic_name(word)
                if generic_name:
                    found_drugs.add(generic_name)
            
            # Also try the full text
            generic_name = self.get_generic_name(text)
            if generic_name:
                found_drugs.add(generic_name)
        
        result = sorted(list(found_drugs))
        logger.info(f"Found {len(result)} drugs: {result}")
        return result
