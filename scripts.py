import subprocess

def start():
    """Run index.py with poetry"""
    result = subprocess.run(['poetry', 'run', 'python', 'index.py'], cwd='.')
    exit(result.returncode)

def build():
    result = subprocess.run(['cmd', '/c', 'Build.bat'], cwd='.')
    exit(result.returncode)
