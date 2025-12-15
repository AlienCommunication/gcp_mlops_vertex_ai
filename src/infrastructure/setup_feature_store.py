from google.cloud import aiplatform, bigquery
from config import *

def setup_infrastructure():
    aiplatform.init(project=PROJECT_ID, location=REGION)
    bq_client = bigquery.Client(project=PROJECT_ID)

    # 1. Prepare BigQuery Source (Clean Public Data)
    query = """
    CREATE OR REPLACE TABLE `{}.{}.{}` AS
    SELECT 
        species, 
        island, 
        culmen_length_mm, 
        culmen_depth_mm, 
        flipper_length_mm, 
        body_mass_g,
        sex,
        GENERATE_UUID() as entity_id, -- Unique ID for Feature Store
        CURRENT_TIMESTAMP() as feature_timestamp
    FROM `bigquery-public-data.ml_datasets.penguins`
    WHERE body_mass_g IS NOT NULL
    """.format(PROJECT_ID, BQ_DATASET, BQ_TABLE)
    
    # Create dataset if not exists
    bq_client.create_dataset(f"{PROJECT_ID}.{BQ_DATASET}", exists_ok=True)
    bq_client.query(query).result()
    print("BigQuery Data Prepared.")

    # 2. Create Feature Online Store (Optimized Serving)
    try:
        fs = aiplatform.FeatureOnlineStore.create(
            name=FEATURE_STORE_ID,
        )
        fs.wait()
    except Exception as e:
        print(f"Feature Store might already exist: {e}")

    # 3. Create Feature View (Links FS to BQ)
    try:
        fs = aiplatform.FeatureOnlineStore(FEATURE_STORE_ID)
        fs.create_feature_view(
            name=FEATURE_VIEW_ID,
            bigquery_source_uri=f"bq://{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}",
            sync_config=aiplatform.gapic.SyncConfig(cron="0 0 * * *") # Daily sync
        ).wait()
    except Exception as e:
        print(f"Feature View might already exist: {e}")

if __name__ == "__main__":
    setup_infrastructure()
