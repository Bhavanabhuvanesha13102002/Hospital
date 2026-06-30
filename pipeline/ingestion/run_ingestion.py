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