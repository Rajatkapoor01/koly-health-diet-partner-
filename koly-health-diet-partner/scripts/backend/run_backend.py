#!/usr/bin/env python3
"""
KOYL AI Backend Runner
This script initializes and runs the Flask backend server
"""

import os
import sys
import logging
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def setup_environment():
    """Set up environment variables"""
    # Set default values if not provided
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('PORT', '5000')
    
    logger.info("Environment setup complete")

def check_dependencies():
    """Check if all required dependencies are available"""
    required_packages = [
        'flask', 'torch', 'transformers', 'sentence_transformers', 
        'faiss', 'numpy', 'sklearn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages: {missing_packages}")
        logger.error("Please install requirements: pip install -r requirements.txt")
        return False
    
    logger.info("All dependencies are available")
    return True

def main():
    """Main function to run the backend"""
    logger.info("Starting KOYL AI Backend...")
    
    # Setup environment
    setup_environment()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Import and run the Flask app
        from app import app
        
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_ENV') == 'development'
        
        logger.info(f"Starting server on port {port}")
        logger.info(f"Debug mode: {debug}")
        
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            threaded=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start backend: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
