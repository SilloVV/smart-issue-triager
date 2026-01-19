import json
import boto3
from moto import mock_aws


@mock_aws
def test_sqs_producer_consumer_flow():
    # 1. Setup : Créer une queue virtuelle
    sqs = boto3.client("sqs", region_name="eu-west-3")
    queue = sqs.create_queue(QueueName="test-queue")
    queue_url = queue["QueueUrl"]

    # 2. Test du Producer (Logique simplifiée)
    test_data = {"Ticket Subject": "Bug test", "Priority": "High"}
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(test_data))

    # 3. Test du Consumer (Logique simplifiée)
    response = sqs.receive_message(QueueUrl=queue_url)

    assert "Messages" in response
    message = response["Messages"][0]
    body = json.loads(message["Body"])

    assert body["Ticket Subject"] == "Bug test"
    assert body["Priority"] == "High"

    # 4. Suppression (Nettoyage virtuel)
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])
