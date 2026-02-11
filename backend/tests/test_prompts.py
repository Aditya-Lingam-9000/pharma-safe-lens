import pytest
from backend.app.prompts import PromptTemplates

class TestPromptTemplates:
    def test_format_explanation_prompt_structure(self):
        """Test that the explanation prompt is formatted with all required fields."""
        interaction_data = {
            "drug_pair": ("aspirin", "warfarin"),
            "risk_level": "high",
            "mechanism": "Both affect blood clotting",
            "clinical_effect": "Increased bleeding risk",
            "recommendation": "Avoid combination"
        }
        
        prompt = PromptTemplates.format_explanation_prompt(interaction_data)
        
        # Check for key components
        assert "Aspirin" in prompt
        assert "Warfarin" in prompt
        assert "HIGH" in prompt
        assert "Both affect blood clotting" in prompt
        assert "Increased bleeding risk" in prompt
        assert "Avoid combination" in prompt
        
        # Check for system instructions
        assert "You are MedGemma" in prompt
        assert "DO NOT hallucinate" in prompt
        assert "DO NOT give medical advice" in prompt
        
    def test_format_explanation_prompt_missing_data(self):
        """Test that the prompt handles missing data gracefully."""
        # Minimal data
        interaction_data = {
            "drug_pair": "aspirin+unknown"
        }
        
        prompt = PromptTemplates.format_explanation_prompt(interaction_data)
        
        # Should fill defaults
        assert "Aspirin" in prompt
        assert "Unknown" in prompt
        assert "UNKNOWN" in prompt  # Risk level default
        assert "No mechanism data available" in prompt
        assert "Consult your doctor" in prompt

    def test_safety_disclaimer_presence(self):
        """Ensure the safety disclaimer is accessible."""
        disclaimer = PromptTemplates.get_safety_disclaimer()
        assert "informational tool only" in disclaimer.lower()
        assert "consult your doctor" in disclaimer.lower()

    def test_translation_prompt_structure(self):
        """Test the translation prompt formatting."""
        original = "Consult your doctor immediately."
        target = "Spanish"
        
        prompt = PromptTemplates.format_translation_prompt(original, target)
        
        # Check components
        assert "medical translator" in prompt
        assert "medical advice" in prompt  # Safety rule
        assert "Original (English): Consult your doctor immediately." in prompt
        assert "Target Language: Spanish" in prompt
        assert "[INST]" in prompt
