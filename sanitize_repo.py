"""Sanitize repository before publishing to GitHub.

Deletes user-uploaded resumes, result artifacts, trained model binaries,
and cleaned datasets. Writes small placeholder files to indicate removal.

Run: python sanitize_repo.py
"""
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent

def remove_files_in(dirpath):
    p = ROOT / dirpath
    if not p.exists():
        return
    for child in p.iterdir():
        try:
            if child.is_file() or child.is_symlink():
                child.unlink()
            elif child.is_dir():
                shutil.rmtree(child)
        except Exception as e:
            print(f"Failed to remove {child}: {e}")

def write_placeholder(path, message):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(message, encoding='utf-8')

def main():
    print("Sanitizing repository: removing sensitive files...")

    # Directories to clear
    remove_files_in('uploads/resumes')
    remove_files_in('results')
    remove_files_in('logs')

    # Remove model binary files but keep a placeholder metadata file
    models_dir = ROOT / 'models'
    if models_dir.exists():
        for f in models_dir.iterdir():
            if f.is_file() and f.suffix.lower() in ('.pkl', '.npz', '.bin'):
                try:
                    f.unlink()
                except Exception as e:
                    print(f"Failed to remove model file {f}: {e}")

    # Remove cleaned/derived datasets
    dataset_dir = ROOT / 'dataset'
    if dataset_dir.exists():
        for f in dataset_dir.iterdir():
            if f.is_file() and (f.name.startswith('cleaned') or 'updated' in f.name.lower()):
                try:
                    f.unlink()
                except Exception as e:
                    print(f"Failed to remove dataset file {f}: {e}")

    # Write placeholders
    write_placeholder('uploads/README.md', 'User resumes removed for privacy.\n')
    write_placeholder('results/README.md', 'Analysis results removed for privacy. Re-run locally to regenerate.\n')
    write_placeholder('logs/README.md', 'Logs removed.\n')

    # Sanitize model_metadata.json
    meta = models_dir / 'model_metadata.json'
    if meta.exists():
        meta.write_text('{"sanitized": true, "note": "Model binaries removed for publishing."}\n', encoding='utf-8')

    print("Sanitization complete. Please review changes and commit.")

if __name__ == '__main__':
    main()
