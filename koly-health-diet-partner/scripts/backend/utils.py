import re
from typing import Dict, List, Optional
from datetime import datetime

def validate_input(data: Dict) -> Optional[str]:
    """Enhanced input validation for comprehensive recommendations"""
    if not data:
        return "No data provided"
    
    symptoms = data.get('symptoms', '').strip()
    if not symptoms:
        return "Symptoms are required for comprehensive analysis"
    
    if len(symptoms) < 10:
        return "Please provide more detailed symptoms (at least 10 characters) for accurate analysis"
    
    if len(symptoms) > 3000:
        return "Symptoms description is too long (maximum 3000 characters)"
    
    allergies = data.get('allergies', [])
    if not isinstance(allergies, list):
        return "Allergies must be provided as a list"
    
    # Validate each allergy
    for allergy in allergies:
        if not isinstance(allergy, str):
            return "Each allergy must be a string"
        if len(allergy.strip()) == 0:
            return "Empty allergy entries are not allowed"
        if len(allergy) > 50:
            return "Allergy names must be less than 50 characters"
    
    return None

def format_comprehensive_response(
    recommendation: str,
    sources: List[Dict],
    allergy_masked: List[str],
    nutritional_highlights: List[str],
    safety_score: int,
    confidence: int,
    use_case: str,
    meal_plan: Dict,
    specific_recommendations: Dict,
    supplement_suggestions: List[str],
    lifestyle_recommendations: List[str]
) -> Dict:
    """Format comprehensive API response with all components"""
    return {
        'recommendation': recommendation,
        'sources': sources,
        'allergy_masked': allergy_masked,
        'nutritional_highlights': nutritional_highlights,
        'safety_score': safety_score,
        'confidence': confidence,
        'use_case': use_case,
        'meal_plan': meal_plan,
        'specific_recommendations': specific_recommendations,
        'supplement_suggestions': supplement_suggestions,
        'lifestyle_recommendations': lifestyle_recommendations,
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'analysis_type': 'comprehensive_multi_source'
    }

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\-.,!?():/#]', '', text)
    
    return text.strip()

def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text for better matching"""
    # Simple keyword extraction
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Filter out common stop words
    stop_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 
        'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 
        'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 
        'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use', 'with', 'have',
        'this', 'will', 'your', 'from', 'they', 'know', 'want', 'been', 'good',
        'much', 'some', 'time', 'very', 'when', 'come', 'here', 'just', 'like',
        'long', 'make', 'many', 'over', 'such', 'take', 'than', 'them', 'well',
        'were'
    }
    
    keywords = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Return unique keywords
    return list(set(keywords))

def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate simple text similarity based on common words"""
    words1 = set(extract_keywords(text1))
    words2 = set(extract_keywords(text2))
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def format_meal_plan_text(meal_plan: Dict) -> str:
    """Format meal plan dictionary into readable text"""
    formatted_text = "## 🍽️ Personalized Meal Plan\n\n"
    
    meal_emojis = {
        'breakfast': '🌅',
        'lunch': '☀️',
        'dinner': '🌙',
        'snacks': '🍎'
    }
    
    for meal_type, items in meal_plan.items():
        emoji = meal_emojis.get(meal_type, '🍽️')
        formatted_text += f"### {emoji} {meal_type.title()}\n"
        for item in items:
            formatted_text += f"• {item}\n"
        formatted_text += "\n"
    
    return formatted_text

def validate_meal_plan(meal_plan: Dict) -> bool:
    """Validate meal plan structure"""
    required_meals = ['breakfast', 'lunch', 'dinner', 'snacks']
    
    if not isinstance(meal_plan, dict):
        return False
    
    for meal in required_meals:
        if meal not in meal_plan:
            return False
        if not isinstance(meal_plan[meal], list):
            return False
        if len(meal_plan[meal]) == 0:
            return False
    
    return True

def sanitize_user_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\';\\]', '', text)
    
    # Limit length
    sanitized = sanitized[:5000]
    
    # Remove excessive whitespace
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    return sanitized

def generate_recommendation_id() -> str:
    """Generate unique ID for recommendation tracking"""
    import uuid
    return str(uuid.uuid4())[:8]

def log_recommendation_request(symptoms: str, allergies: List[str], user_profile: Dict = None):
    """Log recommendation request for analytics (anonymized)"""
    import logging
    logger = logging.getLogger(__name__)
    
    # Create anonymized log entry
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'symptoms_length': len(symptoms),
        'allergies_count': len(allergies),
        'has_user_profile': bool(user_profile),
        'request_id': generate_recommendation_id()
    }
    
    logger.info(f"Recommendation request: {log_data}")
    return log_data['request_id']
