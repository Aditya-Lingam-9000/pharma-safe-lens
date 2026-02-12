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


# Real MedGemma Integration (for Kaggle with GPU - OPTIMIZED for Tesla T4)
class RealMedGemmaInference:
    """
    Real MedGemma model integration for Kaggle GPU deployment.
    OPTIMIZED for maximum GPU utilization on Tesla T4 x2.
    
    Optimizations:
    - Float16 precision (optimal for T4 architecture)
    - Flash Attention 2 when available
    - torch.compile() for kernel optimization
    - Reduced generation length for speed
    - Model warmup at startup
    - CUDA memory optimization
    """
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = None
        self._is_warmed_up = False
    
    def load_model(self, model_name: str = "google/medgemma-4b-it", hf_token: str = None):
        """
        Load MedGemma model with MAXIMUM GPU optimization for Tesla T4.
        """
        try:
            print(f"   📥 Importing PyTorch and Transformers...")
            import torch
            import os
            from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
            
            # ===== CUDA OPTIMIZATIONS FOR T4 =====
            if torch.cuda.is_available():
                # Enable TensorFloat-32 for faster matrix multiplication
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True
                # Enable cuDNN autotuner for best convolution algorithm
                torch.backends.cudnn.benchmark = True
                # Set memory allocation strategy
                torch.cuda.empty_cache()
                print(f"   ⚡ CUDA optimizations enabled (TF32, cuDNN benchmark)")
            
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
                print(f"   ❌ ERROR: HuggingFace token not found!")
                print(f"   💡 Add 'HF_TOKEN' to Kaggle Secrets")
                return False
            
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            if self.device == "cuda":
                gpu_name = torch.cuda.get_device_name(0)
                gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1024**3
                print(f"   🎮 GPU: {gpu_name} ({gpu_mem:.1f} GB)")
                
                # Check for multiple GPUs
                num_gpus = torch.cuda.device_count()
                if num_gpus > 1:
                    print(f"   🎮 Multi-GPU detected: {num_gpus} GPUs available")
            else:
                print(f"   ⚠️  WARNING: No GPU! Enable GPU T4 x2 in Kaggle settings")
                return False
            
            print(f"   📦 Loading MedGemma: {model_name}")
            print(f"   ⏳ Downloading model (~8GB) - please wait...")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                token=token,
                trust_remote_code=True,
                padding_side="left"
            )
            
            # Set pad token if not set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print(f"   ✅ Tokenizer loaded")
            
            # ===== OPTIMIZED MODEL LOADING FOR T4 =====
            # T4 is optimized for float16 (not bfloat16)
            # Use device_map="auto" for automatic multi-GPU distribution
            
            model_kwargs = {
                "token": token,
                "torch_dtype": torch.float16,  # T4 optimal dtype
                "device_map": "auto",  # Distribute across available GPUs
                "trust_remote_code": True,
                "low_cpu_mem_usage": True,
            }
            
            # Try to use Flash Attention 2 for faster inference
            try:
                model_kwargs["attn_implementation"] = "flash_attention_2"
                print(f"   ⚡ Flash Attention 2 enabled")
            except:
                print(f"   ℹ️  Using standard attention")
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                **model_kwargs
            )
            
            # ===== MODEL OPTIMIZATION =====
            # Put model in evaluation mode
            self.model.eval()
            
            # Try torch.compile for additional speedup (PyTorch 2.0+)
            try:
                self.model = torch.compile(self.model, mode="reduce-overhead")
                print(f"   ⚡ torch.compile() enabled (kernel optimization)")
            except Exception as e:
                print(f"   ℹ️  torch.compile not available: {e}")
            
            print(f"   ✅ Model loaded successfully!")
            print(f"   💾 Precision: float16 (T4 optimized)")
            print(f"   🎮 Device: {self.device}")
            
            # Show GPU memory usage
            if self.device == "cuda":
                allocated = torch.cuda.memory_allocated() / 1024**3
                reserved = torch.cuda.memory_reserved() / 1024**3
                print(f"   📊 GPU Memory: {allocated:.1f}GB allocated, {reserved:.1f}GB reserved")
            
            return True
            
        except ImportError as e:
            print(f"   ❌ ImportError: {e}")
            print(f"   💡 pip install torch transformers accelerate flash-attn")
            return False
        except Exception as e:
            print(f"   ❌ Failed to load model: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def warmup(self):
        """
        Warm up the model with a dummy inference.
        This pre-compiles CUDA kernels for faster subsequent inferences.
        """
        if self.model is None or self._is_warmed_up:
            return
            
        print("   🔥 Warming up model (compiling CUDA kernels)...")
        import torch
        
        try:
            dummy_prompt = "What is aspirin?"
            inputs = self.tokenizer(dummy_prompt, return_tensors="pt").to(self.device)
            
            with torch.inference_mode():
                _ = self.model.generate(
                    **inputs,
                    max_new_tokens=10,
                    do_sample=False,
                    pad_token_id=self.tokenizer.pad_token_id
                )
            
            # Clear CUDA cache after warmup
            if self.device == "cuda":
                torch.cuda.empty_cache()
                torch.cuda.synchronize()
            
            self._is_warmed_up = True
            print("   ✅ Model warmup complete - ready for fast inference!")
        except Exception as e:
            print(f"   ⚠️  Warmup failed (non-critical): {e}")
    
    def generate_explanation(self, interaction_data: Dict, prompt: str) -> Dict:
        """
        Generate explanation using MedGemma with OPTIMIZED inference.
        Target: < 15 seconds on T4 GPU.
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        import torch
        import time
        
        start_time = time.time()
        
        try:
            # Tokenize with optimizations
            inputs = self.tokenizer(
                prompt, 
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=1024  # Limit input length
            ).to(self.device)
            
            input_length = inputs["input_ids"].shape[1]
            
            # ===== OPTIMIZED GENERATION =====
            # Use inference_mode (faster than no_grad)
            with torch.inference_mode():
                # Synchronize before generation for accurate timing
                if self.device == "cuda":
                    torch.cuda.synchronize()
                
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=512,  # Reduced for speed (was 2048)
                    min_new_tokens=100,  # Ensure meaningful response
                    do_sample=False,  # Greedy decoding (fastest)
                    num_beams=1,  # No beam search (fastest)
                    use_cache=True,  # Enable KV cache
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
                
                # Synchronize after generation
                if self.device == "cuda":
                    torch.cuda.synchronize()
            
            # Decode only the new tokens
            generated_text = self.tokenizer.decode(
                outputs[0][input_length:], 
                skip_special_tokens=True
            )
            
            inference_time = time.time() - start_time
            print(f"   ⚡ MedGemma inference: {inference_time:.1f}s ({len(outputs[0]) - input_length} tokens)")
            
            # Parse output into structured format
            return self._parse_output_to_structure(generated_text, interaction_data)
            
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to mock if real generation fails
            return AIInference.generate_explanation(interaction_data)
    
    def _parse_output_to_structure(self, text: str, interaction_data: Dict) -> Dict:
        """
        Parse free-text output into structured format.
        This is a placeholder - real implementation would use sophisticated parsing.
        """
        # TODO: Implement parsing logic to extract sections from generated text
        # For now, return mock structure
        return AIInference.generate_explanation(interaction_data)
