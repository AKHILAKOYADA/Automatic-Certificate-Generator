"""
Vercel Serverless Function Wrapper for Flask App
This file enables Flask to run on Vercel's serverless platform.
"""
import sys
import os

# Add parent directory to path to import app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import Flask app
try:
    from app import app
except ImportError as e:
    print(f"Error importing app: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    raise

# Vercel's @vercel/python runtime automatically detects Flask app objects
# Just exporting the app is enough - Vercel will wrap it appropriately

