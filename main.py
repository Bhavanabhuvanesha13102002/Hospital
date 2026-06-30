import pandas as pd

from config.datasets import DATASETS
from pipeline.ingestion.downloader import CMSDownloader
from pipeline.ingestion.mysql_loader import MySQLLoader
from pipeline.databricks.databricks_uploader import DatabricksUploader


SAMPLE_ROW_COUNT = 100


def create_sample_csv(csv_file):
    sample_csv_file = csv_file.replace(".csv", ".csv")

    df = pd.read_csv(csv_file)
    df.head(SAMPLE_ROW_COUNT).to_csv(sample_csv_file, index=False)

    print(f"[INFO] Sample CSV created: {sample_csv_file}")
    return sample_csv_file


def main():
    downloader = CMSDownloader()
    mysql_loader = MySQLLoader()
    databricks_uploader = DatabricksUploader()

    try:
        for dataset in DATASETS:

            if not dataset["url"]:
                print(f"[SKIP] {dataset['name']} - URL not configured.")
                continue

            csv_file = downloader.download_dataset(
                dataset_url=dataset["url"],
                output_filename=dataset["filename"]
            )

            mysql_loader.load_csv_to_mysql(
                csv_file=csv_file,
                table_name=dataset["raw_table"]
            )

            sample_csv_file = create_sample_csv(csv_file)

            databricks_uploader.upload_file_to_volume(
                local_file_path=sample_csv_file,
                volume_file_path=dataset["raw_path"]
            )

            print(f"[SUCCESS] {dataset['name']} pipeline completed.")

    finally:
        downloader.close()


if __name__ == "__main__":
    main()