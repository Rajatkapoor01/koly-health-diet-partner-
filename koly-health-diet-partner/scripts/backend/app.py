#!/usr/bin/env python3
"""
Enhanced KOYL AI Flask Backend Application
Main Flask server with comprehensive RAG pipeline integration
"""

import os
import sys
import logging
import traceback
from datetime import datetime
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
except ImportError as e:
    print(f"Error importing Flask modules: {e}")
    print("Please install Flask: pip install Flask Flask-CORS")
    sys.exit(1)

# Import our custom modules
try:
    from ai_pipeline import EnhancedRAGPipeline
    from allergy_filter import AllergyFilter
    from knowledge_base import KnowledgeBase
    from utils import validate_input, format_comprehensive_response
except ImportError as e:
    print(f"Error importing custom modules: {e}")
    print("Make sure all backend files are in the same directory")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('koyl_ai.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

# Global variables for AI components
knowledge_base = None
rag_pipeline = None
allergy_filter = None

def initialize_ai_components():
    """Initialize AI components with proper error handling"""
    global knowledge_base, rag_pipeline, allergy_filter
    
    try:
        logger.info("🚀 Initializing Enhanced AI Components...")
        
        # Initialize knowledge base first
        logger.info("📚 Loading comprehensive knowledge base...")
        knowledge_base = KnowledgeBase()
        
        # Initialize allergy filter
        logger.info("🛡️ Setting up advanced allergy filter...")
        allergy_filter = AllergyFilter()
        
        # Initialize enhanced RAG pipeline
        logger.info("🧠 Initializing Enhanced RAG pipeline (this may take a few minutes on first run)...")
        rag_pipeline = EnhancedRAGPipeline(knowledge_base)
        
        logger.info("✅ All Enhanced AI components initialized successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize AI components: {e}")
        logger.error(traceback.format_exc())
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Enhanced health check endpoint"""
    try:
        components_status = {
            'knowledge_base': knowledge_base.is_ready() if knowledge_base else False,
            'allergy_filter': allergy_filter.is_ready() if allergy_filter else False,
            'rag_pipeline': rag_pipeline.is_ready() if rag_pipeline else False
        }
        
        all_ready = all(components_status.values())
        
        # Get additional stats
        stats = {}
        if knowledge_base:
            stats['knowledge_base'] = knowledge_base.get_statistics()
        
        return jsonify({
            'status': 'healthy' if all_ready else 'initializing',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'components': components_status,
            'statistics': stats,
            'message': 'Enhanced multi-source analysis ready' if all_ready else 'Components still initializing'
        }), 200 if all_ready else 503
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'status': 'error',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 500

@app.route('/recommend', methods=['POST'])
def get_comprehensive_recommendation():
    """Enhanced recommendation endpoint with comprehensive analysis"""
    try:
        # Check if components are ready
        if not all([knowledge_base, rag_pipeline, allergy_filter]):
            return jsonify({
                'error': 'Enhanced AI components are still initializing. Please wait a moment and try again.',
                'status': 'initializing'
            }), 503
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate input
        validation_error = validate_input(data)
        if validation_error:
            return jsonify({'error': validation_error}), 400
        
        symptoms = data.get('symptoms', '').strip()
        allergies = data.get('allergies', [])
        user_profile = data.get('user_profile', {})
        
        logger.info(f"🔍 Processing comprehensive recommendation request...")
        logger.info(f"📋 Symptoms: {symptoms[:100]}...")
        logger.info(f"🚫 Allergies: {allergies}")
        
        # Generate comprehensive recommendation using enhanced RAG pipeline
        comprehensive_result = rag_pipeline.generate_comprehensive_recommendation(
            symptoms=symptoms,
            user_context=user_profile
        )
        
        # Filter out allergy-related content from all components
        filtered_recommendation, allergy_masked = allergy_filter.filter_recommendation(
            recommendation=comprehensive_result['recommendation'],
            allergies=allergies
        )
        
        # Filter meal plan for allergies
        filtered_meal_plan = allergy_filter.filter_meal_plan(
            meal_plan=comprehensive_result['mealPlan'],
            allergies=allergies
        )
        
        # Calculate safety and confidence scores
        safety_score = allergy_filter.calculate_safety_score(allergies, filtered_recommendation)
        confidence_score = rag_pipeline.get_confidence_score()
        
        # Extract nutritional highlights
        nutritional_highlights = rag_pipeline.extract_nutritional_highlights(filtered_recommendation)
        
        # Format comprehensive response
        response = format_comprehensive_response(
            recommendation=filtered_recommendation,
            sources=comprehensive_result['sources'],
            allergy_masked=allergy_masked,
            nutritional_highlights=nutritional_highlights,
            safety_score=safety_score,
            confidence=confidence_score,
            use_case=comprehensive_result['useCase'],
            meal_plan=filtered_meal_plan,
            specific_recommendations=comprehensive_result['specificRecommendations'],
            supplement_suggestions=comprehensive_result['supplementSuggestions'],
            lifestyle_recommendations=comprehensive_result['lifestyleRecommendations']
        )
        
        logger.info("✅ Comprehensive recommendation generated successfully")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ Error generating comprehensive recommendation: {e}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': 'Internal server error while generating comprehensive recommendation',
            'details': str(e) if app.debug else 'Please try again later'
        }), 500

@app.route('/sources', methods=['GET'])
def get_comprehensive_sources():
    """Get comprehensive knowledge sources information"""
    try:
        if not knowledge_base:
            return jsonify({'error': 'Knowledge base not initialized'}), 503
            
        sources = knowledge_base.get_source_info()
        statistics = knowledge_base.get_statistics()
        
        return jsonify({
            'sources': sources,
            'statistics': statistics,
            'total_documents': len(knowledge_base.get_documents()),
            'source_types': ['pubmed', 'usda', 'eatright', 'harvard']
        })
    except Exception as e:
        logger.error(f"Error getting comprehensive sources: {e}")
        return jsonify({'error': 'Failed to retrieve sources'}), 500

@app.route('/status', methods=['GET'])
def get_comprehensive_status():
    """Get detailed system status with enhanced information"""
    try:
        import torch
        import faiss
        
        status = {
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'mode': 'comprehensive_analysis',
            'python_version': sys.version,
            'torch_version': torch.__version__,
            'faiss_version': faiss.__version__,
            'device': 'cuda' if torch.cuda.is_available() else 'cpu',
            'components': {
                'knowledge_base': {
                    'ready': knowledge_base.is_ready() if knowledge_base else False,
                    'documents': len(knowledge_base.documents) if knowledge_base else 0,
                    'sources': len(knowledge_base.sources_info) if knowledge_base else 0
                },
                'rag_pipeline': {
                    'ready': rag_pipeline.is_ready() if rag_pipeline else False,
                    'models_loaded': hasattr(rag_pipeline, 'encoder') if rag_pipeline else False,
                    'index_size': len(rag_pipeline.document_texts) if rag_pipeline and hasattr(rag_pipeline, 'document_texts') else 0
                },
                'allergy_filter': {
                    'ready': allergy_filter.is_ready() if allergy_filter else False,
                    'allergies_supported': len(allergy_filter.allergy_mappings) if allergy_filter else 0
                }
            },
            'capabilities': [
                'multi_source_analysis',
                'comprehensive_meal_planning',
                'allergy_safe_filtering',
                'evidence_based_recommendations',
                'timeline_based_implementation'
            ]
        }
        
        return jsonify(status)
    except Exception as e:
        logger.error(f"Status check error: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get configuration from environment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"🚀 Starting Enhanced KOYL AI Backend on {host}:{port}")
    logger.info(f"🔧 Debug mode: {debug}")
    logger.info(f"🧠 Mode: Comprehensive Multi-Source Analysis")
    
    # Initialize AI components
    if initialize_ai_components():
        logger.info("✅ Enhanced AI components ready, starting Flask server...")
        app.run(host=host, port=port, debug=debug, threaded=True)
    else:
        logger.error("❌ Failed to initialize enhanced AI components, exiting...")
        sys.exit(1)
