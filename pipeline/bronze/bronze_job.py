from delta.tables import DeltaTable
from pyspark.sql.functions import current_timestamp, lit, col
from pyspark.sql.types import StructType


METADATA_COLUMNS = ["source_quarter", "ingestion_timestamp"]


def read_raw_data(spark, dataset):
    print(f"[INFO] Reading raw file: {dataset['raw_path']}")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(dataset["raw_path"])
    )

    print(f"[INFO] Raw count: {df.count()}")
    return df


def select_required_columns(df, dataset):
    print(f"[INFO] Selecting required columns for: {dataset['name']}")
    return df.select(*dataset["required_columns"])


def remove_duplicates(df, dataset):
    before_count = df.count()
    dedup_df = df.dropDuplicates(dataset["dedup_columns"])
    after_count = dedup_df.count()

    print(f"[INFO] Rows before deduplication: {before_count}")
    print(f"[INFO] Rows after deduplication: {after_count}")
    print(f"[INFO] Duplicate rows removed: {before_count - after_count}")

    return dedup_df


def remove_existing_metadata_columns(df):
    for column_name in METADATA_COLUMNS:
        if column_name in df.columns:
            df = df.drop(column_name)

    return df


def add_metadata_columns(df, source_quarter):
    df = remove_existing_metadata_columns(df)

    return (
        df
        .withColumn("source_quarter", lit(source_quarter))
        .withColumn("ingestion_timestamp", current_timestamp())
    )


def delta_exists(spark, path):
    try:
        return DeltaTable.isDeltaTable(spark, path)
    except Exception:
        return False


def create_initial_bronze(df, dataset):
    print(f"[INFO] Bronze does not exist. Creating initial Bronze: {dataset['bronze_path']}")

    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(dataset["bronze_path"])
    )

    print(f"[INFO] Initial Bronze created for: {dataset['name']}")


def build_join_condition(left_alias, right_alias, key_columns):
    conditions = [
        col(f"{left_alias}.{key}") == col(f"{right_alias}.{key}")
        for key in key_columns
    ]

    final_condition = conditions[0]

    for condition in conditions[1:]:
        final_condition = final_condition & condition

    return final_condition


def build_change_condition(current_alias, existing_alias, compare_columns):
    conditions = [
        col(f"{current_alias}.{column}") != col(f"{existing_alias}.{column}")
        for column in compare_columns
    ]

    final_condition = conditions[0]

    for condition in conditions[1:]:
        final_condition = final_condition | condition

    return final_condition


def get_new_records(current_df, existing_df, dataset):
    join_condition = build_join_condition(
        left_alias="current",
        right_alias="existing",
        key_columns=dataset["dedup_columns"]
    )

    new_df = (
        current_df.alias("current")
        .join(
            existing_df.alias("existing"),
            join_condition,
            "left_anti"
        )
    )

    print(f"[INFO] New records found: {new_df.count()}")
    return new_df


def get_changed_records(current_df, existing_df, dataset):
    join_condition = build_join_condition(
        left_alias="current",
        right_alias="existing",
        key_columns=dataset["dedup_columns"]
    )

    change_condition = build_change_condition(
        current_alias="current",
        existing_alias="existing",
        compare_columns=dataset["compare_columns"]
    )

    changed_current_df = (
        current_df.alias("current")
        .join(
            existing_df.alias("existing"),
            join_condition,
            "inner"
        )
        .where(change_condition)
        .select("current.*")
    )

    changed_existing_df = (
        existing_df.alias("existing")
        .join(
            changed_current_df.alias("changed"),
            build_join_condition(
                left_alias="existing",
                right_alias="changed",
                key_columns=dataset["dedup_columns"]
            ),
            "inner"
        )
        .select("existing.*")
    )

    print(f"[INFO] Changed records found: {changed_current_df.count()}")

    return changed_current_df, changed_existing_df


def archive_changed_records(changed_existing_df, dataset):
    changed_count = changed_existing_df.count()

    if changed_count == 0:
        print("[INFO] No records to archive.")
        return

    print(f"[INFO] Archiving old changed records: {changed_count}")

    (
        changed_existing_df.write
        .format("delta")
        .mode("append")
        .save(dataset["archive_path"])
    )

    print(f"[INFO] Archive completed: {dataset['archive_path']}")


def rebuild_bronze(existing_df, new_df, changed_current_df, dataset):
    key_columns = dataset["dedup_columns"]

    changed_keys_df = changed_current_df.select(*key_columns).dropDuplicates()

    unchanged_existing_df = (
        existing_df.alias("existing")
        .join(
            changed_keys_df.alias("changed"),
            build_join_condition(
                left_alias="existing",
                right_alias="changed",
                key_columns=key_columns
            ),
            "left_anti"
        )
    )

    final_bronze_df = (
        unchanged_existing_df
        .unionByName(changed_current_df)
        .unionByName(new_df)
    )

    return final_bronze_df


def write_updated_bronze(final_bronze_df, dataset):
    print(f"[INFO] Writing updated Bronze: {dataset['bronze_path']}")

    (
        final_bronze_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .save(dataset["bronze_path"])
    )

    print(f"[INFO] Bronze update completed for: {dataset['name']}")


def process_bronze_dataset(spark, dataset, source_quarter):
    print("=" * 80)
    print(f"[START] Bronze processing: {dataset['name']}")
    print("=" * 80)

    raw_df = read_raw_data(spark, dataset)
    selected_df = select_required_columns(raw_df, dataset)
    dedup_df = remove_duplicates(selected_df, dataset)

    current_df = add_metadata_columns(dedup_df, source_quarter)

    if not delta_exists(spark, dataset["bronze_path"]):
        create_initial_bronze(current_df, dataset)
        return current_df

    print(f"[INFO] Existing Bronze found: {dataset['bronze_path']}")

    existing_df = spark.read.format("delta").load(dataset["bronze_path"])

    new_df = get_new_records(
        current_df=current_df,
        existing_df=existing_df,
        dataset=dataset
    )

    changed_current_df, changed_existing_df = get_changed_records(
        current_df=current_df,
        existing_df=existing_df,
        dataset=dataset
    )

    archive_changed_records(
        changed_existing_df=changed_existing_df,
        dataset=dataset
    )

    final_bronze_df = rebuild_bronze(
        existing_df=existing_df,
        new_df=new_df,
        changed_current_df=changed_current_df,
        dataset=dataset
    )

    write_updated_bronze(
        final_bronze_df=final_bronze_df,
        dataset=dataset
    )

    print("=" * 80)
    print(f"[END] Bronze processing completed: {dataset['name']}")
    print("=" * 80)

    return final_bronze_df