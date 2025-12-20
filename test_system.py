"""
Test Script - Quick test of Resume Analyzer components
Run this to verify your setup is working correctly
"""

import os
import sys

def test_imports():
    """Test if all required packages are installed"""
    print("\n" + "="*70)
    print("TEST 1: Checking Dependencies")
    print("="*70)
    
    required_packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('sklearn', 'scikit-learn'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('PyPDF2', 'PyPDF2'),
        ('docx', 'python-docx'),
        ('dotenv', 'python-dotenv'),
        ('openpyxl', 'openpyxl'),
    ]
    
    missing = []
    for module, package in required_packages:
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    else:
        print("\n✅ All dependencies installed!")
        return True

def test_config():
    """Test if configuration is set up correctly"""
    print("\n" + "="*70)
    print("TEST 2: Checking Configuration")
    print("="*70)
    
    try:
        from config import (
            AI_PROVIDER, OPENAI_API_KEY, GEMINI_API_KEY,
            MODEL_PATH, VECTORIZER_PATH, CLEANED_DATA_PATH
        )
        
        print(f"✓ Configuration loaded")
        print(f"  AI Provider: {AI_PROVIDER}")
        
        # Check API key
        if AI_PROVIDER == 'openai':
            if OPENAI_API_KEY and OPENAI_API_KEY != 'your-openai-api-key-here':
                print(f"✓ OpenAI API key configured")
            else:
                print(f"⚠ OpenAI API key not configured")
                print(f"  Please add your API key to .env file")
        
        elif AI_PROVIDER == 'gemini':
            if GEMINI_API_KEY and GEMINI_API_KEY != 'your-gemini-api-key-here':
                print(f"✓ Gemini API key configured")
            else:
                print(f"⚠ Gemini API key not configured")
                print(f"  Please add your API key to .env file")
        
        print("\n✅ Configuration OK!")
        return True
    
    except Exception as e:
        print(f"✗ Configuration error: {str(e)}")
        return False

def test_data():
    """Test if data files exist"""
    print("\n" + "="*70)
    print("TEST 3: Checking Data Files")
    print("="*70)
    
    files_to_check = [
        ('dataset/naukri_com-job_sample.csv', 'Raw job data'),
    ]
    
    optional_files = [
        ('dataset/cleaned_job_data.csv', 'Cleaned data (run data_cleaning.ipynb to generate)'),
    ]
    
    all_good = True
    
    # Check required files
    for filepath, description in files_to_check:
        if os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"✓ {description}: {filepath} ({size_mb:.2f} MB)")
        else:
            print(f"✗ {description}: {filepath} - NOT FOUND")
            all_good = False
    
    # Check optional files
    for filepath, description in optional_files:
        if os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"✓ {description}: {filepath} ({size_mb:.2f} MB)")
        else:
            print(f"⚠ {description}: {filepath} - NOT FOUND")
    
    if all_good:
        print("\n✅ Required data files present!")
    else:
        print("\n⚠ Some required files are missing!")
    
    return all_good

def test_models():
    """Test if trained models exist"""
    print("\n" + "="*70)
    print("TEST 4: Checking Trained Models")
    print("="*70)
    
    model_files = [
        'models/tfidf_vectorizer.pkl',
        'models/job_matcher_model.pkl',
        'models/label_encoder.pkl',
    ]
    
    models_exist = True
    
    for filepath in model_files:
        if os.path.exists(filepath):
            size_kb = os.path.getsize(filepath) / 1024
            print(f"✓ {os.path.basename(filepath)} ({size_kb:.2f} KB)")
        else:
            print(f"✗ {os.path.basename(filepath)} - NOT FOUND")
            models_exist = False
    
    if models_exist:
        print("\n✅ All models present!")
        print("   System is ready to make predictions!")
    else:
        print("\n⚠ Models not found!")
        print("   Please run model_training.ipynb to train models")
    
    return models_exist

def test_resume_parser():
    """Test resume parser module"""
    print("\n" + "="*70)
    print("TEST 5: Testing Resume Parser Module")
    print("="*70)
    
    try:
        from resume_parser import ResumeParser
        print("✓ Resume parser module imported")
        
        # Try to initialize (won't work without valid API key)
        try:
            parser = ResumeParser()
            print("✓ Resume parser initialized")
            print(f"  Provider: {parser.provider}")
            return True
        except Exception as e:
            print(f"⚠ Could not initialize parser: {str(e)}")
            print("  This is expected if API key is not configured")
            return False
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_job_predictor():
    """Test job predictor module"""
    print("\n" + "="*70)
    print("TEST 6: Testing Job Predictor Module")
    print("="*70)
    
    try:
        from job_predictor import JobPredictor
        print("✓ Job predictor module imported")
        
        if os.path.exists('models/tfidf_vectorizer.pkl') and \
           os.path.exists('dataset/cleaned_job_data.csv'):
            try:
                predictor = JobPredictor()
                print("✓ Job predictor initialized")
                print(f"  Loaded {len(predictor.job_data)} job records")
                return True
            except Exception as e:
                print(f"✗ Could not initialize predictor: {str(e)}")
                return False
        else:
            print("⚠ Required files not found")
            print("  Run data_cleaning.ipynb and model_training.ipynb first")
            return False
    
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("RESUME ANALYZER - SYSTEM TEST")
    print("="*70)
    
    results = {
        'Dependencies': test_imports(),
        'Configuration': test_config(),
        'Data Files': test_data(),
        'Trained Models': test_models(),
        'Resume Parser': test_resume_parser(),
        'Job Predictor': test_job_predictor(),
    }
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20s}: {status}")
    
    print("\n" + "="*70)
    print(f"OVERALL: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\n🎉 All tests passed! Your system is ready to use!")
        print("\nNext steps:")
        print("1. Place a resume in uploads/resumes/")
        print("2. Run: python main.py")
    else:
        print("\n⚠ Some tests failed. Please check the issues above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure API key in .env file")
        print("3. Run data_cleaning.ipynb")
        print("4. Run model_training.ipynb")


if __name__ == "__main__":
    run_all_tests()
