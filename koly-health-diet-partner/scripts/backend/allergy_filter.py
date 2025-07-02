#!/usr/bin/env python3
"""
KOYL AI Allergy Filter
Intelligent filtering system for food allergies and intolerances
"""

import re
import logging
from typing import List, Tuple, Dict, Set

logger = logging.getLogger(__name__)

class AllergyFilter:
    """Intelligent allergy filtering system"""
    
    def __init__(self):
        # Define comprehensive allergy mappings and related terms
        self.allergy_mappings = {
            'dairy': {
                'terms': ['milk', 'cheese', 'yogurt', 'butter', 'cream', 'lactose', 'casein', 'whey', 
                         'kefir', 'cottage cheese', 'sour cream', 'ice cream', 'mozzarella', 'cheddar'],
                'severity': 'high',
                'category': 'protein'
            },
            'gluten': {
                'terms': ['wheat', 'barley', 'rye', 'oats', 'bread', 'pasta', 'flour', 'cereal',
                         'crackers', 'cookies', 'cake', 'malt', 'bulgur', 'semolina', 'spelt'],
                'severity': 'high',
                'category': 'grain'
            },
            'nuts': {
                'terms': ['almonds', 'walnuts', 'pecans', 'cashews', 'hazelnuts', 'pistachios',
                         'brazil nuts', 'macadamia', 'pine nuts', 'nut butter', 'almond milk'],
                'severity': 'high',
                'category': 'tree_nut'
            },
            'peanuts': {
                'terms': ['peanut', 'groundnut', 'peanut butter', 'peanut oil'],
                'severity': 'high',
                'category': 'legume'
            },
            'shellfish': {
                'terms': ['shrimp', 'crab', 'lobster', 'oysters', 'mussels', 'clams', 'scallops',
                         'crawfish', 'prawns', 'crayfish'],
                'severity': 'high',
                'category': 'seafood'
            },
            'fish': {
                'terms': ['salmon', 'tuna', 'cod', 'mackerel', 'sardines', 'trout', 'halibut',
                         'bass', 'flounder', 'fish oil', 'anchovies'],
                'severity': 'high',
                'category': 'seafood'
            },
            'eggs': {
                'terms': ['egg', 'albumin', 'mayonnaise', 'meringue', 'custard'],
                'severity': 'medium',
                'category': 'protein'
            },
            'soy': {
                'terms': ['soybean', 'tofu', 'tempeh', 'miso', 'soy sauce', 'edamame',
                         'soy milk', 'soy protein', 'lecithin'],
                'severity': 'medium',
                'category': 'legume'
            },
            'sesame': {
                'terms': ['sesame seeds', 'tahini', 'sesame oil', 'hummus'],
                'severity': 'medium',
                'category': 'seed'
            },
            'corn': {
                'terms': ['corn', 'maize', 'cornstarch', 'corn syrup', 'popcorn', 'polenta'],
                'severity': 'low',
                'category': 'grain'
            }
        }
        
        # Alternative suggestions for filtered foods
        self.alternatives = {
            'dairy': [
                'plant-based milk alternatives (almond, oat, coconut, rice milk)',
                'nutritional yeast for cheesy flavor',
                'dairy-free yogurt alternatives',
                'coconut cream for cooking',
                'calcium-fortified plant milks'
            ],
            'gluten': [
                'quinoa, rice, and other gluten-free grains',
                'gluten-free oats (certified)',
                'buckwheat and amaranth',
                'almond flour and coconut flour',
                'gluten-free bread and pasta alternatives'
            ],
            'nuts': [
                'seeds (sunflower, pumpkin, hemp seeds)',
                'seed butters (sunflower seed butter)',
                'coconut products',
                'avocado for healthy fats'
            ],
            'peanuts': [
                'sunflower seed butter',
                'other tree nuts (if not allergic)',
                'tahini (sesame seed butter)',
                'soy nut butter (if soy is tolerated)'
            ],
            'shellfish': [
                'other fish varieties (if fish is tolerated)',
                'plant-based proteins (legumes, tofu)',
                'seaweed for ocean flavor',
                'mushrooms for umami taste'
            ],
            'fish': [
                'plant-based omega-3 sources (flaxseeds, chia seeds, walnuts)',
                'algae-based omega-3 supplements',
                'hemp seeds for healthy fats',
                'plant-based proteins'
            ],
            'eggs': [
                'flax eggs (1 tbsp ground flaxseed + 3 tbsp water)',
                'chia eggs (1 tbsp chia seeds + 3 tbsp water)',
                'commercial egg replacers',
                'applesauce or mashed banana in baking'
            ],
            'soy': [
                'other legumes (lentils, chickpeas, black beans)',
                'hemp protein powder',
                'pea protein',
                'coconut aminos instead of soy sauce'
            ],
            'sesame': [
                'other seeds and nuts (if not allergic)',
                'sunflower seed butter',
                'pumpkin seed butter'
            ],
            'corn': [
                'other whole grains (rice, quinoa, millet)',
                'arrowroot starch instead of cornstarch',
                'maple syrup instead of corn syrup'
            ]
        }
        
        logger.info(f"✅ Allergy filter initialized with {len(self.allergy_mappings)} allergy types")
    
    def filter_recommendation(self, recommendation: str, allergies: List[str]) -> Tuple[str, List[str]]:
        """Filter recommendation to remove allergy-related content"""
        if not allergies:
            return recommendation, []
        
        filtered_text = recommendation
        allergy_masked = []
        
        # Normalize allergies to lowercase
        normalized_allergies = [allergy.lower().strip() for allergy in allergies]
        
        logger.info(f"🔍 Filtering recommendation for allergies: {normalized_allergies}")
        
        for allergy in normalized_allergies:
            if allergy in self.allergy_mappings:
                # Get all related terms for this allergy
                allergy_info = self.allergy_mappings[allergy]
                related_terms = allergy_info['terms']
                
                # Find and replace mentions
                masked_items = self._mask_allergy_content(filtered_text, allergy, related_terms)
                
                if masked_items:
                    allergy_masked.extend(masked_items)
                    
                    # Replace with alternatives
                    filtered_text = self._replace_with_alternatives(filtered_text, allergy, related_terms)
            else:
                # Handle unknown allergies
                logger.warning(f"⚠️ Unknown allergy type: {allergy}")
                masked_items = self._handle_unknown_allergy(filtered_text, allergy)
                if masked_items:
                    allergy_masked.extend(masked_items)
        
        logger.info(f"✅ Filtering complete. Masked {len(allergy_masked)} items")
        return filtered_text, allergy_masked
    
    def _mask_allergy_content(self, text: str, allergy: str, related_terms: List[str]) -> List[str]:
        """Identify content that should be masked due to allergies"""
        masked_items = []
        
        for term in related_terms:
            # Case-insensitive search for the term
            pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
            matches = pattern.findall(text)
            
            if matches:
                severity = self.allergy_mappings[allergy]['severity']
                masked_items.append(f"{term.title()} recommendations [Removed - {severity.title()} Allergy Risk: {allergy}]")
        
        return list(set(masked_items))  # Remove duplicates
    
    def _replace_with_alternatives(self, text: str, allergy: str, related_terms: List[str]) -> str:
        """Replace allergenic foods with safe alternatives"""
        filtered_text = text
        
        # Get alternatives for this allergy
        alternatives = self.alternatives.get(allergy, ['suitable alternatives'])
        
        for term in related_terms:
            # Replace mentions with alternatives
            pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
            
            if pattern.search(filtered_text):
                # Choose appropriate alternative
                alternative = self._select_best_alternative(term, alternatives)
                replacement = f"[Safe Alternative to {term}: {alternative}]"
                filtered_text = pattern.sub(replacement, filtered_text)
        
        return filtered_text
    
    def _select_best_alternative(self, original_term: str, alternatives: List[str]) -> str:
        """Select the most appropriate alternative for a given term"""
        # Simple logic to match alternatives to original terms
        original_lower = original_term.lower()
        
        if 'milk' in original_lower:
            return next((alt for alt in alternatives if 'milk' in alt), alternatives[0])
        elif 'cheese' in original_lower:
            return next((alt for alt in alternatives if 'yeast' in alt or 'cheese' in alt), alternatives[0])
        elif 'butter' in original
