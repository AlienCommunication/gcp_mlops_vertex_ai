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
    import os

    # 1. Load Data
    df = pd.read_csv(input_data.path)
    df = df.dropna()
    
    # Simple Encoding
    # Dropping non-numeric columns not used for training
    X = pd.get_dummies(df.drop(columns=['species', 'entity_id', 'feature_timestamp'], errors='ignore'))
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