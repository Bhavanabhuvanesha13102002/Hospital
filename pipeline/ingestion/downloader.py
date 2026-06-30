   
import glob
import os
import shutil
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import DOWNLOAD_FOLDER


class CMSDownloader:

    def __init__(self):
        os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

        chrome_options = Options()

        prefs = {
            "download.default_directory": os.path.abspath(DOWNLOAD_FOLDER),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }

        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        self.driver.maximize_window()

    def download_dataset(self, dataset_url, output_filename):
        print("=" * 60)
        print(f"Downloading : {output_filename}")
        print("=" * 60)

        self.driver.get(dataset_url)

        wait = WebDriverWait(self.driver, 30)

        download_button = wait.until(
            EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, "Download full dataset")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            download_button
        )

        time.sleep(2)

        self.driver.execute_script(
            "arguments[0].click();",
            download_button
        )

        print("Download started...")

        time.sleep(20)

        csv_files = glob.glob(
            os.path.join(DOWNLOAD_FOLDER, "*.csv")
        )

        if not csv_files:
            raise Exception("No CSV file found after download.")

        latest_file = max(csv_files, key=os.path.getctime)

        destination = os.path.join(
            DOWNLOAD_FOLDER,
            output_filename
        )

        if os.path.exists(destination):
            os.remove(destination)

        shutil.move(latest_file, destination)

        print(f"Saved as : {destination}")

        return destination

    def close(self):
        self.driver.quit()