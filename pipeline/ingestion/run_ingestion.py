# import os

# from ingestion.downloader import CMSDownloader
# from ingestion.mysql_loader import MySQLLoader
# from config.settings import DOWNLOAD_FOLDER


# DATASET_URL = "https://data.cms.gov/provider-data/dataset/9n3s-kdb3"

# CSV_FILE = os.path.join(
#     DOWNLOAD_FOLDER,
#     "general_info.csv"
# )

# TABLE_NAME = "raw_general_info"


# def main():

#     downloader = CMSDownloader()

#     downloader.download_dataset(DATASET_URL)

#     downloader.close()

#     loader = MySQLLoader()

#     loader.load_csv_to_mysql(
#         CSV_FILE,
#         TABLE_NAME
#     )


# if __name__ == "__main__":
#     main()

# pipeline/ingestion/run_ingestion.py

from config.datasets import DATASETS
from pipeline.ingestion.downloader import CMSDownloader
from pipeline.ingestion.mysql_loader import MySQLLoader


def main():
    downloader = CMSDownloader()
    loader = MySQLLoader()

    try:
        for dataset in DATASETS:

            if not dataset["url"]:
                print(f"Skipping {dataset['name']} - URL not configured.")
                continue

            csv_file = downloader.download_dataset(
                dataset_url=dataset["url"],
                output_filename=dataset["filename"]
            )

            loader.load_csv_to_mysql(
                csv_file=csv_file,
                table_name=dataset["raw_table"]
            )

            print(f"{dataset['name']} ingestion completed successfully.")

    finally:
        downloader.close()


if __name__ == "__main__":
    main()