import os

PROJECT_ID = "classdemo-425210"
REGION = "us-central1"
BUCKET_NAME = f"gs://{PROJECT_ID}-vertex-artifacts"
SERVICE_ACCOUNT = f"vertex-sa@{PROJECT_ID}.iam.gserviceaccount.com"

# Feature Store (BigQuery-backed)
FEATURE_STORE_ID = "penguin_feature_store"
FEATURE_VIEW_ID = "penguin_view"
BQ_DATASET = "penguin_dataset"
BQ_TABLE = "penguins_cleaned"

# Model
MODEL_DISPLAY_NAME = "penguin-classifier"
SERVING_IMAGE = "us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-0:latest"
PIPELINE_ROOT = f"{BUCKET_NAME}/pipeline_root"