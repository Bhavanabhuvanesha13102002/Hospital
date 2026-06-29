import os

from config.datasets import DATASETS
from spark.spark_session import create_spark_session
from pipeline.ingestion.bronze_writer import BronzeWriter


def run_bronze_pipeline():

    spark = create_spark_session()

    writer = BronzeWriter()

    for dataset in DATASETS:

        if not os.path.exists(dataset["input_file"]):
           print(f"Skipping {dataset['name']} - file not found.")
           continue

        extractor = dataset["extractor"](spark)

        raw_df = extractor.extract(dataset["input_file"])

        raw_df.createOrReplaceTempView(dataset["temp_view"])

        with open(dataset["sql_file"], "r") as file:
            query = file.read()

        bronze_df = spark.sql(query)

        writer.write(
            dataframe=bronze_df,
            output_path=dataset["output_path"],
            dataset_name=dataset["name"]
        )

    spark.stop()