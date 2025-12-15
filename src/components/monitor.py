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
    from google.cloud.aiplatform import model_monitoring[ 3 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQESzLDLVkfmbvLYAPyVVRbjfWKJa3ZhfbSYHHJ6O_lzwjqDkrEkbMv_ypR9XTh3n1_yzPnqx0JC_YqUTXBiI0X8tLw3QEJjbdWYlW2ShimeIwLP-8NJYa5ZwcL2vwC1tdLXtj8_JF5D1K_MmaT6Ez-WRSwhuM7knL15qqiNudNohwpTINBz8kLaElpHww==)][ 6 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF6TctUvUjv9RK0-Ps9_P-osfV4hz3FkXJjlVip_leLJyEhTW6L9HPaamgnCzNPYaDEgguDlB41-8O0E24U7PzFBqH1iEL0RcxFvRj3drY69oG2GN4rldmgjBw88c8sCGrQAYoBMo7vZYqen_nsp9ixKNJA18M6flwK334w-XZ6Y7n2IHLKS67nuee3xSBUHMYF54a7ovgIOBsbuuwaQtb6pPXOY6VvUXsbeThIq14SsEqqdqtlp7bWpyLGw87H9XSwXQo_-TgtecHV8EIVZAoVuiYSaYrv9jf-vIf1q1xuNhFqJDqgge9_0IexXiX8DisNNM8U)][ 12 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHsVeyX46kVGju2gkDRHHWHUJJ1DAtA0OPtNPQnO4Y9Rp-IjXDiSDMgOyuxo_aft6FTv4I-8oAZPSws7PKRNXNh86XK-29JxAXsACsdAQv0wRD-qfAMATI-F5_RN_GP2e7ZrLS8avDXRgKTM_jgXgt4509AYhXGtAe3StI_4qKk13T3O5YqQDsco272CHhUzs1o)]

    aiplatform.init(project=project_id, location=region)[ 5 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF0hD0i4aZXeUg6L2LdPIgQX86orDELbjPu8XCVo-NU4KSIWI47g0wEvhFM5cIJ1jn9L53_svhLsVzLYSCQnlO-VOKa9e3W0q7FwVOso-VqnYQMLRmjV4gkak2fqg4-JV-UJruPUB_oxabFS5UhorQ1ww1rJK4=)]
    
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