# CI/CD for Data Science with Databricks

Projet réalisé avec GitHub Actions, Databricks, MLflow et Pytest.

## Objectif

Automatiser les tests, la mise à jour du code dans Databricks,
l’entraînement d’un modèle et son enregistrement dans MLflow Model Registry.

## Modèle

- Dataset : Iris.
- Algorithme : Random Forest, 100 arbres.
- Découpage : 80 % entraînement, 20 % test, stratifié.
- random_state : 42.
- Accuracy observée : 90 %.

## Organisation

- notebooks/train_model.py : entraînement et suivi MLflow.
- notebooks/run_training : notebook d’exécution Databricks.
- tests/test_train_model.py : tests unitaires.
- requirements.txt : dépendances Python.
- .github/workflows/ci_cd_pipeline.yml : pipeline CI/CD.

## Tests locaux

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest tests/ -v
```

Deux tests vérifient le seuil de précision et la validité des prédictions.

## Pipeline CI/CD

À chaque push sur main, GitHub Actions :

1. Récupère le code et installe les dépendances.
2. Exécute les tests unitaires.
3. Met à jour le dossier Git Databricks depuis main.
4. Lance le job d’entraînement et attend sa fin.
5. Le notebook enregistre une nouvelle version du modèle dans Unity Catalog.

La mise à jour du dossier Git remplace l’import manuel des notebooks.

## Configuration

Secrets GitHub Actions nécessaires :

- DATABRICKS_HOST : URL du workspace.
- DATABRICKS_TOKEN : token Databricks.

Le job, le dossier Git et l’authentification GitHub doivent être
configurés dans Databricks avant d’exécuter le pipeline.

- Job : iris-training-ci-cd.
- Job ID : 421411543873570.
- Modèle : workspace.default.irisrfmodel.
- Dépendances du notebook : mlflow==3.18.0 et scikit-learn==1.7.2.

Ne jamais enregistrer les tokens dans le code.

## Validation

- Tests locaux : 2 passed.
- Entraînement local avec suivi MLflow réussi.
- Dépôt GitHub connecté à Databricks.
- Job Databricks exécuté avec succès.
- Pipeline GitHub Actions exécuté avec succès.
- Plusieurs versions du modèle visibles dans Unity Catalog.

## Model Serving

La version 10 du modèle workspace.default.irisrfmodel est déployée
sur l’endpoint iris-rf-endpoint, avec un calcul CPU et Scale to zero activé.

Une requête contenant les mesures de trois fleurs a été envoyée
depuis l’interface Query endpoint.

Réponse obtenue : {"predictions": [0, 1, 2]}, correspondant
respectivement à Setosa, Versicolor et Virginica.

L’endpoint sert la version 10. Les nouvelles versions enregistrées
par le pipeline ne remplacent pas automatiquement cette version servie.

## Limites

Le pipeline entraîne et enregistre le modèle.
Aucun endpoint Model Serving n’a été configuré :
cette partie est facultative dans l’énoncé.

## Nettoyage

Après la démonstration et l’évaluation :

- arrêter les ressources de calcul classiques éventuellement actives ;
- arrêter le serveur MLflow local avec Ctrl+C ;
- désactiver le workflow si aucune nouvelle exécution n’est souhaitée ;
- révoquer les tokens dédiés au TP lorsqu’ils ne sont plus nécessaires.
