from config.datasets import DATASETS

from pipeline.ingestion.csv_downloader import CSVDownloader

from spark.bronze_job import run_bronze_pipeline


def download_all_datasets():

    downloader = CSVDownloader()

    for dataset in DATASETS:

        if dataset["download_url"]:

            downloader.download(
                url=dataset["download_url"],
                filename=dataset["input_file"].split("/")[-1]
            )


if __name__ == "__main__":

    print("=" * 60)
    print("Hospital Quality Bronze Pipeline")
    print("=" * 60)

    # Step 1 - Download all datasets
    download_all_datasets()

    # Step 2 - Execute Bronze Pipeline
    run_bronze_pipeline()

    print("=" * 60)
    print("Pipeline Completed Successfully")
    print("=" * 60)