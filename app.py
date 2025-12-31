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

try:
    # Import the Flask app
    from app import app
    
    if __name__ == '__main__':
        # Ensure output directories exist
        try:
            os.makedirs('../outputs', exist_ok=True)
            os.makedirs('../models', exist_ok=True)
            print("✓ Directories created successfully")
        except Exception as e:
            print(f"⚠ Warning creating directories: {e}")
        
        # Get port from environment variable (Render sets this)
        port = int(os.environ.get('PORT', 5000))
        
        print("🚀 Starting AI Study Pal on Render...")
        print(f"🌐 Server will run on port {port}")
        
        # Run the Flask app (production mode for Render)
        app.run(host='0.0.0.0', port=port, debug=False)
        
except Exception as e:
    print(f"❌ Error starting application: {e}")
    import traceback
    traceback.print_exc()
    
    # Create a minimal Flask app as fallback
    from flask import Flask
    fallback_app = Flask(__name__)
    
    @fallback_app.route('/')
    def hello():
        return f"<h1>AI Study Pal</h1><p>Application is starting up... Please refresh in a moment.</p><p>Error: {str(e)}</p>"
    
    @fallback_app.route('/health')
    def health():
        return {"status": "starting", "error": str(e)}
    
    port = int(os.environ.get('PORT', 5000))
    print(f"🔄 Starting fallback server on port {port}")
    fallback_app.run(host='0.0.0.0', port=port, debug=False)