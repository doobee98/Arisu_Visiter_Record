import zipfile
import os
import sys

def create_zip(zip_name, *items):
    """Create zip file from files and/or folders"""
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
        for item in items:
            if os.path.isfile(item):
                # 파일인 경우
                z.write(item, os.path.basename(item))
            elif os.path.isdir(item):
                # 폴더인 경우
                for root, dirs, files in os.walk(item):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.join(os.path.relpath(root, '.'), file)
                        z.write(file_path, arcname)
    print(f"✓ {zip_name} created")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python zip.py <zip_name> <item1> [item2] ...")
        sys.exit(1)
    create_zip(sys.argv[1], *sys.argv[2:])
