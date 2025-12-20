"""
Simple server runner to diagnose startup issues
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    try:
        print("Starting Flask application...")
        from app import app
        print("App imported successfully!")
        print("Starting server on http://127.0.0.1:5000")
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"\nError starting server: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
