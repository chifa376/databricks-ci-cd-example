import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def train_model():
    # Charger les mesures des fleurs et leurs espèces
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Utiliser 80 % des données pour apprendre et 20 % pour évaluer
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # Entraîner le modèle
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    )
    model.fit(X_train, y_train)

    # Évaluer ses prédictions
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, accuracy, X_test


def main():
    model, accuracy, X_test = train_model()

    # Enregistrer les résultats et le modèle dans MLflow
    with mlflow.start_run() as run:
        mlflow.log_param("n_estimators", 100)
        mlflow.log_param("random_state", 42)
        mlflow.log_metric("accuracy", accuracy)

        signature = infer_signature(
            X_test,
            model.predict(X_test),
        )

        mlflow.sklearn.log_model(
            sk_model=model,
            name="random_forest_model",
            signature=signature,
            input_example=X_test[:2],
            skops_trusted_types=["sklearn.tree._tree.Tree"],
        )

        print(f"Accuracy : {accuracy:.2%}")
        print(f"MLflow run ID : {run.info.run_id}")

        return run.info.run_id


if __name__ == "__main__":
    main()