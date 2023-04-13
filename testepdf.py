import requests
from bs4 import BeautifulSoup
import os
from time import sleep
import shutil
import lxml
url = 'https://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?jornal=529&pagina=62&data=12/04/2023&captchafield=firstAccess'
antigaurl = "https://pesquisa.in.gov.br/imprensa/jsp/visualiza/index.jsp?jornal=529&pagina=62&data=12/04/2023"


folder_path = "C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\FetchDOU\\PDFs\\"


# Send a GET request to the URL
response = requests.get(url)
sleep(3)
# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, "lxml")
sleep(3)
# Find the URL of the embedded PDF file
pdf_url = None
for tag in soup.find_all(["embed", "object", "iframe"]):
    if tag.name == "embed" and tag.get("type") == "application/pdf":
        pdf_url = tag.get("src")
        break
    elif tag.name in ["object", "iframe"]:
        embed_tag = tag.find("embed")
        if embed_tag and embed_tag.get("type") == "application/pdf":
            pdf_url = embed_tag.get("src")
            break

# Construct the absolute URL of the PDF file
if pdf_url and not pdf_url.startswith("http"):
    base_url = response.url.rsplit("/", 1)[0]
    pdf_url = f"{base_url}/{pdf_url}"

# Download the PDF file to the specified folder
if pdf_url:
    try:
        response = requests.get(pdf_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(folder_path, os.path.basename(pdf_url))
            with open(file_path, "wb") as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
                print("PDF file saved successfully.")
        else:
            print(f"Error downloading PDF file. HTTP status code: {response.status_code}")
    except Exception as e:
        print(f"Error saving PDF file: {str(e)}")
else:
    print("No embedded PDF file found.")






