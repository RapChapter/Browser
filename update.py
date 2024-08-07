import requests
import zipfile
import os

GITHUB_REPO = 'https://github.com/RapChapter/Browser'
DOWNLOAD_URL = f'{GITHUB_REPO}/archive/refs/heads/main.zip'
EXTRACT_TO = 'Browser-update'
ZIP_FILE = 'update.zip'

def download_update():
    response = requests.get(DOWNLOAD_URL, stream=True)
    response.raise_for_status()
    
    with open(ZIP_FILE, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def extract_update():
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_TO)

def replace_files():
    # Sicherstellen, dass die alten Dateien gesichert oder gelöscht werden
    if os.path.exists('backup'):
        os.rmdir('backup')
    os.rename('Browser.py', 'backup/Browser.py')
    
    # Kopiere neue Dateien
    os.rename(f'{EXTRACT_TO}/Browser-main/Browser.py', 'Browser.py')

def cleanup():
    os.remove(ZIP_FILE)
    os.rmdir(EXTRACT_TO)

def main():
    download_update()
    extract_update()
    replace_files()
    cleanup()

if __name__ == '__main__':
    main()
