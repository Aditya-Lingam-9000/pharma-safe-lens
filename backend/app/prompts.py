"""
Prompt Engineering for MedGemma.
Safety-first prompts for explanation generation.

PHASE 3 - OPTIMIZED for Phase 6: Concise but comprehensive explanations
"""


class PromptTemplates:
    """
    Prompt templates for MedGemma interaction.
    OPTIMIZED for fast inference on T4 GPU (target: <15 seconds)
    """
    
    # Concise System Prompt
    SYSTEM_PROMPT = """You are MedGemma, a medical AI that explains drug interactions.
RULES: Only use verified facts provided. No medical advice. Advise consulting doctors."""

    # Optimized concise prompt for faster generation
    EXPLANATION_PROMPT = """Analyze this drug interaction concisely:

Drug A: {drug_a}
Drug B: {drug_b}
Risk: {risk_level}
Mechanism: {reason}
Effect: {effect}

Provide brief analysis in these sections (2-3 key points each):

1. MECHANISM: How these drugs interact pharmacologically
2. SYMPTOMS: What clinical effects may occur
3. RISK FACTORS: Who is most at risk
4. MONITORING: What to watch for
5. ALTERNATIVES: General safer options

Keep responses focused and clinically relevant. End with: Consult your healthcare provider."""

    TRANSLATION_PROMPT = """System: You are a medical translator. Translate the text preserving safety warnings exactly.

Original ({source_lang}): {original_text}
Target Language: {target_lang}

Translation:"""

    SAFETY_DISCLAIMER = """\n\n⚠️ **IMPORTANT**: This information is for educational purposes only and does not constitute medical advice. Always consult your doctor or pharmacist before changing your medication regimen."""

    @staticmethod
    def format_explanation_prompt(interaction_data: dict) -> str:
        """
        Format the explanation prompt using the interaction verification data.
        OPTIMIZED: Shorter prompt for faster generation.
        """
        # Extract drugs from the pair tuple or string
        drugs = interaction_data.get('drug_pair')
        if isinstance(drugs, tuple) or isinstance(drugs, list):
            drug_a, drug_b = drugs[0], drugs[1]
        else:
            # Fallback if just a string key
            parts = str(drugs).split('+')
            drug_a = parts[0] if len(parts) > 0 else "Unknown"
            drug_b = parts[1] if len(parts) > 1 else "Unknown"

        return PromptTemplates.EXPLANATION_PROMPT.format(
            drug_a=drug_a.title(),
            drug_b=drug_b.title(),
            risk_level=interaction_data.get('risk_level', 'Unknown').upper(),
            reason=interaction_data.get('mechanism', 'Unknown mechanism'),
            effect=interaction_data.get('clinical_effect', 'Unknown effect')
        )

    @staticmethod
    def get_safety_disclaimer() -> str:
        return PromptTemplates.SAFETY_DISCLAIMER

    @staticmethod
    def format_translation_prompt(original_text: str, target_language: str) -> str:
        """
        Format the translation prompt.
        
        Args:
            original_text (str): The text to translate
            target_language (str): The target language (e.g., "Spanish", "Hindi")
        """
        return PromptTemplates.TRANSLATION_PROMPT.format(
            source_lang="English",
            original_text=original_text,
            target_lang=target_language
        )
