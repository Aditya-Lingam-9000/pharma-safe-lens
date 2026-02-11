import re
from typing import Tuple

class SafetyGuard:
    """
    Safety Guardrails for MedGemma output.
    Blocks hallucinated medical advice, dosages, and prescriptions.
    """
    
    # Strict patterns that should NEVER appear in the output
    DANGEROUS_PATTERNS = [
        r"\b(take|use|consume)\s+\d+(mg|g|ml|tablets|pills)",  # e.g., "take 500mg"
        r"\b(prescribe|prescription)",                        # e.g., "I prescribe"
        r"\b(diagnose|diagnosis)",                            # e.g., "I diagnose you"
        r"\b(stop|discontinue)\s+(taking|using)\s+immediately",# Dangerous advice
        r"\b(increase|decrease)\s+(the\s+)?dose",            # Dosage change
        r"\b(treatment\s+plan)",                              # Medical planning
    ]

    @staticmethod
    def validate_output(text: str) -> Tuple[bool, str]:
        """
        Check if the text contains any dangerous patterns.
        
        Args:
            text (str): The AI-generated text.
            
        Returns:
            (bool, str): (is_safe, sanitized_text_or_warning)
        """
        if not text:
            return False, "Error: Empty output."

        # Check for dangerous patterns
        for pattern in SafetyGuard.DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return False, "⚠️ SAFETY ALERT: The AI output contained potential medical advice or dosage instructions, which has been blocked for your safety. Please consult a doctor."

        # Check for mandatory disclaimer (soft check, or enforce injection)
        # We don't block if missing, but we append it if missing in the final app.
        # Here we just validate safety.
        
        return True, text
