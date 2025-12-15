from kfp.dsl import component, Input, Artifact

@component(
    packages_to_install=["google-cloud-aiplatform"],
    base_image="python:3.9"
)
def setup_monitoring(
    project_id: str,
    region: str,
    endpoint: Input[Artifact],
    email: str
):
    from google.cloud import aiplatform
    from google.cloud.aiplatform import model_monitoring
    aiplatform.init(project=project_id, location=region)
    endpoint_name = endpoint.metadata["resourceName"]
    my_endpoint = aiplatform.Endpoint(endpoint_name)

    # Configure Skew Detection
    skew_config = model_monitoring.SkewDetectionConfig(
        data_source="", # Usually training data URI, simplified here
        skew_thresholds={"body_mass_g": 0.001}, # Monitoring specific feature
        attribute_skew_thresholds={"body_mass_g": 0.001}
    )

    # Configure Drift Detection
    drift_config = model_monitoring.DriftDetectionConfig(
        drift_thresholds={"body_mass_g": 0.001}
    )

    # Create Monitoring Job
    job = aiplatform.ModelDeploymentMonitoringJob.create(
        display_name="penguin-monitoring-job",
        logging_sampling_strategy=model_monitoring.RandomSampleConfig(sample_rate=0.8),
        schedule_config=model_monitoring.ScheduleConfig(monitor_interval=24), # Hours
        alert_config=model_monitoring.EmailAlertConfig(user_emails=[email]),
        objective_config=model_monitoring.ObjectiveConfig(
            skew_detection_config=skew_config,
            drift_detection_config=drift_config
        ),
        endpoint=my_endpoint
    )