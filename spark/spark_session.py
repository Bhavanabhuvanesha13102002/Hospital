from pyspark.sql import SparkSession

from config.settings import APP_NAME


def create_spark_session():
    """
    Creates and returns a Spark Session with Delta Lake support.
    """

    spark = (
        SparkSession.builder
        .appName(APP_NAME)
        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension"
        )
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog"
        )
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    return spark