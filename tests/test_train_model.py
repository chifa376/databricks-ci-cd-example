from notebooks.train_model import train_model


def test_model_accuracy():
    model, accuracy, X_test = train_model()

    # Vérifier que le modèle reconnaît au moins 90 % des fleurs de test
    assert accuracy >= 0.90


def test_model_predictions():
    model, accuracy, X_test = train_model()

    predictions = model.predict(X_test)

    # Une prédiction pour chaque fleur
    assert len(predictions) == len(X_test)

    # Les prédictions correspondent aux trois espèces possibles
    assert set(predictions).issubset({0, 1, 2})