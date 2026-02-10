"""
Safety Guardrails - Enforce responsible AI usage.

PHASE 4 - Sub-Phase 4.1
"""

from typing import Dict, Any
import re


class SafetyGuardrails:
    """
    Enforces safety rules on all outputs.
    Prevents medical advice, dosage recommendations, etc.
    """
    
    # Forbidden patterns that indicate medical advice
    FORBIDDEN_PATTERNS = [
        r"take\s+\d+\s*(mg|ml|tablets?|pills?)",  # Dosage instructions
        r"stop\s+taking",  # Medication cessation advice
        r"start\s+taking",  # Medication initiation advice
        r"increase\s+dose",  # Dosage changes
        r"decrease\s+dose",
        r"you\s+should\s+(not\s+)?take",  # Direct medication advice
    ]
    
    REQUIRED_DISCLAIMER = (
        "⚠️ IMPORTANT: This is an informational tool only. "
        "Always consult a qualified healthcare professional before making "
        "any decisions about your medications."
    )
    
    @staticmethod
    def validate_output(text: str) -> tuple[bool, str]:
        """
        Validate that output doesn't contain medical advice.
        
        Args:
            text: Generated text to validate
            
        Returns:
            Tuple of (is_safe, reason)
        """
        for pattern in SafetyGuardrails.FORBIDDEN_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return False, f"Contains forbidden medical advice pattern: {pattern}"
        
        return True, "Output is safe"
    
    @staticmethod
    def add_disclaimer(response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add mandatory safety disclaimer to response.
        
        Args:
            response: API response dictionary
            
        Returns:
            Response with disclaimer added
        """
        response["disclaimer"] = SafetyGuardrails.REQUIRED_DISCLAIMER
        return response
    
    @staticmethod
    def sanitize_explanation(explanation: str) -> str:
        """
        Remove any potentially harmful advice from explanation.
        
        Args:
            explanation: Generated explanation text
            
        Returns:
            Sanitized explanation
        """
        # TODO: Implement in Phase 4, Sub-Phase 4.1
        # For now, just validate
        is_safe, reason = SafetyGuardrails.validate_output(explanation)
        if not is_safe:
            raise ValueError(f"Unsafe output detected: {reason}")
        
        return explanation
