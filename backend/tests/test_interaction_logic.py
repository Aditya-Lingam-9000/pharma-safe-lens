"""
Unit tests for Interaction Logic module.
Tests deterministic drug interaction checking.
"""

import pytest
from backend.app.interaction_logic import InteractionChecker


class TestInteractionChecker:
    """Test suite for interaction checking functionality."""
    
    @pytest.fixture
    def checker(self):
        """Create an InteractionChecker instance for testing."""
        return InteractionChecker()
    
    def test_knowledge_base_loads(self, checker):
        """Test that the knowledge base loads successfully."""
        assert len(checker.interactions) > 0
        assert "aspirin+warfarin" in checker.interactions
    
    def test_normalize_pair_key(self, checker):
        """Test that pair keys are normalized correctly."""
        # Order shouldn't matter
        key1 = checker._normalize_pair_key("aspirin", "warfarin")
        key2 = checker._normalize_pair_key("warfarin", "aspirin")
        assert key1 == key2
        assert key1 == "aspirin+warfarin"
        
        # Case shouldn't matter
        key3 = checker._normalize_pair_key("ASPIRIN", "Warfarin")
        assert key3 == key1
    
    def test_check_interaction_high_risk(self, checker):
        """Test detection of high-risk interaction."""
        result = checker.check_interaction("aspirin", "warfarin")
        
        assert result["risk_level"] == "high"
        assert result["drug_pair"] == ("aspirin", "warfarin")
        assert "bleeding" in result["clinical_effect"].lower()
        assert result["source"] != "insufficient_data"
    
    def test_check_interaction_moderate_risk(self, checker):
        """Test detection of moderate-risk interaction."""
        result = checker.check_interaction("lisinopril", "ibuprofen")
        
        assert result["risk_level"] == "moderate"
        assert result["drug_pair"] == ("lisinopril", "ibuprofen")
    
    def test_check_interaction_low_risk(self, checker):
        """Test detection of low-risk interaction."""
        result = checker.check_interaction("metformin", "atorvastatin")
        
        assert result["risk_level"] == "low"
        assert result["drug_pair"] == ("metformin", "atorvastatin")
    
    def test_check_interaction_no_risk(self, checker):
        """Test detection of no interaction."""
        result = checker.check_interaction("aspirin", "metformin")
        
        assert result["risk_level"] == "none"
    
    def test_check_interaction_unknown(self, checker):
        """Test handling of unknown drug pair."""
        result = checker.check_interaction("aspirin", "unknown_drug")
        
        assert result["risk_level"] == "unknown"
        assert result["source"] == "insufficient_data"
        assert "consult" in result["recommendation"].lower()
    
    def test_check_interaction_same_drug(self, checker):
        """Test handling of same drug twice."""
        result = checker.check_interaction("aspirin", "aspirin")
        
        assert result["risk_level"] == "none"
        assert "same" in result["mechanism"].lower()
    
    def test_check_interaction_order_independent(self, checker):
        """Test that order doesn't matter."""
        result1 = checker.check_interaction("aspirin", "warfarin")
        result2 = checker.check_interaction("warfarin", "aspirin")
        
        assert result1["risk_level"] == result2["risk_level"]
        assert result1["mechanism"] == result2["mechanism"]
    
    def test_check_multiple_empty_list(self, checker):
        """Test with empty drug list."""
        result = checker.check_multiple([])
        assert result == []
    
    def test_check_multiple_single_drug(self, checker):
        """Test with single drug."""
        result = checker.check_multiple(["aspirin"])
        assert result == []
    
    def test_check_multiple_two_drugs(self, checker):
        """Test with two drugs."""
        result = checker.check_multiple(["aspirin", "warfarin"])
        
        assert len(result) == 1
        assert result[0]["risk_level"] == "high"
        assert result[0]["drug_pair"] == ("aspirin", "warfarin")
    
    def test_check_multiple_three_drugs(self, checker):
        """Test with three drugs (checks all pairs)."""
        result = checker.check_multiple(["aspirin", "warfarin", "metformin"])
        
        # Should check: aspirin+warfarin, aspirin+metformin, warfarin+metformin
        # aspirin+warfarin = high
        # aspirin+metformin = none (excluded)
        # warfarin+metformin = low
        
        assert len(result) >= 1  # At least the high-risk one
        
        # Check that high-risk interaction is included
        high_risk = [i for i in result if i["risk_level"] == "high"]
        assert len(high_risk) == 1
    
    def test_check_multiple_filters_none_risk(self, checker):
        """Test that 'none' risk interactions are filtered out."""
        result = checker.check_multiple(["aspirin", "metformin"])
        
        # aspirin+metformin has no interaction
        assert len(result) == 0
    
    def test_check_multiple_no_duplicates(self, checker):
        """Test that duplicate pairs aren't checked twice."""
        result = checker.check_multiple(["aspirin", "warfarin", "aspirin"])
        
        # Should only check aspirin+warfarin once
        assert len(result) == 1
    
    def test_get_highest_risk_empty(self, checker):
        """Test highest risk with empty list."""
        result = checker.get_highest_risk([])
        assert result is None
    
    def test_get_highest_risk_single(self, checker):
        """Test highest risk with single interaction."""
        interactions = [
            {"risk_level": "moderate"}
        ]
        result = checker.get_highest_risk(interactions)
        assert result == "moderate"
    
    def test_get_highest_risk_multiple(self, checker):
        """Test highest risk with multiple interactions."""
        interactions = [
            {"risk_level": "low"},
            {"risk_level": "high"},
            {"risk_level": "moderate"}
        ]
        result = checker.get_highest_risk(interactions)
        assert result == "high"
    
    def test_get_highest_risk_priority(self, checker):
        """Test risk priority ordering."""
        interactions = [
            {"risk_level": "unknown"},
            {"risk_level": "low"},
            {"risk_level": "moderate"}
        ]
        result = checker.get_highest_risk(interactions)
        assert result == "moderate"
