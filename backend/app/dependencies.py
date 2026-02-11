from functools import lru_cache
from backend.app.drug_db import DrugDatabase
from backend.app.interaction_logic import InteractionChecker

@lru_cache()
def get_drug_db():
    print("Loading Drug Database...")
    return DrugDatabase()

@lru_cache()
def get_interaction_checker():
    print("Loading Interaction Checker...")
    return InteractionChecker()
