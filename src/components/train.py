from kfp.dsl import component, Input, Output, Dataset, Model, Metrics

@component(
    packages_to_install=["scikit-learn", "pandas", "google-cloud-aiplatform", "joblib"],
    base_image="python:3.9"
)
def train_model(
    input_data: Input[Dataset],
    model_output: Output[Model],
    metrics: Output[Metrics],
    project_id: str,
    region: str,
    experiment_name: str,
    model_display_name: str
):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
    from google.cloud import aiplatform
    import joblib
    import os[ 1 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE96YphVQYI1uqiYKBVWIYW51Ir0rER1Xb3LnMfBIolbL7J7qx-VHQJ6htc_XI8sFQsGX2pb1ejLwu6PdimXApm94wy5pTHCdEi7fhDcC4V2dczIWgLPp5_bX7s88vQjTSoJaC9fbblOr3JZvLcBJRp5ZL55L_c22-cZsFr7pJ0gtbItieNIlWIB05FLDV2fEi18HKtkJg99jpQR-9YNZF4rhG-Q-s8oYHjaPtzp0ZveocEytT8O0OC1TphCaRxhg==)][ 2 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEQZMfXCy8d7KLOnZPUn1RvP0rwqmv5_jS0VUwg5T-xbjR2fq5m17bGvPPRzM8kN-ddGj_BVCbWH3HaRDaH5RuO09qIKJ-Jt1UiwPXf6x84VUsZNh-0NXTVBCDnuJDQVUVtVFfm5_ZhSCIAaTT908sX9ivdQVgknr_93cMy1nJoWUrmaNroES8Yk-EROfJNsnQptzCfQoUDCcowcABLiaK5OJrJJzYg0JGfhLPTb29rB_t-oD_t)][ 3 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQESzLDLVkfmbvLYAPyVVRbjfWKJa3ZhfbSYHHJ6O_lzwjqDkrEkbMv_ypR9XTh3n1_yzPnqx0JC_YqUTXBiI0X8tLw3QEJjbdWYlW2ShimeIwLP-8NJYa5ZwcL2vwC1tdLXtj8_JF5D1K_MmaT6Ez-WRSwhuM7knL15qqiNudNohwpTINBz8kLaElpHww==)][ 4 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEr70Ougt8pi-0vhaqyszHuTa39cWY9Pos80qvuwKdcAoXYcGNfRKlqdEerMeFgKRzhN7D-oMxy4JZRWJhXfOcLBkzJOd8veSFFpYEaezlI21Oq8UJV8btGox_lAfR70CN3xXS3K6QUqVfW-4dy-bVimazekGXXYLVg29Jp8aLJ-UEZa7fyYxrccja4CgJRl8jb4fAtm_7wbJWwx0FjA98SjNJvi4EXEg0=)][ 5 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF0hD0i4aZXeUg6L2LdPIgQX86orDELbjPu8XCVo-NU4KSIWI47g0wEvhFM5cIJ1jn9L53_svhLsVzLYSCQnlO-VOKa9e3W0q7FwVOso-VqnYQMLRmjV4gkak2fqg4-JV-UJruPUB_oxabFS5UhorQ1ww1rJK4=)][ 6 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF6TctUvUjv9RK0-Ps9_P-osfV4hz3FkXJjlVip_leLJyEhTW6L9HPaamgnCzNPYaDEgguDlB41-8O0E24U7PzFBqH1iEL0RcxFvRj3drY69oG2GN4rldmgjBw88c8sCGrQAYoBMo7vZYqen_nsp9ixKNJA18M6flwK334w-XZ6Y7n2IHLKS67nuee3xSBUHMYF54a7ovgIOBsbuuwaQtb6pPXOY6VvUXsbeThIq14SsEqqdqtlp7bWpyLGw87H9XSwXQo_-TgtecHV8EIVZAoVuiYSaYrv9jf-vIf1q1xuNhFqJDqgge9_0IexXiX8DisNNM8U)][ 7 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFFaB-S2AO3JgAZQA2hSno80g8lziugiF86gkHqS4t12dsLXVsuR2EYjJFxRSqVJgEyiT3JBn_Kd5BggSd8zX3e287ej_OBZNshlnGyBdRCemQq23MvEoNyY7wh32t42JSYq98P2YbzzcecLUIC_e3e7-HlCPf2boxIRbIcIpHsIrwWy7VGhlIlNo1l-q_Gk6M0CxUIEgurNs7p1ar9vjISssiM4_roq3iyoJ9x4TGu)][ 8 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGGJedtZvbZgQVdD3Lkk-bVh-7v8LD55GGHf2uJrdY6a0Oi4WN1UOGf5mCKDnlgYr4TPM-mm7LIb0fCqBOTYQZZT62qX2qW4GcDETcPAJu3mO3NZUAngCClETITiw==)][ 9 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGIX4gjGItjghdrXyaZszwlhCpF90Ry56h44XfsxUWNEqPibKWTjWstxTchZUPBOBcUwN7ieGNetNz3EFzReeO90-bQxCXvDM8lHDUt2w1SHTn1xcy96mClDnVnfD6eAEUUxP06yvKojWGAErAdslvig8Rge9Xpjdu5ihEF0w==)][ 10 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHUZOzToxNyTgnHZEQghwNnUQpM40h2HflooRXfO1A130Z83nASxhQrIkmLtdd4e4YsQSfCwgnp07GDF6Qyk0HiKoiUFn3UoQ3s02_FTMN_2czjsDU3n8GwxpteYP1qCB1nhfe6PeF7E47WIZJkhyrPGfLNOSkuo6Ch5g9lk9e6K6gMKemRl-j68gGe0jexp3WlgUlmI_3mMAuZMU5Sag7ceBOLmidCRrQGSKmOeCe1LNw=)][ 11 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHra8Nc92AHh9FRBYstPhPjCcdQrQLqCcfW41OzXsfNn3TE3zNcDe1MjUs5SP1QTlstVqBFFyhm8bPwsRfK-lzuXc1QXLgOeC1nyFmNKpEFk9-mlYhvgpV7quFbYk15Z7M5NnngQwPmIjlhDImghkqpcQDpEmpP_AjoiSQvQTyacBG12iUQoZM9iq5BthHjcQeuQrpJGb42w3phru4CDX45b4fx0CQ0)][ 12 (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHsVeyX46kVGju2gkDRHHWHUJJ1DAtA0OPtNPQnO4Y9Rp-IjXDiSDMgOyuxo_aft6FTv4I-8oAZPSws7PKRNXNh86XK-29JxAXsACsdAQv0wRD-qfAMATI-F5_RN_GP2e7ZrLS8avDXRgKTM_jgXgt4509AYhXGtAe3StI_4qKk13T3O5YqQDsco272CHhUzs1o)]

    # 1. Load Data
    df = pd.read_csv(input_data.path)
    df = df.dropna()
    
    # Simple Encoding for demo
    X = pd.get_dummies(df.drop(columns=['species', 'entity_id', 'feature_timestamp']))
    y = df['species']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # 2. Track Experiment
    aiplatform.init(project=project_id, location=region, experiment=experiment_name)
    aiplatform.start_run("run-v1")
    
    params = {"n_estimators": 100, "max_depth": 5}
    aiplatform.log_params(params)

    # 3. Train
    clf = RandomForestClassifier(**params)
    clf.fit(X_train, y_train)
    
    # 4. Evaluate
    acc = accuracy_score(y_test, clf.predict(X_test))
    aiplatform.log_metrics({"accuracy": acc})
    metrics.log_metric("accuracy", acc)

    # 5. Save Model Artifact (sklearn format)
    os.makedirs(model_output.path, exist_ok=True)
    joblib.dump(clf, os.path.join(model_output.path, "model.joblib"))
    
    # 6. End Experiment Run
    aiplatform.end_run()