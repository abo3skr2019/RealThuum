import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import concurrent.futures

def download_file(url, headers, directory):
    file_url = urllib.parse.urljoin(url, src)
    file_name = os.path.basename(file_url)
    file_path = os.path.join(directory, file_name)

    try:
        file_response = requests.get(file_url, headers=headers)
        file_response.raise_for_status()
        with open(file_path, 'wb') as file:
            file.write(file_response.content)
    except (requests.HTTPError, requests.ConnectionError, IOError) as err:
        print(f"Error occurred while downloading {file_url}: {err}")

def download_audio_files(url, directory):
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except (requests.HTTPError, requests.ConnectionError) as err:
        print(f"Error occurred: {err}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    audio_srcs = [audio['src'] for audio in soup.find_all('audio', src=True)]

    os.makedirs(directory, exist_ok=True)

    # Use a ThreadPoolExecutor to download files concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_file, audio_srcs, [headers]*len(audio_srcs), [directory]*len(audio_srcs))

    print('Download complete!')
# Example usage
url = 'https://elderscrolls.fandom.com/wiki/Dragon_Shouts'  # Replace with the URL you want to scrape
directory = 'TrainingData'  # Replace with the directory path where you want to save the files
download_audio_files(url, directory)