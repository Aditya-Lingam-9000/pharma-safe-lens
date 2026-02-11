from backend.app.safety import SafetyGuard

def debug_safety():
    print("--- Testing Safety Guard ---")
    
    # Test 1: Safe
    safe = "This combination increases bleeding risk."
    res, msg = SafetyGuard.validate_output(safe)
    print(f"Safe Text: {safe} -> {res}")
    assert res is True
    assert msg == safe
    
    # Test 2: Dangerous Dosage
    danger1 = "You should take 500mg of Aspirin."
    res, msg = SafetyGuard.validate_output(danger1)
    print(f"Danger1: {danger1} -> {res}")
    assert res is False
    assert "SAFETY ALERT" in msg
    
    # Test 3: Prescription
    danger2 = "I prescribe discontinuing Warfarin immediately."
    res, msg = SafetyGuard.validate_output(danger2)
    print(f"Danger2: {danger2} -> {res}")
    assert res is False
    assert "SAFETY ALERT" in msg

    print("\n✅ All Safety Tests Passed!")

if __name__ == "__main__":
    debug_safety()
