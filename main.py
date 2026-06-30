import pandas as pd

from config.datasets import DATASETS
from pipeline.ingestion.downloader import CMSDownloader
from pipeline.ingestion.mysql_loader import MySQLLoader
from pipeline.databricks.databricks_uploader import DatabricksUploader
from pipeline.databricks.job_runner import DatabricksJobRunner


SAMPLE_ROW_COUNT = 100
USE_SAMPLE_FILE = True   


def create_sample_csv(csv_file):
    sample_csv_file = csv_file.replace(".csv", "_sample.csv")

    df = pd.read_csv(csv_file)
    df.head(SAMPLE_ROW_COUNT).to_csv(sample_csv_file, index=False)

    print(f"[INFO] Sample CSV created: {sample_csv_file}")
    print(f"[INFO] Sample rows: {SAMPLE_ROW_COUNT}")

    return sample_csv_file


def main():
    downloader = CMSDownloader()
    mysql_loader = MySQLLoader()
    databricks_uploader = DatabricksUploader()
    job_runner = DatabricksJobRunner()

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

            upload_file = csv_file

            if USE_SAMPLE_FILE:
                upload_file = create_sample_csv(csv_file)

            databricks_uploader.upload_file_to_volume(
                local_file_path=upload_file,
                volume_file_path=dataset["raw_path"]
            )

            print(f"[SUCCESS] {dataset['name']} ingestion completed.")

        job_runner.run_bronze_job()

    finally:
        downloader.close()


if __name__ == "__main__":
    main()