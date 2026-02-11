from backend.app.prompts import PromptTemplates

def debug():
    # Test 1: Explanation Structure
    print("\n--- TEST explanation ---")
    data = {
        "drug_pair": ("aspirin", "warfarin"),
        "risk_level": "high",
        "mechanism": "Both affect blood clotting",
        "clinical_effect": "Increased bleeding risk",
        "recommendation": "Avoid combination"
    }
    prompt = PromptTemplates.format_explanation_prompt(data)
    print(prompt)
    
    # Assertions
    assert "Aspirin" in prompt
    assert "Warfarin" in prompt
    assert "HIGH" in prompt
    assert "You are MedGemma" in prompt
    
    # Test 2: Missing Data
    print("\n--- TEST missing data ---")
    data_bad = {"drug_pair": "aspirin+unknown"}
    prompt_bad = PromptTemplates.format_explanation_prompt(data_bad)
    print(prompt_bad)
    
    assert "Unknown" in prompt_bad
    assert "UNKNOWN" in prompt_bad
    
    # Test 3: Translation
    print("\n--- TEST translation ---")
    trans = PromptTemplates.format_translation_prompt("Hello", "Spanish")
    print(trans)
    assert "Original (English): Hello" in trans
    assert "Target Language: Spanish" in trans

if __name__ == "__main__":
    debug()
