import urllib.request
import zipfile
import os

url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
zip_path = "ffmpeg.zip"

print("Downloading FFmpeg...")
urllib.request.urlretrieve(url, zip_path)

print("Extracting FFmpeg...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    for file_info in zip_ref.infolist():
        if file_info.filename.endswith('ffmpeg.exe'):
            # Extract just ffmpeg.exe to the current directory
            file_info.filename = 'ffmpeg.exe'
            zip_ref.extract(file_info, '.')
            print("Extracted ffmpeg.exe")
            break

os.remove(zip_path)
print("Done!")
