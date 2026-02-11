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
    
    # System Prompt to set the behavior
    SYSTEM_PROMPT = """You are MedGemma, a helpful and safety-focused medical AI assistant.
Your goal is to explain verified drug interactions to patients using simple, clear language.
STRICT RULES:
1. ONLY use the verified facts provided in the prompt.
2. DO NOT hallucinate or makeup new interactions.
3. DO NOT give medical advice or prescribe medication.
4. IF unknown/insufficient data, state that clearly.
5. ALWAYS advise consulting a healthcare professional.
"""

    EXPLANATION_PROMPT = """<start_of_turn>user
System: {system_prompt}

Task: Explain the following drug interaction to a patient.

Verified Facts:
- Drug A: {drug_a}
- Drug B: {drug_b}
- Risk Level: {risk_level}
- Clinical Effect: {effect}
- Recommendation: {recommendation}

Instructions:
- Summarize the risk in simple language.
- Explain clearly *why* it is dangerous.
- State what to watch out for.
- End with a mandatory disclaimer.
<end_of_turn>
<start_of_turn>model"""

    TRANSLATION_PROMPT = """<start_of_turn>user
System: You are a medical translator. Translate the text preserving safety warnings exactly.

Original ({source_lang}): {original_text}
Target Language: {target_lang}

Translation:
<end_of_turn>
<start_of_turn>model"""

    SAFETY_DISCLAIMER = """\n\n⚠️ **IMPORTANT**: This information is for educational purposes only and does not constitute medical advice. Always consult your doctor or pharmacist before changing your medication regimen."""

    @staticmethod
    def format_explanation_prompt(interaction_data: dict) -> str:
        """
        Format the explanation prompt using the interaction verification data.
        
        Args:
            interaction_data (dict): Dictionary containing interaction details
                                   (drug_pair, risk_level, mechanism, clinical_effect, recommendation)
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
            system_prompt=PromptTemplates.SYSTEM_PROMPT,
            drug_a=drug_a.title(),
            drug_b=drug_b.title(),
            risk_level=interaction_data.get('risk_level', 'Unknown').upper(),
            reason=interaction_data.get('mechanism', 'No mechanism data available.'),
            effect=interaction_data.get('clinical_effect', 'No clinical effect data available.'),
            recommendation=interaction_data.get('recommendation', 'Consult your doctor.')
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
