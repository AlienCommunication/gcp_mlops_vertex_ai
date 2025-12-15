from kfp.dsl import component, Input, Model, Output, Artifact

@component(
    packages_to_install=["google-cloud-aiplatform"],
    base_image="python:3.9"
)
def deploy_model_to_endpoint(
    model: Input[Model],
    project_id: str,
    region: str,
    display_name: str,
    serving_image: str,
    vertex_endpoint: Output[Artifact]
):
    from google.cloud import aiplatform

    aiplatform.init(project=project_id, location=region)
    # 1. Upload to Model Registry
    uploaded_model = aiplatform.Model.upload(
        display_name=display_name,
        artifact_uri=model.uri.replace("/model", ""), # Parent directory of model.joblib
        serving_container_image_uri=serving_image,
        serving_container_predict_route="/predict",
        serving_container_health_route="/health"
    )

    # 2. Create or Get Endpoint
    endpoints = aiplatform.Endpoint.list(filter=f'display_name="{display_name}-endpoint"')
    if endpoints:
        endpoint = endpoints 0 
    else:
        endpoint = aiplatform.Endpoint.create(display_name=f"{display_name}-endpoint")

    # 3. Deploy
    uploaded_model.deploy(
        endpoint=endpoint,
        machine_type="n1-standard-2",
        min_replica_count=1,
        max_replica_count=1,
        traffic_split={"0": 100}
    )
    
    vertex_endpoint.metadata["resourceName"] = endpoint.resource_name
    vertex_endpoint.uri = f"https://{region}-aiplatform.googleapis.com/v1/{endpoint.resource_name}"