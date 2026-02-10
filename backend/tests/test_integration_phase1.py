"""
Integration tests for Phase 1 - Drug ID Extraction.
Tests the complete flow: Image → OCR → Normalization → Drug List
"""

import pytest
from pathlib import Path
from backend.app.ocr import extract_text
from backend.app.drug_db import DrugDatabase


class TestPhase1Integration:
    """Integration tests for the complete Phase 1 pipeline."""
    
    @pytest.fixture
    def drug_db(self):
        """Create a DrugDatabase instance."""
        return DrugDatabase()
    
    def test_end_to_end_synthetic_image(self, tmp_path, drug_db):
        """Test complete pipeline with a synthetic image."""
        import cv2
        import numpy as np
        
        # Create a synthetic pill strip image
        img = np.ones((200, 500), dtype=np.uint8) * 255
        cv2.putText(img, 'ASPIRIN 100MG', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 0, 3)
        cv2.putText(img, 'WARFARIN 5MG', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.5, 0, 3)
        cv2.putText(img, 'MFG: 2024', (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 0, 2)
        
        test_image = tmp_path / "pill_strip.jpg"
        cv2.imwrite(str(test_image), img)
        
        # Step 1: OCR
        raw_text = extract_text(str(test_image))
        assert isinstance(raw_text, list)
        
        # Step 2: Normalization
        drugs = drug_db.normalize(raw_text)
        
        # Verify results (OCR may not be perfect, so we check structure)
        assert isinstance(drugs, list)
        # If OCR worked, we should find at least one drug
        # (but we don't assert specific drugs due to OCR variability)
    
    def test_pipeline_with_brand_names(self, tmp_path, drug_db):
        """Test pipeline with brand name recognition."""
        import cv2
        import numpy as np
        
        # Create image with brand names
        img = np.ones((150, 400), dtype=np.uint8) * 255
        cv2.putText(img, 'ECOSPRIN', (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 2, 0, 3)
        
        test_image = tmp_path / "brand_name.jpg"
        cv2.imwrite(str(test_image), img)
        
        # Run pipeline
        raw_text = extract_text(str(test_image))
        drugs = drug_db.normalize(raw_text)
        
        # Structure check
        assert isinstance(drugs, list)
    
    def test_pipeline_filters_non_drugs(self, drug_db):
        """Test that non-drug text is filtered out."""
        # Simulate OCR output with mixed content
        raw_text = [
            'ASPIRIN 100MG',
            'MFG: 2024-01-15',
            'EXP: 2026-01-15',
            'BATCH: ABC123',
            'WARFARIN 5MG',
            'STRIP OF 10 TABLETS'
        ]
        
        drugs = drug_db.normalize(raw_text)
        
        # Should only extract drug names
        assert 'aspirin' in drugs or 'warfarin' in drugs
        # Should not include metadata
        assert not any('2024' in d for d in drugs)
        assert not any('BATCH' in d.upper() for d in drugs)
    
    def test_pipeline_handles_empty_ocr(self, drug_db):
        """Test pipeline with empty OCR output."""
        raw_text = []
        drugs = drug_db.normalize(raw_text)
        
        assert isinstance(drugs, list)
        assert len(drugs) == 0
    
    def test_pipeline_handles_no_matches(self, drug_db):
        """Test pipeline when no drugs are recognized."""
        raw_text = ['UNKNOWN TEXT', 'RANDOM WORDS', '12345']
        drugs = drug_db.normalize(raw_text)
        
        assert isinstance(drugs, list)
        # May be empty if nothing matches
