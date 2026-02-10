"""
Prompt Engineering for MedGemma.
Safety-first prompts for explanation generation.

PHASE 3 - Sub-Phase 3.1
"""


class PromptTemplates:
    """
    Prompt templates for MedGemma interaction.
    
    CRITICAL RULES:
    - Safety-framed language
    - No medical advice
    - Use grounding info only
    - No diagnosis or prescription
    """
    
    EXPLANATION_PROMPT = """You are a medical safety assistant helping patients understand drug interactions.

Given the following VERIFIED interaction data:
Drug A: {drug_a}
Drug B: {drug_b}
Risk Level: {risk_level}
Verified Reason: {reason}

Your task:
1. Explain this interaction risk in simple, patient-friendly language
2. Use ONLY the verified information provided above
3. DO NOT add new facts or medical advice
4. DO NOT suggest dosage changes
5. Always remind the user to consult a healthcare professional

Generate a clear, concise explanation:"""

    TRANSLATION_PROMPT = """You are a medical translator. Translate the following drug interaction explanation to {target_language}.

Original (English): {original_text}

Rules:
1. Preserve the exact meaning
2. Keep safety warnings intact
3. Do NOT add medical advice
4. Maintain patient-friendly tone

Translation:"""

    SAFETY_DISCLAIMER = """⚠️ IMPORTANT: This is an informational tool only. Always consult a qualified healthcare professional before making any decisions about your medications."""

    @staticmethod
    def format_explanation_prompt(drug_a: str, drug_b: str, risk_level: str, reason: str) -> str:
        """Format the explanation generation prompt."""
        return PromptTemplates.EXPLANATION_PROMPT.format(
            drug_a=drug_a,
            drug_b=drug_b,
            risk_level=risk_level,
            reason=reason
        )
    
    @staticmethod
    def format_translation_prompt(original_text: str, target_language: str) -> str:
        """Format the translation prompt."""
        return PromptTemplates.TRANSLATION_PROMPT.format(
            original_text=original_text,
            target_language=target_language
        )
