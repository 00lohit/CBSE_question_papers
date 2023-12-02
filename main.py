import os
from bs4 import BeautifulSoup
import requests
import shutil
from urllib.parse import urljoin, urlparse, unquote
from zipfile import ZipFile
def download_question_papers(subject_name, standard, output_folder, error_log_path):
    # Ensure the output folder exists, create it if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_url = "https://www.cbse.gov.in/cbsenew/question-paper.html"
    response = requests.get(base_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', href=lambda href: subject_name.lower() in (href.lower() if href else '') and "zip" in (href.lower() if href else '') and f"/{standard.lower()}/" in (href.lower() if href else ''))


        for link in links:
            year = link.text.strip()
            paper_url = link['href'].strip()

            # Download the question paper
            download_url = urljoin(base_url, paper_url)

            # Extract the filename from the URL
            file_name = os.path.basename(unquote(urlparse(download_url).path))

            # Create a unique file name based on the subject, standard/class, year, and the URL pattern after "question-paper/"
            url_pattern = paper_url.split("question-paper/")[1].replace('/', '_').replace(':', '_').replace(' ', '_').replace('(', '_').replace(')', '_')
            unique_filename = f"{year.replace('-', '')}_{url_pattern}"

            # Remove the "Download_" prefix
            unique_filename = unique_filename.replace("Download_", "")

            paper_path = os.path.join(output_folder, unique_filename)

            try:
                with requests.get(download_url, stream=True) as r:
                    r.raise_for_status()  # Raise HTTPError for bad responses
                    with open(paper_path, 'wb') as file:
                        shutil.copyfileobj(r.raw, file)

                print(f"Downloaded {unique_filename} from {download_url}")
            except requests.exceptions.HTTPError as errh:
                log_error(error_log_path, f"HTTP Error: {errh}")
            except requests.exceptions.RequestException as err:
                log_error(error_log_path, f"Request Exception: {err}")

def log_error(error_log_path, message):
    with open(error_log_path, 'a') as log_file:
        log_file.write(f"{message}\n")

def extract_zip(zip_path, extraction_path):
    """
    Extract the contents of a ZIP file to the specified extraction path.
    :param zip_path: Path to the ZIP file.
    :param extraction_path: Path where the contents should be extracted.
    """
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)

def process_downloaded_files(output_folder, extraction_folder):
    # Get a list of all downloaded ZIP files
    zip_files = [file for file in os.listdir(output_folder) if file.endswith('.zip')]

    for zip_file in zip_files:
        zip_file_path = os.path.join(output_folder, zip_file)
        extraction_output_path = os.path.join(extraction_folder, os.path.splitext(zip_file)[0])

        # Extract the contents of the ZIP file
        extract_zip(zip_file_path, extraction_output_path)

        print(f"Extracted contents from {zip_file} to {extraction_output_path}")

        # Remove the original ZIP file
        os.remove(zip_file_path)
        print(f"Deleted {zip_file}")

if __name__ == "__main__":
    # Replace 'subject_name', 'standard', 'output_folder', and 'error_log_path' as before
    subject_name = 'ECONOMICS'
    standard = 'XII'
    output_folder = './question_papers'
    error_log_path = './error_log.txt'


    download_question_papers(subject_name, standard, output_folder, error_log_path)
    process_downloaded_files(output_folder, output_folder)
