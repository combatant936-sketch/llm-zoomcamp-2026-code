import os
import dlt
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["LOGFIRE_READ_TOKEN"]
BASE_URL = "https://logfire-us.pydantic.dev/v1/query"

@dlt.resource(name="traces", write_disposition="append")
def get_traces():
    query = """
        SELECT *
        FROM records
        WHERE otel_scope_name = 'pydantic-ai'
        ORDER BY start_timestamp DESC
    """
    resp = requests.get(
        BASE_URL,
        params={"sql": query},
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    resp.raise_for_status()
    data = resp.json()
    rows = data.get("rows", data)
    yield rows

pipeline = dlt.pipeline(
    pipeline_name="logfire_pipeline",
    destination="duckdb",
    dataset_name="agent_traces",
)

if __name__ == "__main__":
    load_info = pipeline.run(get_traces())
    print(load_info)