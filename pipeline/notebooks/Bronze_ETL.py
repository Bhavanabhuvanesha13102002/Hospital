from config.datasets import DATASETS
from pipeline.bronze.bronze_job import process_bronze_dataset
from utils.metadata import get_source_quarter, get_pipeline_timestamp


SOURCE_QUARTER = get_source_quarter()
PIPELINE_TIMESTAMP = get_pipeline_timestamp()

print(f"Source Quarter     : {SOURCE_QUARTER}")
print(f"Pipeline Timestamp : {PIPELINE_TIMESTAMP}")


for dataset in DATASETS:

    if not dataset["url"]:
        print(f"[SKIP] {dataset['name']} - URL not configured.")
        continue

    bronze_df = process_bronze_dataset(
        spark=spark,
        dataset=dataset,
        source_quarter=SOURCE_QUARTER
    )

    bronze_df.show(20, truncate=False)