"""
Prompt Engineering for MedGemma.
Safety-first prompts for explanation generation.

PHASE 3 - Enhanced for Phase 6: Detailed, Structured, Point-wise Explanations
"""


class PromptTemplates:
    """
    Prompt templates for MedGemma interaction.
    
    CRITICAL RULES:
    - Safety-framed language
    - No medical advice
    - Use grounding info only
    - No diagnosis or prescription
    - Generate DETAILED, LENGTHY, STRUCTURED explanations
    - Minimum 5-7 points per section
    - Each point should be comprehensive (2-3 sentences)
    """
    
    # System Prompt to set the behavior
    SYSTEM_PROMPT = """You are MedGemma, a helpful and safety-focused medical AI assistant.
Your goal is to explain verified drug interactions with COMPREHENSIVE, DETAILED, STRUCTURED information.

STRICT RULES:
1. ONLY use the verified facts provided in the prompt.
2. DO NOT hallucinate or makeup new interactions.
3. DO NOT give medical advice or prescribe medication.
4. IF unknown/insufficient data, state that clearly.
5. ALWAYS advise consulting a healthcare professional.

OUTPUT REQUIREMENTS:
1. Generate DETAILED, LENGTHY explanations (5-7 points per section minimum)
2. Each point should be COMPREHENSIVE (2-3 sentences with specific details)
3. Use STRUCTURED, POINT-WISE format
4. Include medical terminology with clear explanations
5. Reference physiological mechanisms and clinical evidence
6. Be thorough, educational, and evidence-based
"""

    EXPLANATION_PROMPT = """System: {system_prompt}

Task: Provide a COMPREHENSIVE, DETAILED, STRUCTURED analysis of this drug interaction.

Verified Facts:
- Drug A: {drug_a}
- Drug B: {drug_b}
- Risk Level: {risk_level}
- Mechanism: {reason}
- Clinical Effect: {effect}
- Recommendation: {recommendation}

REQUIRED OUTPUT STRUCTURE (Each section MUST have 5-7 detailed points):

### MECHANISM OF INTERACTION:
Provide 5-7 detailed points explaining:
- Pharmacodynamic mechanisms (how drugs affect the body)
- Pharmacokinetic pathways (absorption, distribution, metabolism, excretion)
- Molecular and cellular interactions
- Enzyme interactions (CYP450, P-glycoprotein, etc.)
- Receptor-level effects
- Time course of interaction development
Each point MUST be 2-3 sentences with specific physiological details.

### CLINICAL MANIFESTATIONS:
Provide 5-7 detailed points describing:
- Specific symptoms and clinical signs
- Severity levels and onset timeline
- Affected organ systems
- Observable laboratory findings
- Clinical presentation variations
- Frequency and likelihood statistics
- Population-specific effects (elderly, children, etc.)
Each point MUST be comprehensive with clinical details.

### RISK FACTORS:
Provide 5-7 detailed points identifying:
- High-risk patient populations
- Comorbidities that increase risk
- Genetic factors (if applicable)
- Dose-dependent risk factors
- Duration-dependent considerations
- Concurrent medication risks
- Lifestyle and dietary factors
Each point MUST explain WHY it increases risk.

### MONITORING RECOMMENDATIONS:
Provide 5-7 detailed points specifying:
- Clinical monitoring parameters
- Laboratory tests and frequency
- Symptom surveillance strategies
- Vital sign monitoring protocols
- Follow-up timeline recommendations
- Emergency warning signs
- Documentation requirements
Each point MUST include specific monitoring details.

### ALTERNATIVE SUGGESTIONS:
Provide 5-7 detailed points suggesting:
- Safer medication alternatives (general classes, not specific drugs)
- Non-pharmacological approaches
- Dose adjustment considerations (general principles only)
- Administration timing modifications
- Supportive care measures
- Specialist consultation indications
- Evidence-based management preferences
Each point MUST explain the rationale.

CRITICAL CONSTRAINTS:
- DO NOT provide specific dosage numbers
- DO NOT prescribe or recommend specific drugs
- DO NOT diagnose conditions
- ALWAYS emphasize consulting healthcare professionals
- End with mandatory safety disclaimer"""

    TRANSLATION_PROMPT = """System: You are a medical translator. Translate the text preserving safety warnings exactly.

Original ({source_lang}): {original_text}
Target Language: {target_lang}

Translation:"""

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
