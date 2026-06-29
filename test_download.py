from pipeline.ingestion.downloader import CMSDownloader

downloader = CMSDownloader()

downloader.download_dataset(
    dataset_url="https://data.cms.gov/provider-data/dataset/9n3s-kdb3",
    output_filename="general_info.csv"
)

downloader.close()