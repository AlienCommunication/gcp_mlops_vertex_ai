import sys
import os
from google.api_core import exceptions
from google.cloud import aiplatform
from google.cloud import aiplatform_v1
from google.cloud import bigquery
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from config import *

def setup_infrastructure():
    aiplatform.init(project=PROJECT_ID, location=REGION)
    bq_client = bigquery.Client(project=PROJECT_ID)
    print("Preparing BigQuery Data...")
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
    
    bq_client.create_dataset(f"{PROJECT_ID}.{BQ_DATASET}", exists_ok=True)
    bq_client.query(query).result()
    print("BigQuery Data Prepared.")    
    # 1. Create the Admin Client
    admin_client = aiplatform_v1.FeatureOnlineStoreAdminServiceClient(
        client_options={"api_endpoint": f"{REGION}-aiplatform.googleapis.com"}
    )
    parent = f"projects/{PROJECT_ID}/locations/{REGION}"

    # 2. Create Feature Online Store
    print(f"Creating Feature Online Store: {FEATURE_STORE_ID}...")
    
    # Define the configuration (using Bigtable AutoScaling)
    online_store_config = aiplatform_v1.FeatureOnlineStore(
        bigtable=aiplatform_v1.FeatureOnlineStore.Bigtable(
            auto_scaling=aiplatform_v1.FeatureOnlineStore.Bigtable.AutoScaling(
                min_node_count=1, 
                max_node_count=1, 
                cpu_utilization_target=50
            )
        )
    )

    try:
        lro = admin_client.create_feature_online_store(
            parent=parent,
            feature_online_store_id=FEATURE_STORE_ID,
            feature_online_store=online_store_config,
        )
        print("Waiting for Feature Store creation (this handles retry internally)...")
        lro.result()
        print("Feature Online Store created.")
    except exceptions.AlreadyExists:
        print(f"Feature Online Store '{FEATURE_STORE_ID}' already exists. Skipping creation.")
    except Exception as e:
        print(f"Error creating Feature Store: {e}")

    # 3. Create Feature View (Links FS to BQ)
    print(f"Creating Feature View: {FEATURE_VIEW_ID}...")

    # Define Feature View configuration
    feature_view_config = aiplatform_v1.FeatureView(
        big_query_source=aiplatform_v1.FeatureView.BigQuerySource(
            uri=f"bq://{PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}",
            entity_id_columns=["entity_id"]
        ),
        sync_config=aiplatform_v1.FeatureView.SyncConfig(
            cron="0 0 * * *"
        )
    )

    try:
        lro = admin_client.create_feature_view(
            parent=f"{parent}/featureOnlineStores/{FEATURE_STORE_ID}",
            feature_view_id=FEATURE_VIEW_ID,
            feature_view=feature_view_config
        )
        print("Waiting for Feature View creation...")
        lro.result()
        print("Feature View created.")
    except exceptions.AlreadyExists:
        print(f"Feature View '{FEATURE_VIEW_ID}' already exists. Skipping creation.")
    except Exception as e:
        print(f"Error creating Feature View: {e}")

if __name__ == "__main__":
    setup_infrastructure()