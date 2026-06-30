from databricks.sdk import WorkspaceClient
from config.settings import DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_JOB_ID


class DatabricksJobRunner:

    def __init__(self):
        self.client = WorkspaceClient(
            host=DATABRICKS_HOST,
            token=DATABRICKS_TOKEN
        )

    def run_bronze_job(self):
        print("[INFO] Triggering Databricks Bronze Job...")

        run = self.client.jobs.run_now(
            job_id=int(DATABRICKS_JOB_ID)
        )

        print(f"[INFO] Bronze Job triggered successfully. Run ID: {run.run_id}")

        return run.run_id