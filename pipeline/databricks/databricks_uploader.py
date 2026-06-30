import os
import time

from databricks.sdk import WorkspaceClient
from config.settings import DATABRICKS_HOST, DATABRICKS_TOKEN


class DatabricksUploader:

    def __init__(self):
        self.client = WorkspaceClient(
            host=DATABRICKS_HOST,
            token=DATABRICKS_TOKEN
        )

    def upload_file_to_volume(self, local_file_path, volume_file_path, retries=3):
        print("[INFO] Uploading file to Databricks Volume")
        print(f"[INFO] Local file: {local_file_path}")
        print(f"[INFO] Volume path: {volume_file_path}")

        file_size_mb = os.path.getsize(local_file_path) / (1024 * 1024)
        print(f"[INFO] File size: {file_size_mb:.2f} MB")

        last_error = None

        for attempt in range(1, retries + 1):
            try:
                print(f"[INFO] Upload attempt {attempt}/{retries}")

                with open(local_file_path, "rb") as file:
                    self.client.files.upload(
                        file_path=volume_file_path,
                        contents=file,
                        overwrite=True
                    )

                print("[INFO] Databricks upload completed successfully.")
                return

            except Exception as error:
                last_error = error
                print(f"[WARN] Upload failed: {error}")
                time.sleep(10)

        raise last_error