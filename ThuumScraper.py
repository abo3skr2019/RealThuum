import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import concurrent.futures


def download_file(session, url, src, directory):
    file_url = urllib.parse.urljoin(url, src)
    url_path = urllib.parse.urlparse(file_url).path
    file_name = url_path.split("/revision")[0].split("/")[-1]

    if not file_name or file_name == "latest":
        print(f"Unexpected file name for URL {file_url}. Skipping download.")
        return

    file_path = os.path.join(directory, file_name)

    try:
        file_response = session.get(file_url)
        file_response.raise_for_status()
        with open(file_path, "wb") as file:
            file.write(file_response.content)
    except (requests.HTTPError, requests.ConnectionError, IOError) as err:
        print(f"Error occurred while downloading {file_url}: {err}")


def download_audio_files(url, directory):
    headers = {"User-Agent": "Mozilla/5.0"}

    with requests.Session() as session:
        session.headers.update(headers)

        try:
            response = session.get(url)
            response.raise_for_status()
        except (requests.HTTPError, requests.ConnectionError) as err:
            print(f"Error occurred: {err}")
            return

        soup = BeautifulSoup(response.content, "html.parser")
        audio_srcs = [audio["src"] for audio in soup.find_all("audio", src=True)]

        os.makedirs(directory, exist_ok=True)

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(
                lambda src: download_file(session, url, src, directory), audio_srcs
            )

        print("Download complete!")


# Example usage
url = os.getenv("ScraperURL")  # Replace with the URL you want to scrape
directory = (
    "TrainingData"  # Replace with the directory path where you want to save the files
)
download_audio_files(url, directory)
