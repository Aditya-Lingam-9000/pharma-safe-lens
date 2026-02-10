"""
Unit tests for Drug Database module.
Tests drug name normalization and fuzzy matching.
"""

import pytest
from backend.app.drug_db import DrugDatabase


class TestDrugDatabase:
    """Test suite for drug database functionality."""
    
    @pytest.fixture
    def drug_db(self):
        """Create a DrugDatabase instance for testing."""
        return DrugDatabase()
    
    def test_database_loads(self, drug_db):
        """Test that the database loads successfully."""
        assert len(drug_db.drug_map) > 0
        assert 'aspirin' in drug_db.drug_map
        assert 'warfarin' in drug_db.drug_map
    
    def test_exact_match_generic(self, drug_db):
        """Test exact match with generic drug name."""
        result = drug_db.get_generic_name('aspirin')
        assert result == 'aspirin'
    
    def test_exact_match_brand(self, drug_db):
        """Test exact match with brand name."""
        result = drug_db.get_generic_name('ecosprin')
        assert result == 'aspirin'
        
        result = drug_db.get_generic_name('coumadin')
        assert result == 'warfarin'
    
    def test_case_insensitive(self, drug_db):
        """Test that matching is case-insensitive."""
        assert drug_db.get_generic_name('ASPIRIN') == 'aspirin'
        assert drug_db.get_generic_name('Ecosprin') == 'aspirin'
        assert drug_db.get_generic_name('WARFARIN') == 'warfarin'
    
    def test_fuzzy_match_typo(self, drug_db):
        """Test fuzzy matching with typos."""
        # Common typos should match
        result = drug_db.get_generic_name('asprin')  # Missing 'i'
        assert result == 'aspirin'
        
        result = drug_db.get_generic_name('warfrin')  # Wrong vowel
        assert result == 'warfarin'
    
    def test_no_match_unknown(self, drug_db):
        """Test that unknown drugs return None."""
        result = drug_db.get_generic_name('unknowndrug123')
        assert result is None
        
        result = drug_db.get_generic_name('xyz')
        assert result is None
    
    def test_normalize_single_drug(self, drug_db):
        """Test normalization with a single drug."""
        raw_text = ['ASPIRIN 100MG']
        result = drug_db.normalize(raw_text)
        
        assert 'aspirin' in result
    
    def test_normalize_multiple_drugs(self, drug_db):
        """Test normalization with multiple drugs."""
        raw_text = ['ASPIRIN 100MG', 'WARFARIN 5MG', 'METFORMIN 500MG']
        result = drug_db.normalize(raw_text)
        
        assert 'aspirin' in result
        assert 'warfarin' in result
        assert 'metformin' in result
    
    def test_normalize_with_brand_names(self, drug_db):
        """Test normalization with brand names."""
        raw_text = ['ECOSPRIN', 'COUMADIN', 'GLUCOPHAGE']
        result = drug_db.normalize(raw_text)
        
        assert 'aspirin' in result
        assert 'warfarin' in result
        assert 'metformin' in result
    
    def test_normalize_filters_unknown(self, drug_db):
        """Test that unknown text is filtered out."""
        raw_text = ['ASPIRIN', 'UNKNOWN_DRUG', 'WARFARIN', 'XYZ123']
        result = drug_db.normalize(raw_text)
        
        assert 'aspirin' in result
        assert 'warfarin' in result
        assert len(result) == 2  # Only known drugs
    
    def test_normalize_removes_duplicates(self, drug_db):
        """Test that duplicates are removed."""
        raw_text = ['ASPIRIN', 'ECOSPRIN', 'ASPIRIN 100MG']
        result = drug_db.normalize(raw_text)
        
        # All should map to 'aspirin', but only one entry
        assert result.count('aspirin') == 1
    
    def test_extract_drug_words(self, drug_db):
        """Test extraction of drug words from text."""
        text = "ASPIRIN 100MG TABLETS MFG:2024"
        words = drug_db._extract_drug_words(text)
        
        # Should extract 'ASPIRIN' and filter out dosage/metadata
        assert 'ASPIRIN' in words or 'aspirin' in [w.lower() for w in words]
        assert not any('100' in w for w in words)
        assert not any('MFG' in w.upper() for w in words)
    
    def test_similarity_calculation(self, drug_db):
        """Test similarity score calculation."""
        # Exact match
        assert drug_db._calculate_similarity('aspirin', 'aspirin') == 100.0
        
        # Similar strings
        score = drug_db._calculate_similarity('aspirin', 'asprin')
        assert score > 80.0  # Should be above threshold
        
        # Very different strings
        score = drug_db._calculate_similarity('aspirin', 'xyz')
        assert score < 50.0
