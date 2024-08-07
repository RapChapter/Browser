import os
import requests
import zipfile
import shutil

GITHUB_REPO = 'https://github.com/DEIN_NUTZERNAME/DEIN_REPOSITORY'
ZIP_URL = f'{GITHUB_REPO}/archive/refs/heads/main.zip'
EXTRACT_TO = 'update_temp'

def download_and_extract_zip(url, extract_to):
    response = requests.get(url)
    response.raise_for_status()
    with open('update.zip', 'wb') as file:
        file.write(response.content)

    with zipfile.ZipFile('update.zip', 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    os.remove('update.zip')

def replace_files(source, destination):
    for item in os.listdir(source):
        s = os.path.join(source, item)
        d = os.path.join(destination, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

if __name__ == '__main__':
    download_and_extract_zip(ZIP_URL, EXTRACT_TO)
    replace_files(EXTRACT_TO, '.')
    shutil.rmtree(EXTRACT_TO)
    print('Update abgeschlossen. Starte den Browser neu.')
