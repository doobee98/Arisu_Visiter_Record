import subprocess

def build():
    result = subprocess.run(['cmd', '/c', 'Build.bat'], cwd='.')
    exit(result.returncode)
