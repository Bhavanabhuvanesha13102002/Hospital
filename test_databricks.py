import os
import requests
from urllib.parse import quote

from config.settings import DATABRICKS_HOST, DATABRICKS_TOKEN


class DatabricksUploader:

    def __init__(self):
        self.host = DATABRICKS_HOST.rstrip("/")
        self.token = DATABRICKS_TOKEN

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/octet-stream"
        }

    def upload_file_to_volume(self, local_file_path, volume_file_path):
        print("[INFO] Uploading to Databricks Volume using REST API")
        print(f"[INFO] Local file: {local_file_path}")
        print(f"[INFO] Volume path: {volume_file_path}")

        file_size_mb = os.path.getsize(local_file_path) / (1024 * 1024)
        print(f"[INFO] File size: {file_size_mb:.2f} MB")

        encoded_path = quote(volume_file_path, safe="")
        url = f"{self.host}/api/2.0/fs/files/{encoded_path}"

        with open(local_file_path, "rb") as file:
            response = requests.put(
                url,
                headers=self.headers,
                data=file,
                timeout=120
            )

        print("Status:", response.status_code)
        print("Response:", response.text)

        if response.status_code not in [200, 201, 204]:
            raise Exception(
                f"Upload failed. Status: {response.status_code}, Response: {response.text}"
            )

        print("[INFO] Upload completed successfully.")