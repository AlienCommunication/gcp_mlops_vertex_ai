from kfp.dsl import component, Output, Dataset

@component(
    packages_to_install=["google-cloud-bigquery", "pandas", "db-dtypes"],
    base_image="python:3.9"
)
def get_data_from_feature_store(
    project_id: str,
    bq_dataset: str,
    bq_table: str,
    dataset: Output[Dataset]
):
    from google.cloud import bigquery
    import pandas as pd

    client = bigquery.Client(project=project_id)
    
    # In a real scenario, this is the "Offline Store" fetch
    query = f"SELECT * FROM `{project_id}.{bq_dataset}.{bq_table}`"
    df = client.query(query).to_dataframe()
    
    df.to_csv(dataset.path, index=False)