import pytest
import json
from moto import mock_aws
import boto3
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


# --- Fixture pour simuler un modèle MLflow ---
@pytest.fixture
def mock_model():
    # On crée un modèle avec AU MOINS 2 classes différentes
    pipeline = Pipeline([("vec", CountVectorizer()), ("clf", LogisticRegression())])

    # X = les textes, y = les catégories
    X_train = ["My screen is broken", "I cannot login to my mail"]
    y_train = ["Hardware", "Access"]  # <-- On a bien 2 classes ici

    pipeline.fit(X_train, y_train)
    return pipeline


# --- Test de la logique de traitement ---
@mock_aws
def test_consumer_logic(mock_model):
    # 1. Setup : Créer une queue SQS virtuelle
    sqs = boto3.resource("sqs", region_name="eu-west-3")
    queue = sqs.create_queue(QueueName="test-queue")

    # 2. Envoyer un faux message
    test_data = {"Ticket Subject": "My screen is black", "Ticket Priority": "High"}
    queue.send_message(MessageBody=json.dumps(test_data))

    # 3. Simuler la réception (le Consumer)
    messages = queue.receive_messages()
    assert len(messages) == 1

    body = json.loads(messages[0].body)

    # 4. Vérifier la prédiction (MLflow logic)
    prediction = mock_model.predict([body["Ticket Subject"]])[0]

    assert body["Ticket Subject"] == "My screen is black"
    assert prediction == "Hardware"

    print("\n✅ Test SQS + Prédiction réussi !")
