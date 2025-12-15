from kfp import dsl, compiler
from src.components.data_ingest import get_data_from_feature_store
from src.components.train import train_model
from src.components.deploy import deploy_model_to_endpoint
from src.components.monitor import setup_monitoring
from config import *

#pipeline
@dsl.pipeline(
    name="penguin-training-pipeline",
    description="End-to-end MLOps pipeline with Feature Store and Monitoring",
    pipeline_root=PIPELINE_ROOT
)
def pipeline(
    project_id: str = PROJECT_ID,
    region: str = REGION,
    bq_dataset: str = BQ_DATASET,
    bq_table: str = BQ_TABLE,
    model_name: str = MODEL_DISPLAY_NAME,
    serving_image: str = SERVING_IMAGE,
    notification_email: str = "your-email@example.com"
):
    # 1. Data Ingestion
    ingest_task = get_data_from_feature_store(
        project_id=project_id,
        bq_dataset=bq_dataset,
        bq_table=bq_table
    )

    # 2. Training & Experiments
    train_task = train_model(
        input_data=ingest_task.outputs["dataset"],
        project_id=project_id,
        region=region,
        experiment_name="penguin-exp-1",
        model_display_name=model_name
    )

    # 3. Deployment & Registry
    deploy_task = deploy_model_to_endpoint(
        model=train_task.outputs["model_output"],
        project_id=project_id,
        region=region,
        display_name=model_name,
        serving_image=serving_image
    )

    # 4. Monitoring Setup (Runs after deployment)
    setup_monitoring(
        project_id=project_id,
        region=region,
        endpoint=deploy_task.outputs["vertex_endpoint"],
        email=notification_email
    )

if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=pipeline,
        package_path="training_pipeline.json"
    )