from typing import List, Dict
from backend.app.prompts import PromptTemplates

class AIInference:
    """
    Handles AI explanation generation.
    Supports MOCK (Local) and potentially External APIs.
    """
    
    @staticmethod
    def generate_explanation(interaction_data: Dict) -> str:
        """
        Generate an explanation for the given interaction.
        
        Args:
            interaction_data (Dict): The interaction details (risk, mechanism, etc.)
            
        Returns:
            str: The generated explanation.
        """
        # Format the prompt (ensures we use the same Phase 3 logic)
        prompt = PromptTemplates.format_explanation_prompt(interaction_data)
        
        # MOCK IMPLEMENTATION (Local CPU)
        # Returns a static response that mimics MedGemma's style.
        # This allows Frontend/Safety layer testing without GPU.
        
        mock_response = (
            "**Risk Summary:**\n"
            "This combination can increase the risk of side effects. "
            "Based on the verified mechanism, there is a potential for adverse reactions.\n\n"
            "**Mechanism:**\n"
            f"{interaction_data.get('mechanism', 'Unknown mechanism')}.\n\n"
            "**Watchouts:**\n"
            "Please monitor for any unusual symptoms.\n\n"
            "**Disclaimer:**\n"
            "This is an automated educational summary. Always consult your doctor."
        )
        
        return mock_response

    @staticmethod
    def translate_explanation(text: str, target_lang: str) -> str:
        """
        Translate the text (Mock).
        """
        return f"[MOCK TRANSLATION to {target_lang}]: {text[:50]}..."
