"""
AI Inference Module (Mock Implementation for Local Testing)
Enhanced for Phase 6: Detailed, Structured, Point-wise Explanations

This module provides:
1. Mock inference for CPU testing (Phase 5)
2. Real MedGemma integration framework (Phase 6 on Kaggle)
3. Structured output generation with detailed, point-wise explanations
"""

from typing import List, Dict
from backend.app.prompts import PromptTemplates


class AIInference:
    """
    Mock AI inference for local testing.
    Generates detailed, structured, point-wise explanations matching MedGemma output format.
    
    In production (Kaggle), use RealMedGemmaInference class with GPU.
    """
    
    @staticmethod
    def generate_explanation(interaction_data: Dict) -> Dict:
        """
        Generate a detailed, structured explanation for a drug interaction.
        
        Enhanced for Phase 6:
        - Returns structured dict with detailed sections
        - Each section has 5-7 comprehensive points
        - Points are 2-3 sentences with specific details
        - Matches frontend ResultsDisplay expected format
        
        Args:
            interaction_data (dict): Interaction details from InteractionChecker
        
        Returns:
            dict: Structured explanation with detailed, point-wise analysis
        """
        drug_pair = interaction_data.get('drug_pair', ['Unknown', 'Unknown'])
        risk_level = interaction_data.get('risk_level', 'unknown')
        mechanism = interaction_data.get('mechanism', 'Unknown mechanism')
        clinical_effect = interaction_data.get('clinical_effect', 'Unknown effect')
        
        drug1, drug2 = drug_pair[0].title(), drug_pair[1].title()
        
        # Generate detailed, structured explanation matching frontend format
        explanation = {
            "mechanism_of_interaction": [
                f"Point 1: {drug1} acts on specific physiological pathways that can be significantly altered when {drug2} is present in the system. {drug1} primarily works by modulating certain receptors or enzymes in the body, which creates a baseline effect on organ function. When {drug2} is introduced, it can either enhance or inhibit these pathways, leading to amplified or reduced therapeutic effects.",
                
                f"Point 2: The pharmacokinetic interaction involves how these drugs are processed through the body's metabolic systems. {drug1} may be metabolized by liver enzymes (such as CYP450 family enzymes), and {drug2} can either inhibit or induce these same enzymes, altering blood levels. {mechanism}",
                
                f"Point 3: At the cellular level, both {drug1} and {drug2} may compete for the same binding sites on proteins, receptors, or transport molecules. This competitive binding can displace one drug from its target, altering its concentration at the site of action. The magnitude of this effect depends on the relative concentrations of both drugs and their binding affinities.",
                
                f"Point 4: The interaction timeline is crucial for understanding clinical manifestations. This pharmacodynamic effect doesn't occur instantaneously but develops over time as drug concentrations reach steady state. Typically, interactions may begin within hours of co-administration but reach maximum intensity after several days of concurrent use.",
                
                f"Point 5: Distribution patterns throughout the body also play a critical role in this interaction. Both {drug1} and {drug2} distribute to various tissues and organs at different rates and concentrations. In organs where both drugs accumulate, the interaction effects are most pronounced.",
                
                f"Point 6: Excretion pathways represent another critical aspect of this interaction. If both drugs are eliminated through the same renal or hepatic pathways, competition for elimination can occur. {drug2} may interfere with the tubular secretion of {drug1} in the kidneys, leading to prolonged exposure.",
                
                f"Point 7: Genetic factors (pharmacogenomics) can modify how individuals experience this drug interaction. Variations in genes encoding metabolic enzymes, drug transporters, or drug targets can make some patients more susceptible to interactions."
            ],
            
            "clinical_manifestations": [
                f"Point 1: The primary clinical manifestation of the {drug1}-{drug2} interaction is {clinical_effect.lower()}. Patients typically first notice subtle changes in how they feel, which may include unusual fatigue, changes in alertness, or mild symptoms that progressively worsen if the interaction continues.",
                
                f"Point 2: Cardiovascular manifestations may occur in patients experiencing this interaction. Changes in heart rate (either tachycardia or bradycardia), blood pressure fluctuations, or irregular heart rhythms can develop. Patients might experience palpitations, chest discomfort, or dizziness upon standing.",
                
                f"Point 3: Gastrointestinal symptoms frequently emerge as part of this interaction profile. Patients may experience nausea, vomiting, abdominal pain, or changes in bowel habits. These symptoms can range from mild discomfort to severe distress that interferes with eating and hydration.",
                
                f"Point 4: Neurological effects represent a significant concern with this drug combination. Patients may experience alterations in mental status including confusion, difficulty concentrating, memory problems, or changes in mood and behavior. Some individuals develop headaches, tremors, or changes in coordination.",
                
                f"Point 5: Laboratory abnormalities often provide objective evidence of the interaction before severe symptoms develop. Blood tests may reveal changes in liver enzymes, kidney function markers, electrolyte levels, or blood cell counts.",
                
                f"Point 6: The severity and pattern of symptoms can vary significantly among different patient populations. Elderly patients often experience more pronounced and dangerous effects due to age-related changes in drug metabolism and organ function.",
                
                f"Point 7: Duration and reversibility of clinical effects depend on multiple factors including drug half-lives, patient's metabolic capacity, and how quickly the interaction is recognized and managed."
            ],
            
            "risk_factors": [
                "Point 1: Advanced age (typically 65 years and older) significantly increases the risk of serious adverse effects from this drug interaction. Elderly patients experience age-related declines in kidney and liver function, which slows drug elimination and increases the duration of drug exposure.",
                
                "Point 2: Pre-existing kidney disease or renal impairment substantially elevates interaction risk because many drugs are eliminated through the kidneys. Reduced kidney function leads to drug accumulation, higher blood levels, and prolonged exposure to both medications.",
                
                "Point 3: Liver disease or hepatic impairment creates major risk because the liver is the primary site of drug metabolism. Conditions like cirrhosis, hepatitis, fatty liver disease, or even alcohol-related liver damage impair the liver's ability to metabolize drugs properly.",
                
                "Point 4: Cardiovascular disease, including heart failure, coronary artery disease, or arrhythmias, represents a critical risk factor for this interaction. Pre-existing heart conditions reduce the body's ability to tolerate the hemodynamic effects of the drug interaction.",
                
                "Point 5: Genetic polymorphisms in drug-metabolizing enzymes (pharmacogenomic factors) create wide variability in individual risk profiles. Some people are 'poor metabolizers' due to genetic variations in CYP450 enzymes, leading to higher drug levels and increased interaction risk.",
                
                "Point 6: Concurrent use of other medications, particularly those affecting the same metabolic pathways, dramatically amplifies interaction risk. Patients taking multiple drugs metabolized by CYP450 enzymes face compounded effects as these drugs compete for metabolism.",
                
                "Point 7: Lifestyle and dietary factors can modulate interaction risk in important ways. Diet composition affects drug absorption and metabolism - high-fat meals, fiber intake, and protein levels can all influence drug pharmacokinetics."
            ],
            
            "monitoring_recommendations": [
                "Point 1: Regular clinical assessment should occur at baseline before starting the drug combination, then at frequent intervals (typically weekly for the first month, then monthly). Healthcare providers should document vital signs including blood pressure, heart rate, respiratory rate, and temperature at each visit.",
                
                "Point 2: Laboratory monitoring forms the cornerstone of detecting subclinical interaction effects. Complete blood count (CBC) should be checked regularly to detect blood-related complications. Comprehensive metabolic panel including liver enzymes, kidney function, and electrolytes should be monitored.",
                
                "Point 3: Symptom surveillance requires active patient engagement and education. Patients should be instructed to keep a symptom diary documenting any new or worsening symptoms including timing, severity, and duration.",
                
                "Point 4: Cardiovascular monitoring is essential given the potential for hemodynamic effects. Home blood pressure monitoring should be performed daily at consistent times, with results documented and reported at visits.",
                
                "Point 5: Follow-up schedule should be clearly defined with specific timepoints for reassessment. Initial follow-up within 1-2 weeks after starting the combination helps catch early problems, with subsequent visits at 1 month, 3 months, 6 months, and then annually if stable.",
                
                "Point 6: Emergency warning signs must be clearly communicated to patients and caregivers both verbally and in writing. Severe symptoms requiring immediate emergency department evaluation include: severe chest pain, difficulty breathing, sudden severe headache or confusion, loss of consciousness, or signs of bleeding.",
                
                "Point 7: Documentation requirements ensure continuity of care and legal protection. All monitoring activities, results, and clinical decisions should be thoroughly documented in the medical record using structured templates or flowsheets."
            ],
            
            "alternative_suggestions": [
                f"Point 1: Alternative medication classes may provide similar therapeutic benefits with lower interaction risk. Healthcare providers should review the therapeutic indication for both {drug1} and {drug2} and consider whether medications from different pharmacological classes could be substituted.",
                
                f"Point 2: Non-pharmacological interventions should be explored as complementary or alternative approaches to medication management. Lifestyle modifications including dietary changes, exercise programs, stress reduction techniques, and sleep hygiene can sometimes reduce medication needs.",
                
                f"Point 3: Dose adjustment strategies may allow continued use of both medications with reduced interaction risk, though this must be done carefully under close medical supervision. Using the lowest effective doses of each medication minimizes drug exposure and interaction severity.",
                
                f"Point 4: Administration timing modifications can sometimes mitigate interaction effects without changing medications. Taking drugs at different times of day (separating doses by several hours) may reduce direct pharmacokinetic interactions.",
                
                f"Point 5: Supportive care measures can help manage interaction effects if continuing both medications is deemed necessary. Gastroprotective agents may help if GI side effects are problematic. Ensuring adequate hydration supports kidney function and drug elimination.",
                
                f"Point 6: Specialist consultation provides expert guidance for complex interaction management. Clinical pharmacists with expertise in drug interactions can review the complete medication regimen and suggest alternatives. Specialists in the relevant disease area may have experience with alternative treatment strategies.",
                
                f"Point 7: Evidence-based management preferences should guide treatment decisions based on current clinical guidelines and research. Professional society guidelines often provide algorithmic approaches to managing drug interactions with specific quality of evidence ratings."
            ]
        }
        
        return explanation

    @staticmethod
    def translate_explanation(text: str, target_lang: str) -> str:
        """
        Translate the text (Mock).
        """
        return f"[MOCK TRANSLATION to {target_lang}]: {text[:50]}..."


# Real TxGemma Integration (for Kaggle with GPU)
class RealMedGemmaInference:
    """
    TxGemma 2B Predict model integration using text-generation pipeline.
    
    Model: google/txgemma-2b-predict
    - Text-to-text for healthcare prediction/explanation tasks
    - Optimized for Tesla T4 GPU
    """
    
    def __init__(self):
        self.pipe = None
        self.device = None
        self._is_warmed_up = False
        self.model_name = "google/txgemma-2b-predict"
    
    def load_model(self, model_name: str = None, hf_token: str = None):
        """
        Load TxGemma using text-generation pipeline.
        """
        try:
            print(f"   📥 Importing PyTorch and Transformers...")
            import torch
            import os
            from transformers import pipeline
            
            if model_name:
                self.model_name = model_name
            
            # ===== CUDA OPTIMIZATIONS FOR T4 =====
            if torch.cuda.is_available():
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True
                torch.backends.cudnn.benchmark = True
                torch.cuda.empty_cache()
                print(f"   ⚡ CUDA optimizations enabled")
            
            # Get HuggingFace token
            token = hf_token
            if not token:
                token = os.environ.get('HF_TOKEN') or os.environ.get('HUGGING_FACE_HUB_TOKEN')
            
            if not token:
                try:
                    from kaggle_secrets import UserSecretsClient
                    user_secrets = UserSecretsClient()
                    token = user_secrets.get_secret("HF_TOKEN")
                    print(f"   🔑 Using HuggingFace token from Kaggle Secrets")
                except:
                    pass
            
            if not token:
                print("   ℹ️  HF_TOKEN not found; trying public/auth-cached model access")
            
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            if self.device == "cuda":
                gpu_name = torch.cuda.get_device_name(0)
                gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1024**3
                print(f"   🎮 GPU: {gpu_name} ({gpu_mem:.1f} GB)")
            
            print(f"   📦 Loading TxGemma: {self.model_name}")
            print(f"   ⏳ Downloading model - please wait...")

            self.pipe = pipeline(
                "text-generation",
                model=self.model_name,
                token=token if token else None,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
            )
            
            print(f"   ✅ TxGemma loaded successfully!")
            print(f"   💾 Model: {self.model_name}")
            print(f"   🎮 Device: {self.device}")
            
            if self.device == "cuda":
                allocated = torch.cuda.memory_allocated() / 1024**3
                print(f"   📊 GPU Memory: {allocated:.1f}GB allocated")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to load model: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def warmup(self):
        """Warm up the model with a simple query."""
        if self.pipe is None or self._is_warmed_up:
            return
            
        print("   🔥 Warming up model...")
        try:
            _ = self.pipe(
                "Summarize: warfarin and aspirin interaction risk in one line.",
                max_new_tokens=24,
                do_sample=False,
                return_full_text=False,
            )
            self._is_warmed_up = True
            print("   ✅ Model warmup complete!")
        except Exception as e:
            print(f"   ⚠️  Warmup failed: {e}")
    
    def generate_explanation(self, interaction_data: Dict, prompt: str) -> Dict:
        """
        Generate drug interaction explanation using TxGemma.
        """
        if self.pipe is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        import time
        
        start_time = time.time()
        
        try:
            print(f"   🧠 Generating explanation with TxGemma...")
            print(f"   📝 Input prompt: {len(prompt)} chars")

            outputs = self.pipe(
                prompt,
                max_new_tokens=320,
                do_sample=False,
                return_full_text=False,
            )

            generated_text = ""
            if isinstance(outputs, list) and len(outputs) > 0:
                first = outputs[0]
                if isinstance(first, dict):
                    if "generated_text" in first and isinstance(first["generated_text"], str):
                        generated_text = first["generated_text"].strip()
                    elif "text" in first and isinstance(first["text"], str):
                        generated_text = first["text"].strip()
            
            inference_time = time.time() - start_time
            print(f"   ⚡ MedGemma inference: {inference_time:.1f}s")

            if not generated_text:
                print("   ⚠️  Extraction empty; inspecting raw output object")
                print(f"   📝 Raw output object preview: {str(outputs)[:500]}")

                outputs_retry = self.pipe(
                    f"{prompt}\n\nRespond with concise bullet points under: MECHANISM, SYMPTOMS, RISK FACTORS, MONITORING, ALTERNATIVES.",
                    max_new_tokens=256,
                    do_sample=False,
                    return_full_text=False,
                )
                if isinstance(outputs_retry, list) and len(outputs_retry) > 0 and isinstance(outputs_retry[0], dict):
                    retry_gt = outputs_retry[0].get("generated_text", "")
                    if isinstance(retry_gt, str):
                        generated_text = retry_gt.strip()
            
            # DEBUG: Show raw output
            print(f"\n{'='*60}")
            print(f"📝 RAW TXGEMMA OUTPUT:")
            print(f"{'='*60}")
            final_text = generated_text.strip()
            print(final_text[:2000] if final_text else "[EMPTY]")
            print(f"{'='*60}")
            print(f"📝 Parsing MedGemma output ({len(final_text)} chars)...\n")
            
            # Parse output into structured format
            return self._parse_output_to_structure(final_text, interaction_data)
            
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            import traceback
            traceback.print_exc()
            return AIInference.generate_explanation(interaction_data)
    
    def _parse_output_to_structure(self, text: str, interaction_data: Dict) -> Dict:
        """
        Parse MedGemma's free-text output into structured format for frontend.
        ROBUST parsing that handles various output formats.
        """
        import re
        
        drug_pair = interaction_data.get('drug_pair', ['Drug A', 'Drug B'])
        drug1 = drug_pair[0].title() if isinstance(drug_pair, (list, tuple)) else "Drug"
        drug2 = drug_pair[1].title() if isinstance(drug_pair, (list, tuple)) and len(drug_pair) > 1 else "Drug"
        
        print(f"   📝 Parsing MedGemma output ({len(text)} chars)...")
        
        # Clean the text
        text = text.strip()
        
        # Initialize result
        result = {
            "mechanism_of_interaction": [],
            "clinical_manifestations": [],
            "risk_factors": [],
            "monitoring_recommendations": [],
            "alternative_suggestions": []
        }
        
        # Try to find numbered sections (1. MECHANISM, 2. SYMPTOMS, etc.)
        section_patterns = [
            # Pattern: "1. MECHANISM:" or "1. MECHANISM\n" or "**1. MECHANISM**"
            (r'1\.?\s*(?:\*\*)?MECHANISM[:\s\*]*(.+?)(?=2\.?\s*(?:\*\*)?(?:SYMPTOMS|CLINICAL)|$)', 'mechanism_of_interaction'),
            (r'2\.?\s*(?:\*\*)?(?:SYMPTOMS|CLINICAL)[:\s\*]*(.+?)(?=3\.?\s*(?:\*\*)?RISK|$)', 'clinical_manifestations'),
            (r'3\.?\s*(?:\*\*)?RISK[:\s\*]*(.+?)(?=4\.?\s*(?:\*\*)?MONITOR|$)', 'risk_factors'),
            (r'4\.?\s*(?:\*\*)?MONITOR[:\s\*]*(.+?)(?=5\.?\s*(?:\*\*)?ALTERNATIVE|$)', 'monitoring_recommendations'),
            (r'5\.?\s*(?:\*\*)?ALTERNATIVE[:\s\*]*(.+?)(?=Consult|$)', 'alternative_suggestions'),
        ]
        
        found_sections = 0
        for pattern, key in section_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                content = match.group(1).strip()
                # Split into points
                points = self._split_to_points(content)
                if points:
                    result[key] = points
                    found_sections += 1
        
        print(f"   📝 Found {found_sections} structured sections")
        
        # If no structured sections found, try simpler approach
        if found_sections == 0:
            # Split by any headers or numbered items
            lines = text.split('\n')
            all_content = []
            
            for line in lines:
                line = line.strip()
                # Skip empty lines and very short lines
                if len(line) > 30:
                    # Remove markdown formatting
                    line = re.sub(r'\*\*|\*|#{1,3}\s*', '', line)
                    # Remove leading numbers/bullets
                    line = re.sub(r'^[\d]+[\.\)]\s*', '', line)
                    line = re.sub(r'^[-•]\s*', '', line)
                    if line:
                        all_content.append(line)
            
            print(f"   📝 Extracted {len(all_content)} content lines")
            
            # Distribute content across sections
            if all_content:
                n = len(all_content)
                # Mechanism gets first 40%
                mech_end = max(1, int(n * 0.4))
                # Clinical gets next 20%
                clin_end = mech_end + max(1, int(n * 0.2))
                # Risk gets next 15%
                risk_end = clin_end + max(1, int(n * 0.15))
                # Monitor gets next 15%
                mon_end = risk_end + max(1, int(n * 0.15))
                
                result["mechanism_of_interaction"] = all_content[:mech_end]
                result["clinical_manifestations"] = all_content[mech_end:clin_end] if mech_end < n else []
                result["risk_factors"] = all_content[clin_end:risk_end] if clin_end < n else []
                result["monitoring_recommendations"] = all_content[risk_end:mon_end] if risk_end < n else []
                result["alternative_suggestions"] = all_content[mon_end:] if mon_end < n else []
        
        # Ensure each section has content - use raw text segments as fallback
        if not result["mechanism_of_interaction"] and text:
            # Use first part of raw text
            result["mechanism_of_interaction"] = [text[:500] if len(text) > 500 else text]
        
        if not result["clinical_manifestations"]:
            result["clinical_manifestations"] = [f"The {drug1}-{drug2} interaction may lead to adverse clinical effects. Monitor for unusual symptoms and report any concerns to your healthcare provider."]
        
        if not result["risk_factors"]:
            result["risk_factors"] = [f"Patients with pre-existing conditions, elderly patients, and those on multiple medications may be at higher risk for {drug1}-{drug2} interaction effects."]
        
        if not result["monitoring_recommendations"]:
            result["monitoring_recommendations"] = ["Regular monitoring of relevant lab values and clinical symptoms is recommended. Follow up with your healthcare provider as directed."]
        
        if not result["alternative_suggestions"]:
            result["alternative_suggestions"] = ["Discuss potential alternative medications or dosing strategies with your healthcare provider if this interaction is a concern."]
        
        # Log what we parsed
        total_points = sum(len(v) for v in result.values())
        print(f"   ✅ Parsed {total_points} total points across all sections")
        
        # Add raw response for transparency
        result["_raw_response"] = text[:1500]
        
        return result
    
    def _split_to_points(self, content: str) -> list:
        """Split content into individual points/bullets."""
        import re
        
        points = []
        
        # Try splitting by numbered items, bullets, or newlines
        lines = re.split(r'\n(?=[\d•\-\*])', content)
        
        for line in lines:
            line = line.strip()
            # Clean up
            line = re.sub(r'^[\d]+[\.\)]\s*', '', line)
            line = re.sub(r'^[-•\*]\s*', '', line)
            line = re.sub(r'\*\*|\*', '', line)  # Remove markdown bold
            
            if line and len(line) > 20:
                points.append(line)
        
        # If we only got 1 big chunk, try splitting by sentences
        if len(points) <= 1 and content:
            sentences = re.split(r'(?<=[.!?])\s+', content)
            points = []
            current = ""
            for sent in sentences:
                current += sent + " "
                if len(current) > 80:
                    points.append(current.strip())
                    current = ""
            if current.strip():
                points.append(current.strip())
        
        return points[:5]  # Max 5 points per section
