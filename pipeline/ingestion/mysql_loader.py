# import pandas as pd

# from config.database import engine


# class MySQLLoader:

#     def __init__(self):
#         self.engine = engine

#     def load_csv_to_mysql(self, csv_file, table_name):

#         print(f"\nReading CSV: {csv_file}")

#         df = pd.read_csv(csv_file)

#         print(f"Rows : {len(df)}")
#         print(f"Columns : {len(df.columns)}")

#         print("\nLoading data into MySQL...")

#         df.to_sql(
#             name=table_name,
#             con=self.engine,
#             if_exists="replace",
#             index=False
#         )

#         print(f"\nSuccessfully loaded into table '{table_name}'")



import re
import pandas as pd

from config.database import engine


class MySQLLoader:

    def __init__(self):
        self.engine = engine

    def clean_column_names(self, df):
        cleaned_columns = []
        column_count = {}

        for column in df.columns:
            column = column.strip().lower()
            column = column.replace(" ", "_")
            column = column.replace("-", "_")
            column = re.sub(r"[()]", "", column)
            column = column.replace("/", "_")
            column = column.replace(",", "")
            column = column.replace("%", "percent")
            column = column.replace(".", "")
            column = re.sub(r"[^a-zA-Z0-9_]", "", column)
            column = re.sub(r"_+", "_", column)
            column = column.strip("_")

            if column in column_count:
                column_count[column] += 1
                column = f"{column}_{column_count[column]}"
            else:
                column_count[column] = 1

            cleaned_columns.append(column)

        df.columns = cleaned_columns
        return df

    def load_csv_to_mysql(self, csv_file, table_name):
        print("=" * 70)
        print(f"Loading CSV: {csv_file}")
        print("=" * 70)

        df = pd.read_csv(csv_file)
        df = self.clean_column_names(df)

        print(f"Rows: {len(df)}")
        print(f"Columns: {len(df.columns)}")

        df.to_sql(
            name=table_name,
            con=self.engine,
            if_exists="replace",
            index=False
        )

        print(f"Successfully loaded into table: {table_name}")