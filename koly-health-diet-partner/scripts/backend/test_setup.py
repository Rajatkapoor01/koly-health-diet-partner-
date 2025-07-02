#!/usr/bin/env python3
"""
KOYL AI Setup Test
Tests if the backend setup is working correctly
"""

import sys
import os
import json
from datetime import datetime

def test_imports():
    """Test if all required imports work"""
    print("🧪 Testing imports...")
    
    try:
        # Core imports
        import numpy as np
        import requests
        import flask
        print("✅ Core dependencies")
        
        # AI/ML imports
        import torch
        import transformers
        import sentence_transformers
        import faiss
        print("✅ AI/ML dependencies")
        
        # Custom modules
        sys.path.append(os.path.dirname(__file__))
        import knowledge_base
        import allergy_filter
        import utils
        print("✅ Custom modules")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🔧 Testing basic functionality...")
    
    try:
        # Test knowledge base
        from knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        print(f"✅ Knowledge base: {len(kb.documents)} documents loaded")
        
        # Test allergy filter
        from allergy_filter import AllergyFilter
        af = AllergyFilter()
        print(f"✅ Allergy filter: {len(af.allergy_mappings)} allergies supported")
        
        # Test search
        results = kb.search_documents("diabetes nutrition", max_results=3)
        print(f"✅ Search functionality: {len(results)} results")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

def test_api_functionality():
    """Test API-related functionality"""
    print("\n🌐 Testing API functionality...")
    
    try:
        from utils import validate_input, format_comprehensive_response
        
        # Test input validation
        test_data = {
            'symptoms': 'I have diabetes and high blood pressure',
            'allergies': ['dairy', 'nuts']
        }
        
        validation_result = validate_input(test_data)
        if validation_result is None:
            print("✅ Input validation")
        else:
            print(f"❌ Input validation failed: {validation_result}")
            return False
        
        # Test response formatting
        mock_response = format_comprehensive_response(
            recommendation="Test recommendation",
            sources=[],
            allergy_masked=[],
            nutritional_highlights=[],
            safety_score=95,
            confidence=85,
            use_case="Test",
            meal_plan={'breakfast': [], 'lunch': [], 'dinner': [], 'snacks': []},
            specific_recommendations={'immediate': [], 'shortTerm': [], 'longTerm': []},
            supplement_suggestions=[],
            lifestyle_recommendations=[]
        )
        
        if isinstance(mock_response, dict) and 'recommendation' in mock_response:
            print("✅ Response formatting")
        else:
            print("❌ Response formatting failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API test error: {e}")
        return False

def generate_test_report():
    """Generate a test report"""
    report = {
        'test_timestamp': datetime.now().isoformat(),
        'test_results': {},
        'system_info': {
            'python_version': sys.version,
            'platform': sys.platform,
        }
    }
    
    print("📋 Running comprehensive tests...")
    print("=" * 50)
    
    # Run tests
    report['test_results']['imports'] = test_imports()
    report['test_results']['functionality'] = test_basic_functionality()
    report['test_results']['api'] = test_api_functionality()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    all_passed = all(report['test_results'].values())
    
    for test_name, result in report['test_results'].items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name.capitalize()}: {status}")
    
    print()
    if all_passed:
        print("🎉 All tests passed! KOYL AI backend is ready to use.")
        print("\n🚀 Next steps:")
        print("   • Start backend: python run_backend.py")
        print("   • Test API: curl http://localhost:5000/health")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("   • Run: pip install -r requirements.txt")
        print("   • Check: python check_dependencies.py")
    
    # Save report
    with open('test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Test report saved to: test_report.json")
    
    return all_passed

if __name__ == '__main__':
    success = generate_test_report()
    sys.exit(0 if success else 1)
