"""
Vercel Serverless Function Wrapper for Flask App
This file enables Flask to run on Vercel's serverless platform.
"""
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects a handler function that receives (req, res) or follows ASGI/WSGI
def handler(request, response):
    """Vercel serverless function handler"""
    # This will be handled by Vercel's Python runtime automatically
    # The Flask app will be served via the Python runtime adapter
    pass

# Export for Vercel's Python runtime
# Vercel's @vercel/python automatically detects Flask app objects
# and wraps them appropriately for serverless execution
__all__ = ['app']

