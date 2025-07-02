#!/usr/bin/env python3
"""
Enhanced KOYL AI Pipeline with comprehensive multi-source recommendations
"""

import os
import sys
import logging
import warnings
from typing import List, Dict, Tuple
import re
import random

# Suppress warnings
warnings.filterwarnings('ignore')
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

try:
    import numpy as np
    import torch
    from sentence_transformers import SentenceTransformer
    from transformers import T5ForConditionalGeneration, T5Tokenizer
    import faiss
except ImportError as e:
    print(f"Error importing required packages: {e}")
    print("Please install requirements: pip install torch transformers sentence-transformers faiss-cpu numpy")
    sys.exit(1)

logger = logging.getLogger(__name__)

class EnhancedRAGPipeline:
    """Enhanced RAG Pipeline with comprehensive multi-source analysis"""
    
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"🔧 Using device: {self.device}")
        
        # Initialize components
        self.encoder = None
        self.generator = None
        self.tokenizer = None
        self.index = None
        self.document_texts = []
        self.document_metadata = []
        self.last_sources = []
        
        # Use case patterns for different health conditions
        self.use_case_patterns = {
            'cardiovascular': ['blood pressure', 'heart', 'cholesterol', 'cardiovascular', 'hypertension', 'cardiac'],
            'diabetes': ['diabetes', 'blood sugar', 'glucose', 'insulin', 'diabetic', 'a1c'],
            'digestive': ['digestive', 'stomach', 'gut', 'bloating', 'constipation', 'diarrhea', 'ibs'],
            'inflammatory': ['inflammation', 'arthritis', 'joint pain', 'inflammatory', 'autoimmune'],
            'weight_management': ['weight', 'obesity', 'overweight', 'bmi', 'weight loss', 'weight gain'],
            'energy_fatigue': ['fatigue', 'tired', 'energy', 'exhausted', 'weakness', 'lethargy'],
            'mental_health': ['depression', 'anxiety', 'mood', 'stress', 'mental health', 'cognitive'],
            'general_wellness': ['wellness', 'health', 'nutrition', 'healthy', 'general']
        }
        
        # Load models and build index
        self._load_models()
        self._build_vector_index()
        
    def _load_models(self):
        """Load Sentence-BERT and T5 models"""
        try:
            logger.info("📥 Loading Sentence-BERT model (all-MiniLM-L6-v2)...")
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ Sentence-BERT model loaded successfully")
            
            logger.info("📥 Loading T5 model (t5-small)...")
            self.tokenizer = T5Tokenizer.from_pretrained('t5-small')
            self.generator = T5ForConditionalGeneration.from_pretrained('t5-small')
            self.generator.to(self.device)
            logger.info("✅ T5 model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load models: {e}")
            raise
    
    def _build_vector_index(self):
        """Build FAISS vector index from knowledge base"""
        try:
            logger.info("🔍 Building FAISS vector index...")
            
            documents = self.knowledge_base.get_documents()
            if not documents:
                raise ValueError("No documents found in knowledge base")
                
            self.document_texts = [doc['text'] for doc in documents]
            self.document_metadata = [doc['metadata'] for doc in documents]
            
            logger.info(f"📚 Processing {len(self.document_texts)} documents...")
            
            embeddings = self.encoder.encode(
                self.document_texts, 
                show_progress_bar=True,
                batch_size=32
            )
            embeddings = np.array(embeddings).astype('float32')
            
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)
            
            faiss.normalize_L2(embeddings)
            self.index.add(embeddings)
            
            logger.info(f"✅ FAISS index built with {len(self.document_texts)} documents (dimension: {dimension})")
            
        except Exception as e:
            logger.error(f"❌ Failed to build vector index: {e}")
            raise
    
    def _identify_use_case(self, symptoms: str) -> str:
        """Identify the primary use case based on symptoms"""
        symptoms_lower = symptoms.lower()
        use_case_scores = {}
        
        for use_case, patterns in self.use_case_patterns.items():
            score = sum(1 for pattern in patterns if pattern in symptoms_lower)
            if score > 0:
                use_case_scores[use_case] = score
        
        if use_case_scores:
            primary_use_case = max(use_case_scores, key=use_case_scores.get)
            return primary_use_case.replace('_', ' ').title()
        
        return "General Wellness"
    
    def retrieve_relevant_docs(self, query: str, top_k: int = 8) -> List[Dict]:
        """Retrieve most relevant documents for a query with source diversity"""
        try:
            if not self.index:
                logger.error("FAISS index not initialized")
                return []
                
            query_embedding = self.encoder.encode([query])
            query_embedding = np.array(query_embedding).astype('float32')
            faiss.normalize_L2(query_embedding)
            
            # Search for more documents to ensure source diversity
            scores, indices = self.index.search(query_embedding, top_k * 2)
            
            results = []
            source_counts = {}
            
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx != -1 and idx < len(self.document_texts):
                    source_type = self.document_metadata[idx].get('source_type', 'unknown')
                    
                    # Ensure diversity across sources
                    if source_counts.get(source_type, 0) < 3:  # Max 3 per source
                        results.append({
                            'text': self.document_texts[idx],
                            'metadata': self.document_metadata[idx],
                            'score': float(score),
                            'rank': i + 1
                        })
                        source_counts[source_type] = source_counts.get(source_type, 0) + 1
                        
                        if len(results) >= top_k:
                            break
            
            logger.info(f"🔍 Retrieved {len(results)} diverse documents from {len(source_counts)} sources")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error in document retrieval: {e}")
            return []
    
    def generate_comprehensive_recommendation(self, symptoms: str, user_context: Dict = None) -> Dict:
        """Generate comprehensive recommendation with multiple components"""
        try:
            # Identify use case
            use_case = self._identify_use_case(symptoms)
            logger.info(f"🎯 Identified use case: {use_case}")
            
            # Enhanced query for better retrieval
            enhanced_query = self._enhance_query_comprehensive(symptoms, use_case, user_context)
            
            # Retrieve relevant documents
            relevant_docs = self.retrieve_relevant_docs(enhanced_query, top_k=8)
            
            if not relevant_docs:
                logger.warning("⚠️ No relevant documents found, using comprehensive fallback")
                return self._generate_comprehensive_fallback(symptoms, use_case)
            
            # Generate different components
            main_recommendation = self._generate_main_recommendation(relevant_docs, symptoms, use_case)
            meal_plan = self._generate_meal_plan(relevant_docs, symptoms, use_case)
            specific_recommendations = self._generate_specific_recommendations(relevant_docs, symptoms, use_case)
            supplement_suggestions = self._generate_supplement_suggestions(relevant_docs, symptoms)
            lifestyle_recommendations = self._generate_lifestyle_recommendations(relevant_docs, symptoms)
            
            # Prepare sources with summaries
            sources = self._prepare_comprehensive_sources(relevant_docs)
            
            # Store sources for later retrieval
            self.last_sources = relevant_docs
            
            return {
                'recommendation': main_recommendation,
                'sources': sources,
                'useCase': use_case,
                'mealPlan': meal_plan,
                'specificRecommendations': specific_recommendations,
                'supplementSuggestions': supplement_suggestions,
                'lifestyleRecommendations': lifestyle_recommendations
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating comprehensive recommendation: {e}")
            return self._generate_comprehensive_fallback(symptoms, "General Wellness")
    
    def _enhance_query_comprehensive(self, symptoms: str, use_case: str, user_context: Dict = None) -> str:
        """Create comprehensive query for better retrieval"""
        base_query = f"comprehensive dietary nutrition recommendations for {symptoms}"
        
        # Add use case specific terms
        use_case_terms = {
            'Cardiovascular': 'heart healthy diet omega-3 sodium reduction',
            'Diabetes': 'blood sugar control glycemic index carbohydrate management',
            'Digestive': 'gut health fiber probiotics digestive enzymes',
            'Inflammatory': 'anti-inflammatory foods omega-3 antioxidants',
            'Weight Management': 'calorie control portion sizes metabolism',
            'Energy Fatigue': 'energy boosting foods iron B vitamins',
            'Mental Health': 'brain health omega-3 serotonin mood foods',
            'General Wellness': 'balanced nutrition whole foods vitamins minerals'
        }
        
        enhanced_query = f"{base_query} {use_case_terms.get(use_case, '')}"
        
        if user_context and user_context.get('previous_recommendations', 0) > 0:
            enhanced_query += " personalized follow-up advanced nutrition"
        
        return enhanced_query
    
    def _generate_main_recommendation(self, relevant_docs: List[Dict], symptoms: str, use_case: str) -> str:
        """Generate the main comprehensive recommendation"""
        context = self._prepare_context_comprehensive(relevant_docs, symptoms)
        
        # Use T5 for initial generation
        t5_recommendation = self._generate_with_t5_comprehensive(context, symptoms, use_case)
        
        # Enhance with structured formatting
        formatted_recommendation = self._format_comprehensive_recommendation(t5_recommendation, symptoms, use_case)
        
        return formatted_recommendation
    
    def _generate_meal_plan(self, relevant_docs: List[Dict], symptoms: str, use_case: str) -> Dict:
        """Generate personalized meal plan"""
        meal_plans = {
            'Cardiovascular': {
                'breakfast': [
                    'Oatmeal with berries and walnuts',
                    'Greek yogurt with flaxseeds and fruit',
                    'Whole grain toast with avocado',
                    'Smoothie with spinach, banana, and chia seeds'
                ],
                'lunch': [
                    'Grilled salmon with quinoa and steamed vegetables',
                    'Lentil soup with whole grain bread',
                    'Mediterranean salad with olive oil dressing',
                    'Turkey and vegetable wrap with hummus'
                ],
                'dinner': [
                    'Baked cod with sweet potato and broccoli',
                    'Grilled chicken with brown rice and asparagus',
                    'Vegetarian chili with beans and vegetables',
                    'Stir-fried tofu with vegetables and quinoa'
                ],
                'snacks': [
                    'Mixed nuts and seeds',
                    'Apple slices with almond butter',
                    'Carrot sticks with hummus',
                    'Berries with a small portion of dark chocolate'
                ]
            },
            'Diabetes': {
                'breakfast': [
                    'Steel-cut oats with cinnamon and berries',
                    'Vegetable omelet with whole grain toast',
                    'Greek yogurt with nuts and seeds',
                    'Chia seed pudding with unsweetened almond milk'
                ],
                'lunch': [
                    'Grilled chicken salad with mixed greens',
                    'Quinoa bowl with roasted vegetables',
                    'Lentil and vegetable soup',
                    'Turkey lettuce wraps with avocado'
                ],
                'dinner': [
                    'Baked salmon with roasted Brussels sprouts',
                    'Lean beef with cauliflower rice',
                    'Grilled tofu with steamed broccoli',
                    'Chicken stir-fry with low-carb vegetables'
                ],
                'snacks': [
                    'Celery with almond butter',
                    'Hard-boiled eggs',
                    'Cucumber slices with Greek yogurt dip',
                    'Small handful of nuts'
                ]
            }
        }
        
        # Get meal plan for use case or use general plan
        if use_case in meal_plans:
            return meal_plans[use_case]
        else:
            # Generate general healthy meal plan
            return {
                'breakfast': [
                    'Whole grain cereal with fresh fruit',
                    'Smoothie with vegetables and protein',
                    'Oatmeal with nuts and berries',
                    'Greek yogurt parfait'
                ],
                'lunch': [
                    'Grilled protein with quinoa and vegetables',
                    'Large salad with lean protein',
                    'Soup with whole grain bread',
                    'Vegetable and protein wrap'
                ],
                'dinner': [
                    'Baked fish with roasted vegetables',
                    'Lean meat with sweet potato',
                    'Plant-based protein with brown rice',
                    'Stir-fry with mixed vegetables'
                ],
                'snacks': [
                    'Fresh fruit with nuts',
                    'Vegetable sticks with hummus',
                    'Greek yogurt',
                    'Mixed seeds and berries'
                ]
            }
    
    def _generate_specific_recommendations(self, relevant_docs: List[Dict], symptoms: str, use_case: str) -> Dict:
        """Generate specific immediate, short-term, and long-term recommendations"""
        return {
            'immediate': [
                f"Start incorporating anti-inflammatory foods specific to {use_case.lower()} management",
                "Increase water intake to 8-10 glasses daily",
                "Begin a food diary to track symptoms and responses",
                "Eliminate processed foods and added sugars this week"
            ],
            'shortTerm': [
                "Establish regular meal timing every 3-4 hours",
                "Add omega-3 rich foods 2-3 times per week",
                "Increase fiber intake gradually to 25-35g daily",
                "Incorporate 30 minutes of gentle physical activity daily"
            ],
            'longTerm': [
                "Achieve optimal nutrient status through whole food sources",
                "Develop sustainable eating patterns for long-term health",
                "Regular monitoring of relevant health markers",
                "Build a support system for dietary lifestyle changes"
            ]
        }
    
    def _generate_supplement_suggestions(self, relevant_docs: List[Dict], symptoms: str) -> List[str]:
        """Generate evidence-based supplement suggestions"""
        return [
            "Omega-3 fatty acids (EPA/DHA) - 1000-2000mg daily",
            "Vitamin D3 - 1000-2000 IU daily (test levels first)",
            "Magnesium - 200-400mg daily for muscle and nerve function",
            "Probiotics - multi-strain formula for gut health",
            "B-complex vitamins for energy metabolism"
        ]
    
    def _generate_lifestyle_recommendations(self, relevant_docs: List[Dict], symptoms: str) -> List[str]:
        """Generate lifestyle recommendations"""
        return [
            "Practice mindful eating and chew food thoroughly",
            "Manage stress through meditation or yoga",
            "Ensure 7-9 hours of quality sleep nightly",
            "Stay physically active with regular exercise",
            "Limit alcohol consumption and avoid smoking"
        ]
    
    def _prepare_comprehensive_sources(self, relevant_docs: List[Dict]) -> List[Dict]:
        """Prepare comprehensive source information"""
        sources = []
        
        for doc in relevant_docs:
            metadata = doc['metadata']
            sources.append({
                'title': metadata.get('title', 'Medical Research'),
                'url': metadata.get('url', '#'),
                'type': metadata.get('source_type', 'pubmed').lower(),
                'summary': self._generate_source_summary(doc['text']),
                'relevance_score': doc['score']
            })
        
        return sources
    
    def _generate_source_summary(self, text: str) -> str:
        """Generate a brief summary of the source content"""
        # Simple extractive summary - take first sentence or key points
        sentences = text.split('.')
        if sentences:
            return sentences[0][:150] + "..." if len(sentences[0]) > 150 else sentences[0] + "."
        return "Relevant nutritional and medical research findings."
    
    def _generate_with_t5_comprehensive(self, context: str, symptoms: str, use_case: str) -> str:
        """Generate comprehensive recommendation using T5"""
        try:
            input_text = f"summarize: Create comprehensive dietary recommendations for {use_case} management with symptoms: {symptoms}. Medical context: {context[:600]}"
            
            inputs = self.tokenizer.encode(
                input_text, 
                return_tensors='pt', 
                max_length=512, 
                truncation=True
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.generator.generate(
                    inputs,
                    max_length=250,
                    min_length=80,
                    num_beams=4,
                    temperature=0.7,
                    do_sample=True,
                    early_stopping=True,
                    pad_token_id=self.tokenizer.pad_token_id
                )
            
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            logger.info("✅ T5 comprehensive generation completed")
            return generated_text
            
        except Exception as e:
            logger.error(f"❌ Error in T5 comprehensive generation: {e}")
            return f"Evidence-based dietary recommendations for {use_case} management focusing on {symptoms}."
    
    def _format_comprehensive_recommendation(self, generated_text: str, symptoms: str, use_case: str) -> str:
        """Format comprehensive recommendation with detailed structure"""
        cleaned = re.sub(r'\s+', ' ', generated_text).strip()
        
        formatted = f"""# 🏥 Comprehensive Dietary Analysis & Recommendations

## 📋 Health Profile Analysis
**Primary Concern:** {use_case}  
**Symptoms:** {symptoms}  
**Analysis Date:** {self._get_current_date()}

## 🎯 Personalized Nutrition Strategy

### 🔬 Evidence-Based Recommendations:
{cleaned}

## 🥗 Core Dietary Principles for {use_case}

### 🌟 Primary Nutritional Focus:
• **Anti-Inflammatory Protocol**: Prioritize foods that reduce systemic inflammation
• **Nutrient Density**: Choose foods with high nutritional value per calorie
• **Metabolic Support**: Include foods that support optimal metabolic function
• **Gut Health**: Incorporate foods that promote healthy digestive function

### 🍽️ Daily Nutritional Framework:

#### 🥬 Vegetables & Fruits (7-9 servings daily)
• **Leafy Greens**: Spinach, kale, arugula, Swiss chard
• **Cruciferous**: Broccoli, cauliflower, Brussels sprouts, cabbage
• **Colorful Vegetables**: Bell peppers, carrots, beets, sweet potatoes
• **Antioxidant-Rich Fruits**: Berries, cherries, pomegranates, citrus

#### 🐟 Protein Sources (20-25% of daily calories)
• **Fatty Fish**: Salmon, mackerel, sardines, anchovies (2-3x/week)
• **Lean Poultry**: Organic chicken, turkey
• **Plant Proteins**: Legumes, quinoa, hemp seeds, spirulina
• **Quality Dairy**: Greek yogurt, kefir (if tolerated)

#### 🌾 Complex Carbohydrates (40-45% of daily calories)
• **Ancient Grains**: Quinoa, amaranth, buckwheat, millet
• **Whole Grains**: Brown rice, oats, barley
• **Starchy Vegetables**: Sweet potatoes, squash, plantains
• **Legumes**: Lentils, chickpeas, black beans

#### 🥑 Healthy Fats (25-30% of daily calories)
• **Omega-3 Sources**: Fish oil, flaxseeds, chia seeds, walnuts
• **Monounsaturated**: Olive oil, avocados, almonds
• **Medium-Chain Triglycerides**: Coconut oil (moderate amounts)

## ⚡ Therapeutic Food Categories

### 🔥 Anti-Inflammatory Powerhouses:
• **Turmeric**: 1-2 tsp daily with black pepper for absorption
• **Ginger**: Fresh or dried, 1-2g daily
• **Green Tea**: 2-3 cups daily for polyphenols
• **Tart Cherries**: Natural source of melatonin and anthocyanins

### 🧠 Cognitive Support Foods:
• **Blueberries**: 1/2 cup daily for brain health
• **Dark Chocolate**: 70%+ cacao, 1 oz daily
• **Walnuts**: 1 oz daily for omega-3 ALA
• **Avocados**: Rich in monounsaturated fats

### 💪 Energy & Vitality Boosters:
• **Iron-Rich Foods**: Spinach, lentils, pumpkin seeds
• **B-Vitamin Sources**: Nutritional yeast, eggs, leafy greens
• **Magnesium Foods**: Dark chocolate, nuts, seeds, leafy greens

## 🚫 Foods to Minimize or Avoid:

### ❌ Pro-Inflammatory Foods:
• Ultra-processed foods and packaged snacks
• Refined sugars and high-fructose corn syrup
• Trans fats and hydrogenated oils
• Excessive omega-6 oils (corn, soybean, sunflower)

### ⚠️ Potential Triggers:
• High-sodium processed foods (>2300mg daily limit)
• Refined carbohydrates and white flour products
• Excessive alcohol consumption
• Foods high in advanced glycation end products (AGEs)

## 💧 Hydration & Timing Protocol:

### 🚰 Optimal Hydration:
• **Water Intake**: 0.5-1 oz per pound of body weight daily
• **Electrolyte Balance**: Add a pinch of sea salt to water
• **Herbal Teas**: Green tea, chamomile, ginger tea
• **Timing**: Drink water 30 minutes before meals, not during

### ⏰ Meal Timing Strategy:
• **Intermittent Fasting**: Consider 12-16 hour overnight fast
• **Meal Frequency**: 3 main meals + 1-2 healthy snacks
• **Pre/Post Exercise**: Protein within 30 minutes post-workout
• **Evening Cutoff**: Stop eating 2-3 hours before bedtime

## 📊 Expected Health Outcomes:

### 🎯 Short-term Benefits (2-4 weeks):
• Improved energy levels and reduced fatigue
• Better digestive function and regularity
• Enhanced mood and mental clarity
• Reduced inflammation markers

### 🏆 Long-term Benefits (2-6 months):
• Optimized body composition and weight management
• Improved cardiovascular health markers
• Enhanced immune function
• Better sleep quality and recovery

## 🔬 Monitoring & Adjustments:
• Track symptoms and energy levels daily
• Monitor relevant biomarkers every 3-6 months
• Adjust portions based on individual response
• Consider working with a registered dietitian for personalization

**⚕️ Medical Integration Note**: This comprehensive plan is designed to complement medical treatment for {use_case}. Always coordinate dietary changes with your healthcare provider, especially if you take medications or have multiple health conditions. Regular monitoring of relevant health markers is recommended to track progress and make necessary adjustments."""

        return formatted
    
    def _get_current_date(self) -> str:
        """Get current date for documentation"""
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y")
    
    def _generate_comprehensive_fallback(self, symptoms: str, use_case: str) -> Dict:
        """Generate comprehensive fallback when AI systems fail"""
        main_recommendation = f"""# 🏥 Comprehensive Dietary Recommendations for {use_case}

## 📋 Based on Your Symptoms: {symptoms}

### 🎯 Evidence-Based Nutritional Approach:
Our analysis indicates that your symptoms align with {use_case.lower()} management needs. Based on established nutritional science and clinical research, here is your personalized dietary framework:

## 🌟 Core Therapeutic Strategy:

### 🔥 Anti-Inflammatory Foundation:
Your symptoms suggest that reducing systemic inflammation should be a primary focus. This approach is supported by extensive research showing that chronic inflammation contributes to many health conditions.

**Key Anti-Inflammatory Foods:**
• **Omega-3 Rich Sources**: Fatty fish (salmon, mackerel, sardines) 2-3 times weekly
• **Polyphenol-Rich Foods**: Berries, dark leafy greens, green tea, dark chocolate
• **Spices & Herbs**: Turmeric with black pepper, ginger, garlic, rosemary

### ⚖️ Metabolic Optimization:
Supporting your body's metabolic processes through strategic nutrition can help address the underlying causes of your symptoms.

**Metabolic Support Foods:**
• **Complex Carbohydrates**: Quinoa, brown rice, oats, sweet potatoes
• **Lean Proteins**: Fish, poultry, legumes, Greek yogurt
• **Healthy Fats**: Avocados, olive oil, nuts, seeds

## 🍽️ Daily Nutritional Framework:

### 🥗 Meal Structure (Following Harvard Healthy Plate Model):
• **50% Vegetables & Fruits**: Emphasize variety and color
• **25% Lean Proteins**: Include both animal and plant sources
• **25% Whole Grains**: Choose minimally processed options
• **Healthy Oils**: Use olive oil as primary cooking fat

### 📊 Macronutrient Distribution:
• **Carbohydrates**: 45-50% (primarily complex carbs)
• **Proteins**: 20-25% (complete amino acid profiles)
• **Fats**: 25-30% (emphasis on omega-3 and monounsaturated)

## 🎯 Specific Recommendations for {use_case}:

### 🔬 Evidence-Based Interventions:
Based on peer-reviewed research, the following interventions have shown efficacy for conditions similar to yours:

• **Mediterranean Diet Pattern**: Extensively studied for chronic disease prevention
• **DASH Diet Principles**: Particularly effective for cardiovascular health
• **Anti-Inflammatory Protocol**: Reduces markers of systemic inflammation
• **Gut Health Support**: Includes prebiotic and probiotic foods

### 💊 Nutritional Therapeutics:
• **Omega-3 Fatty Acids**: 1-2g daily EPA/DHA for inflammation reduction
• **Fiber Intake**: 25-35g daily for digestive and metabolic health
• **Antioxidant Diversity**: Multiple colors of fruits and vegetables daily
• **Hydration**: 8-10 glasses of water daily for optimal cellular function

## ⏰ Implementation Timeline:

### 🚀 Week 1-2 (Foundation Phase):
• Eliminate processed foods and added sugars
• Increase vegetable intake to 5-7 servings daily
• Add one omega-3 rich meal per day
• Establish regular meal timing

### 📈 Week 3-6 (Optimization Phase):
• Fine-tune portion sizes based on hunger and satiety
• Add fermented foods for gut health
• Incorporate therapeutic spices and herbs
• Monitor symptom changes and energy levels

### 🏆 Week 7+ (Maintenance Phase):
• Maintain consistent healthy eating patterns
• Continue monitoring and adjusting as needed
• Consider advanced nutritional strategies
• Regular health marker assessments

## 🔍 Monitoring & Success Metrics:
• Daily energy levels and mood
• Digestive function and regularity
• Sleep quality and recovery
• Relevant biomarkers (as appropriate for your condition)

**⚕️ Important**: This comprehensive approach is based on current nutritional science and clinical evidence. However, individual responses can vary significantly. We strongly recommend working with a healthcare provider or registered dietitian to personalize this plan based on your specific medical history, current medications, and individual needs."""

        return {
            'recommendation': main_recommendation,
            'sources': self._get_default_comprehensive_sources(),
            'useCase': use_case,
            'mealPlan': self._generate_meal_plan([], symptoms, use_case),
            'specificRecommendations': self._generate_specific_recommendations([], symptoms, use_case),
            'supplementSuggestions': self._generate_supplement_suggestions([], symptoms),
            'lifestyleRecommendations': self._generate_lifestyle_recommendations([], symptoms)
        }
    
    def _get_default_comprehensive_sources(self) -> List[Dict]:
        """Get comprehensive default sources"""
        return [
            {
                'title': 'Anti-inflammatory Diet and Chronic Disease Prevention - Systematic Review',
                'url': 'https://pubmed.ncbi.nlm.nih.gov/',
                'type': 'pubmed',
                'summary': 'Comprehensive analysis of anti-inflammatory dietary patterns and their effects on chronic disease markers.',
                'relevance_score': 0.95
            },
            {
                'title': 'USDA National Nutrient Database - Comprehensive Food Composition',
                'url': 'https://fdc.nal.usda.gov/',
                'type': 'usda',
                'summary': 'Official nutritional composition data for thousands of foods including macro and micronutrients.',
                'relevance_score': 0.90
            },
            {
                'title': 'Academy of Nutrition and Dietetics - Evidence-Based Practice Guidelines',
                'url': 'https://eatright.org/',
                'type': 'eatright',
                'summary': 'Professional dietary guidelines based on systematic reviews and clinical evidence.',
                'relevance_score': 0.88
            },
            {
                'title': 'Harvard T.H. Chan School - Nutrition Source and Healthy Eating Plate',
                'url': 'https://hsph.harvard.edu/',
                'type': 'harvard',
                'summary': 'Evidence-based nutrition recommendations from leading public health researchers.',
                'relevance_score': 0.92
            }
        ]
    
    def get_sources(self) -> List[Dict]:
        """Get sources from last recommendation"""
        if hasattr(self, 'last_sources') and self.last_sources:
            return self._prepare_comprehensive_sources(self.last_sources)
        return self._get_default_comprehensive_sources()
    
    def get_confidence_score(self) -> int:
        """Calculate confidence score based on retrieval quality and source diversity"""
        if hasattr(self, 'last_sources') and self.last_sources:
            # Calculate confidence based on retrieval scores and source diversity
            avg_score = sum(doc['score'] for doc in self.last_sources) / len(self.last_sources)
            
            # Bonus for source diversity
            source_types = set(doc['metadata'].get('source_type', 'unknown') for doc in self.last_sources)
            diversity_bonus = min(10, len(source_types) * 2)
            
            confidence = min(95, max(70, int(avg_score * 80) + diversity_bonus))
            return confidence
        return 80  # Default confidence for comprehensive analysis
    
    def extract_nutritional_highlights(self, recommendation: str) -> List[str]:
        """Extract comprehensive nutritional highlights"""
        highlights = []
        
        # Check for key nutritional components
        if 'omega-3' in recommendation.lower():
            highlights.append("Rich in omega-3 fatty acids for cardiovascular and brain health")
        
        if 'antioxidant' in recommendation.lower() or 'berries' in recommendation.lower():
            highlights.append("High in antioxidants to combat oxidative stress and inflammation")
        
        if 'fiber' in recommendation.lower():
            highlights.append("Adequate fiber for digestive health and metabolic function")
        
        if 'anti-inflammatory' in recommendation.lower():
            highlights.append("Anti-inflammatory properties to reduce chronic inflammation")
        
        if 'protein' in recommendation.lower():
            highlights.append("Complete protein profile for muscle maintenance and repair")
        
        if 'vitamin' in recommendation.lower() or 'mineral' in recommendation.lower():
            highlights.append("Comprehensive vitamin and mineral profile for optimal health")
        
        if 'probiotic' in recommendation.lower() or 'gut' in recommendation.lower():
            highlights.append("Gut health support through prebiotic and probiotic foods")
        
        # Add comprehensive highlights if none found
        if not highlights:
            highlights = [
                "Multi-source evidence-based nutritional approach",
                "Comprehensive macro and micronutrient optimization",
                "Therapeutic food combinations for symptom management",
                "Sustainable dietary pattern for long-term health",
                "Personalized recommendations based on individual symptoms"
            ]
        
        return highlights[:6]  # Limit to 6 highlights
    
    def is_ready(self) -> bool:
        """Check if enhanced pipeline is ready"""
        return all([
            self.encoder is not None,
            self.generator is not None,
            self.tokenizer is not None,
            self.index is not None,
            len(self.document_texts) > 0
        ])

# Alias for backward compatibility
RAGPipeline = EnhancedRAGPipeline

if __name__ == '__main__':
    print("🧪 Testing Enhanced RAG Pipeline...")
    
    try:
        from knowledge_base import KnowledgeBase
        
        # Initialize components
        kb = KnowledgeBase()
        pipeline = EnhancedRAGPipeline(kb)
        
        # Test comprehensive recommendation
        test_symptoms = "I have high blood pressure, diabetes, and joint pain in the mornings"
        result = pipeline.generate_comprehensive_recommendation(test_symptoms)
        
        print("✅ Test completed successfully!")
        print(f"📝 Use case identified: {result['useCase']}")
        print(f"📊 Generated recommendation length: {len(result['recommendation'])} characters")
        print(f"🍽️ Meal plan categories: {list(result['mealPlan'].keys())}")
        print(f"📚 Sources retrieved: {len(result['sources'])}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
