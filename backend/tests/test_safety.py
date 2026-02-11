import pytest
from backend.app.safety import SafetyGuard

class TestSafetyGuard:
    def test_safe_explanation(self):
        """Test that a standard safe explanation passes."""
        safe_text = "Aspirin and Warfarin interact to increase bleeding risk. Monitor for signs of bruising."
        is_safe, msg = SafetyGuard.validate_output(safe_text)
        assert is_safe is True
        assert msg == safe_text

    def test_dosage_advice_blocked(self):
        """Test blocking of specific dosage advice."""
        dangerous_text = "You should take 500mg of Aspirin daily."
        is_safe, msg = SafetyGuard.validate_output(dangerous_text)
        assert is_safe is False
        assert "SAFETY ALERT" in msg

    def test_prescription_advice_blocked(self):
        """Test blocking of prescription words."""
        dangerous_text = "I prescribe this medication for your pain."
        is_safe, msg = SafetyGuard.validate_output(dangerous_text)
        assert is_safe is False
        assert "SAFETY ALERT" in msg

    def test_discontinue_advice_blocked(self):
        """Test blocking of dangerous discontinuation advice."""
        dangerous_text = "Stop taking Warfarin immediately."
        is_safe, msg = SafetyGuard.validate_output(dangerous_text)
        assert is_safe is False
        assert "SAFETY ALERT" in msg

    def test_case_insensitivity(self):
        """Test that filters work regardless of case."""
        dangerous_text = "PLEASE INCREASE THE DOSE."
        is_safe, msg = SafetyGuard.validate_output(dangerous_text)
        assert is_safe is False
        assert "SAFETY ALERT" in msg
