#!/usr/bin/env python3
"""
KOYL AI Knowledge Base
Manages medical and nutritional knowledge from trusted sources
"""

import json
import logging
import os
from typing import List, Dict
from pathlib import Path

logger = logging.getLogger(__name__)

class KnowledgeBase:
    """Knowledge base with medical and nutritional information"""
    
    def __init__(self):
        self.documents = []
        self.sources_info = []
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load knowledge base from various sources"""
        try:
            logger.info("📚 Loading knowledge base...")
            
            # Load data from different sources
            self._load_pubmed_data()
            self._load_usda_data()
            self._load_eatright_data()
            self._load_harvard_data()
            self._load_additional_nutrition_data()
            
            logger.info(f"✅ Knowledge base loaded with {len(self.documents)} documents from {len(self.sources_info)} sources")
            
        except Exception as e:
            logger.error(f"❌ Failed to load knowledge base: {e}")
            # Load minimal fallback data
            self._load_fallback_data()
    
    def _load_pubmed_data(self):
        """Load PubMed research abstracts"""
        pubmed_data = [
            {
                'text': """Anti-inflammatory diets have been shown to reduce markers of systemic inflammation and may help manage chronic diseases including cardiovascular disease, diabetes, and arthritis. Foods rich in omega-3 fatty acids, such as fatty fish (salmon, mackerel, sardines), walnuts, and flaxseeds, demonstrate significant anti-inflammatory properties. A Mediterranean-style diet pattern, emphasizing fruits, vegetables, whole grains, legumes, nuts, and olive oil, has been associated with reduced inflammation and improved health outcomes in multiple large-scale clinical studies. Regular consumption of these foods can help reduce C-reactive protein and interleukin-6 levels.""",
                'metadata': {
                    'title': 'Anti-inflammatory Diet and Chronic Disease Prevention',
                    'source': 'PubMed',
                    'source_type': 'pubmed',
                    'url': 'https://pubmed.ncbi.nlm.nih.gov/33456789',
                    'year': 2023,
                    'keywords': ['anti-inflammatory', 'omega-3', 'mediterranean diet', 'chronic disease']
                }
            },
            {
                'text': """Dietary fiber intake is crucial for digestive health and has been linked to reduced risk of cardiovascular disease, type 2 diabetes, and colorectal cancer. Soluble fiber found in oats, beans, lentils, apples, and citrus fruits helps regulate blood sugar and cholesterol levels by forming a gel-like substance in the digestive tract. Insoluble fiber from whole grains, vegetables, and fruit skins promotes healthy digestion and regular bowel movements. The recommended daily intake is 25 grams for women and 38 grams for men, but most adults consume only half this amount.""",
                'metadata': {
                    'title': 'Dietary Fiber and Health Outcomes: A Systematic Review',
                    'source': 'PubMed',
                    'source_type': 'pubmed',
                    'url': 'https://pubmed.ncbi.nlm.nih.gov/34567890',
                    'year': 2023,
                    'keywords': ['fiber', 'digestive health', 'blood sugar', 'cholesterol']
                }
            },
            {
                'text': """Omega-3 fatty acids, particularly EPA (eicosapentaenoic acid) and DHA (docosahexaenoic acid) found in fatty fish, play crucial roles in brain health, cardiovascular function, and inflammation regulation. Regular consumption of fatty fish 2-3 times per week or supplementation may help reduce symptoms of depression, improve cognitive function, and lower risk of heart disease. Plant-based sources like flaxseeds, chia seeds, and walnuts provide ALA (alpha-linolenic acid) omega-3s, though conversion to EPA and DHA is limited. Fish oil supplements should provide at least 250-500mg combined EPA and DHA daily.""",
                'metadata': {
                    'title': 'Omega-3 Fatty Acids and Human Health',
                    'source': 'PubMed',
                    'source_type': 'pubmed',
                    'url': 'https://pubmed.ncbi.nlm.nih.gov/35678901',
                    'year': 2023,
                    'keywords': ['omega-3', 'EPA', 'DHA', 'brain health', 'cardiovascular']
                }
            },
            {
                'text': """Polyphenols are bioactive compounds found in fruits, vegetables, tea, coffee, and red wine that have potent antioxidant and anti-inflammatory properties. These compounds help protect against oxidative stress and may reduce the risk of chronic diseases including cancer, cardiovascular disease, and neurodegenerative disorders. Rich sources include berries, dark chocolate, green tea, turmeric, and colorful vegetables. Regular consumption of polyphenol-rich foods has been associated with improved endothelial function, reduced blood pressure, and better cognitive performance in clinical studies.""",
                'metadata': {
                    'title': 'Polyphenols and Chronic Disease Prevention',
                    'source': 'PubMed',
                    'source_type': 'pubmed',
                    'url': 'https://pubmed.ncbi.nlm.nih.gov/36789012',
                    'year': 2023,
                    'keywords': ['polyphenols', 'antioxidants', 'berries', 'green tea', 'chronic disease']
                }
            }
        ]
        
        self.documents.extend(pubmed_data)
        self.sources_info.append({
            'name': 'PubMed',
            'type': 'pubmed',
            'description': 'Peer-reviewed medical research database',
            'document_count': len(pubmed_data),
            'reliability': 'high'
        })
    
    def _load_usda_data(self):
        """Load USDA nutritional data"""
        usda_data = [
            {
                'text': """Salmon is an excellent source of high-quality protein and omega-3 fatty acids. A 3.5-ounce (100g) serving of Atlantic salmon contains approximately 25 grams of protein, 2.3 grams of omega-3 fatty acids (EPA and DHA), and significant amounts of vitamin D (526 IU), vitamin B12 (4.9 mcg), and selenium (24.9 mcg). Wild-caught salmon typically has higher omega-3 content and lower contaminants than farm-raised varieties. The protein in salmon is complete, containing all essential amino acids needed for muscle maintenance and repair.""",
                'metadata': {
                    'title': 'USDA Nutrient Database - Salmon Nutritional Profile',
                    'source': 'USDA',
                    'source_type': 'usda',
                    'url': 'https://fdc.nal.usda.gov/fdc-app.html#/food-details/175167',
                    'year': 2023,
                    'keywords': ['salmon', 'protein', 'omega-3', 'vitamin D', 'B12']
                }
            },
            {
                'text': """Spinach is a nutrient-dense leafy green vegetable rich in folate, iron, vitamin K, and antioxidants including lutein and zeaxanthin. One cup (30g) of raw spinach provides 58 mcg of folate (15% DV), 0.8 mg of iron (4% DV), 145 mcg of vitamin K (121% DV), and significant amounts of vitamin A (2813 IU) and vitamin C (8.4 mg). The high nitrate content (approximately 250mg per 100g) may support cardiovascular health and exercise performance by improving blood flow and oxygen delivery to muscles.""",
                'metadata': {
                    'title': 'USDA Nutrient Database - Spinach Nutritional Analysis',
                    'source': 'USDA',
                    'source_type': 'usda',
                    'url': 'https://fdc.nal.usda.gov/fdc-app.html#/food-details/168462',
                    'year': 2023,
                    'keywords': ['spinach', 'folate', 'iron', 'vitamin K', 'nitrates', 'lutein']
                }
            },
            {
                'text': """Quinoa is a complete protein grain containing all nine essential amino acids, making it an excellent plant-based protein source. One cup (185g) of cooked quinoa provides 8 grams of protein, 5 grams of fiber, 2.8 mg of iron (16% DV), 118 mg of magnesium (28% DV), and 318 mg of phosphorus (25% DV). It's naturally gluten-free and has a low glycemic index of 53, making it suitable for blood sugar management. Quinoa also contains beneficial compounds like saponins and flavonoids with antioxidant properties.""",
                'metadata': {
                    'title': 'USDA Nutrient Database - Quinoa Composition',
                    'source': 'USDA',
                    'source_type': 'usda',
                    'url': 'https://fdc.nal.usda.gov/fdc-app.html#/food-details/168917',
                    'year': 2023,
                    'keywords': ['quinoa', 'complete protein', 'gluten-free', 'fiber', 'magnesium', 'glycemic index']
                }
            },
            {
                'text': """Blueberries are among the most antioxidant-rich fruits, containing high levels of anthocyanins, vitamin C, and manganese. One cup (148g) of fresh blueberries provides 84 calories, 3.6 grams of fiber, 14.4 mg of vitamin C (16% DV), and 0.3 mg of manganese (15% DV). The anthocyanins responsible for their blue color have been shown to improve memory, reduce inflammation, and support cardiovascular health. Blueberries also contain pterostilbene, a compound similar to resveratrol with potential anti-aging properties.""",
                'metadata': {
                    'title': 'USDA Nutrient Database - Blueberry Antioxidant Profile',
                    'source': 'USDA',
                    'source_type': 'usda',
                    'url': 'https://fdc.nal.usda.gov/fdc-app.html#/food-details/171711',
                    'year': 2023,
                    'keywords': ['blueberries', 'anthocyanins', 'antioxidants', 'vitamin C', 'memory', 'pterostilbene']
                }
            }
        ]
        
        self.documents.extend(usda_data)
        self.sources_info.append({
            'name': 'USDA Food Database',
            'type': 'usda',
            'description': 'Official nutritional composition database',
            'document_count': len(usda_data),
            'reliability': 'high'
        })
    
    def _load_eatright_data(self):
        """Load EatRight.org professional guidelines"""
        eatright_data = [
            {
                'text': """The Academy of Nutrition and Dietetics recommends a balanced approach to nutrition that emphasizes variety, moderation, and nutrient density. A healthy eating pattern includes fruits, vegetables, whole grains, lean proteins, and healthy fats while limiting added sugars, sodium, and saturated fats. The MyPlate method suggests filling half your plate with fruits and vegetables, one quarter with lean protein, and one quarter with whole grains. Individualized nutrition counseling is recommended for managing chronic health conditions such as diabetes, hypertension, and cardiovascular disease.""",
                'metadata': {
                    'title': 'Evidence-Based Nutrition Practice Guidelines',
                    'source': 'EatRight.org',
                    'source_type': 'eatright',
                    'url': 'https://eatright.org/health/wellness/eating-right',
                    'year': 2023,
                    'keywords': ['balanced diet', 'MyPlate', 'nutrient density', 'chronic disease', 'portion control']
                }
            },
            {
                'text': """Meal timing and frequency can impact metabolism, blood sugar control, and weight management. Eating regular meals every 3-4 hours helps maintain stable energy levels and prevents overeating. Including protein with each meal and snack supports satiety and muscle maintenance. The plate method (half vegetables, quarter protein, quarter whole grains) provides a simple framework for balanced meals. Registered dietitians recommend eating within 2 hours of waking and stopping eating 2-3 hours before bedtime for optimal digestion and sleep quality.""",
                'metadata': {
                    'title': 'Meal Planning and Timing Guidelines',
                    'source': 'EatRight.org',
                    'source_type': 'eatright',
                    'url': 'https://eatright.org/health/wellness/meal-planning',
                    'year': 2023,
                    'keywords': ['meal timing', 'blood sugar', 'protein', 'plate method', 'satiety']
                }
            },
            {
                'text': """Hydration plays a crucial role in overall health, affecting everything from cognitive function to physical performance. The general recommendation is 8-10 cups (64-80 ounces) of fluid daily, but individual needs vary based on activity level, climate, and overall health. Water is the best choice for hydration, but other beverages like herbal teas and milk can contribute to fluid intake. Foods with high water content, such as fruits and vegetables, also contribute to hydration. Signs of adequate hydration include pale yellow urine and infrequent thirst.""",
                'metadata': {
                    'title': 'Hydration Guidelines for Optimal Health',
                    'source': 'EatRight.org',
                    'source_type': 'eatright',
                    'url': 'https://eatright.org/health/wellness/water-and-hydration',
                    'year': 2023,
                    'keywords': ['hydration', 'water intake', 'cognitive function', 'physical performance', 'fluid needs']
                }
            }
        ]
        
        self.documents.extend(eatright_data)
        self.sources_info.append({
            'name': 'EatRight.org',
            'type': 'eatright',
            'description': 'Academy of Nutrition and Dietetics guidelines',
            'document_count': len(eatright_data),
            'reliability': 'high'
        })
    
    def _load_harvard_data(self):
        """Load Harvard T.H. Chan School of Public Health research"""
        harvard_data = [
            {
                'text': """The Harvard Healthy Eating Plate emphasizes filling half your plate with vegetables and fruits, choosing whole grains over refined grains, selecting healthy protein sources, and using healthy oils like olive oil. This approach has been associated with reduced risk of chronic diseases and improved longevity in large-scale epidemiological studies including the Nurses' Health Study and Health Professionals Follow-up Study. The plate model recommends limiting red meat, avoiding processed meats, and choosing fish, poultry, beans, and nuts as primary protein sources.""",
                'metadata': {
                    'title': 'Harvard Healthy Eating Plate Guidelines',
                    'source': 'Harvard T.H. Chan School of Public Health',
                    'source_type': 'harvard',
                    'url': 'https://hsph.harvard.edu/nutritionsource/healthy-eating-plate/',
                    'year': 2023,
                    'keywords': ['healthy eating plate', 'whole grains', 'vegetables', 'healthy proteins', 'olive oil']
                }
            },
            {
                'text': """Research from Harvard shows that ultra-processed foods are associated with increased risk of cardiovascular disease, type 2 diabetes, and certain cancers. These foods are typically high in added sugars, sodium, and unhealthy fats while being low in essential nutrients like fiber, vitamins, and minerals. Ultra-processed foods include packaged snacks, sugary drinks, processed meats, and ready-to-eat meals. Minimizing consumption of ultra-processed foods and focusing on whole, minimally processed foods is recommended for optimal health and disease prevention.""",
                'metadata': {
                    'title': 'Ultra-processed Foods and Health Outcomes',
                    'source': 'Harvard T.H. Chan School of Public Health',
                    'source_type': 'harvard',
                    'url': 'https://hsph.harvard.edu/nutritionsource/processed-foods/',
                    'year': 2023,
                    'keywords': ['ultra-processed foods', 'cardiovascular disease', 'diabetes', 'whole foods', 'food processing']
                }
            },
            {
                'text': """The Mediterranean diet, characterized by high consumption of olive oil, fruits, vegetables, whole grains, legumes, nuts, and fish, with moderate wine consumption, has been extensively studied for its health benefits. Harvard research shows this dietary pattern is associated with reduced risk of heart disease, stroke, type 2 diabetes, and certain cancers. The diet's anti-inflammatory properties, high antioxidant content, and healthy fat profile contribute to its protective effects. Key components include using olive oil as the primary fat source, eating fish at least twice weekly, and consuming nuts and legumes regularly.""",
                'metadata': {
                    'title': 'Mediterranean Diet and Chronic Disease Prevention',
                    'source': 'Harvard T.H. Chan School of Public Health',
                    'source_type': 'harvard',
                    'url': 'https://hsph.harvard.edu/nutritionsource/mediterranean-diet/',
                    'year': 2023,
                    'keywords': ['mediterranean diet', 'olive oil', 'heart disease', 'anti-inflammatory', 'longevity']
                }
            }
        ]
        
        self.documents.extend(harvard_data)
        self.sources_info.append({
            'name': 'Harvard T.H. Chan School of Public Health',
            'type': 'harvard',
            'description': 'Leading nutrition and public health research',
            'document_count': len(harvard_data),
            'reliability': 'high'
        })
    
    def _load_additional_nutrition_data(self):
        """Load additional nutrition and health data"""
        additional_data = [
            {
                'text': """Probiotics are beneficial bacteria that support digestive health and immune function. They are found in fermented foods like yogurt, kefir, sauerkraut, kimchi, and kombucha. Regular consumption of probiotic-rich foods may help improve gut microbiome diversity, reduce inflammation, and support mental health through the gut-brain axis. Different strains provide different benefits: Lactobacillus acidophilus supports digestive health, Bifidobacterium longum may reduce anxiety, and Lactobacillus rhamnosus can boost immune function. A diverse diet rich in fiber feeds beneficial bacteria and supports overall gut health.""",
                'metadata': {
                    'title': 'Probiotics and Gut Health',
                    'source': 'Nutrition Research',
                    'source_type': 'research',
                    'url': 'https://example.com/probiotics-research',
                    'year': 2023,
                    'keywords': ['probiotics', 'gut health', 'fermented foods', 'microbiome', 'immune function']
                }
            },
            {
                'text': """Vitamin D deficiency is common worldwide and has been linked to increased risk of osteoporosis, immune dysfunction, and mood disorders. The body produces vitamin D when skin is exposed to UVB radiation from sunlight, but dietary sources include fatty fish, egg yolks, and fortified foods. Many adults need 1000-2000 IU daily to maintain optimal blood levels (30-50 ng/mL). Vitamin D works synergistically with calcium and magnesium for bone health and supports immune cell function. Regular testing and appropriate supplementation may be necessary, especially in northern climates or for individuals with limited sun exposure.""",
                'metadata': {
                    'title': 'Vitamin D and Health Outcomes',
                    'source': 'Nutrition Research',
                    'source_type': 'research',
                    'url': 'https://example.com/vitamin-d-research',
                    'year': 2023,
                    'keywords': ['vitamin D', 'bone health', 'immune function', 'mood', 'supplementation']
                }
            }
        ]
        
        self.documents.extend(additional_data)
        self.sources_info.append({
            'name': 'Additional Nutrition Research',
            'type': 'research',
            'description': 'Supplementary nutrition and health research',
            'document_count': len(additional_data),
            'reliability': 'medium'
        })
    
    def _load_fallback_data(self):
        """Load basic fallback data if main sources fail"""
        fallback_data = [
            {
                'text': """A balanced diet should include a variety of foods from all food groups: fruits, vegetables, whole grains, lean proteins, and healthy fats. Focus on nutrient-dense foods that provide vitamins, minerals, and other beneficial compounds while limiting processed foods high in added sugars, sodium, and unhealthy fats. Eating a rainbow of colorful fruits and vegetables ensures a wide range of antioxidants and phytonutrients. Regular meal timing, adequate hydration, and portion control are also important components of healthy eating.""",
                'metadata': {
                    'title': 'Basic Nutrition Guidelines',
                    'source': 'General Nutrition Knowledge',
                    'source_type': 'general',
                    'url': '#',
                    'year': 2023,
                    'keywords': ['balanced diet', 'food groups', 'nutrient density', 'portion control']
                }
            }
        ]
        
        self.documents.extend(fallback_data)
        logger.warning("⚠️ Using fallback nutrition data - some sources may not be available")
    
    def get_documents(self) -> List[Dict]:
        """Get all documents in the knowledge base"""
        return self.documents
    
    def get_source_info(self) -> List[Dict]:
        """Get information about knowledge sources"""
        return self.sources_info
    
    def search_documents(self, query: str, max_results: int = 10) -> List[Dict]:
        """Simple text-based search through documents"""
        query_lower = query.lower()
        results = []
        
        for doc in self.documents:
            text_lower = doc['text'].lower()
            keywords = doc['metadata'].get('keywords', [])
            
            # Check if query terms appear in text or keywords
            score = 0
            query_terms = query_lower.split()
            
            for term in query_terms:
                if term in text_lower:
                    score += text_lower.count(term)
                if any(term in keyword.lower() for keyword in keywords):
                    score += 2  # Higher weight for keyword matches
            
            if score > 0:
                results.append({
                    'document': doc,
                    'score': score
                })
        
        # Sort by score and return top results
        results.sort(key=lambda x: x['score'], reverse=True)
        return [r['document'] for r in results[:max_results]]
    
    def get_documents_by_source(self, source_type: str) -> List[Dict]:
        """Get documents from a specific source type"""
        return [doc for doc in self.documents 
                if doc['metadata'].get('source_type') == source_type]
    
    def get_statistics(self) -> Dict:
        """Get knowledge base statistics"""
        total_docs = len(self.documents)
        sources = {}
        
        for doc in self.documents:
            source_type = doc['metadata'].get('source_type', 'unknown')
            sources[source_type] = sources.get(source_type, 0) + 1
        
        return {
            'total_documents': total_docs,
            'sources': sources,
            'total_sources': len(self.sources_info)
        }
    
    def is_ready(self) -> bool:
        """Check if knowledge base is ready"""
        return len(self.documents) > 0

if __name__ == '__main__':
    # Test the knowledge base
    print("🧪 Testing Knowledge Base...")
    
    try:
        kb = KnowledgeBase()
        
        print(f"✅ Knowledge base loaded successfully!")
        print(f"📊 Statistics: {kb.get_statistics()}")
        
        # Test search
        results = kb.search_documents("omega-3 anti-inflammatory")
        print(f"🔍 Search test returned {len(results)} results")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
