import urllib.request
import zipfile
import os

url = "https://archive.ics.uci.edu/static/public/501/beijing+multi+site+air+quality+data.zip"
zip_path = "data/raw/data.zip"
extract_path = "data/raw/"

print("Downloading dataset...")
os.makedirs(extract_path, exist_ok=True)
urllib.request.urlretrieve(url, zip_path)
print("Download complete. Extracting...")

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

print("Extraction complete. Removing zip file...")
os.remove(zip_path)
print("Done!")
