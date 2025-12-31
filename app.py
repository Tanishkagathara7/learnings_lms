#!/usr/bin/env python3
"""
Startup script for Render deployment.
This script runs the Flask app from the web_app directory.
"""

import sys
import os

# Change to web_app directory for proper relative imports
os.chdir('web_app')

# Add current directory to path
sys.path.insert(0, os.getcwd())

# Import the Flask app
from app import app

if __name__ == '__main__':
    # Ensure output directories exist
    os.makedirs('../outputs', exist_ok=True)
    os.makedirs('../models', exist_ok=True)
    
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    
    print("🚀 Starting AI Study Pal on Render...")
    print(f"🌐 Server will run on port {port}")
    
    # Run the Flask app (production mode for Render)
    app.run(host='0.0.0.0', port=port, debug=False)