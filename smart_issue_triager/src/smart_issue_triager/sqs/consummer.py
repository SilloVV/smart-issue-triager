import boto3
import json
import time
from botocore.exceptions import ClientError

# --- Configuration ---
QUEUE_NAME = "issue-triaging-queue"
REGION = "eu-west-3"


def get_queue_url(sqs_client, name):
    """Récupère l'URL de la queue à partir de son nom"""
    try:
        response = sqs_client.get_queue_url(QueueName=name)
        return response["QueueUrl"]
    except ClientError as e:
        print(f" Erreur : Impossible de trouver la file '{name}'.")
        raise e


def run_consumer():
    # Initialisation du client SQS
    sqs = boto3.client("sqs", region_name=REGION)

    # 1. Récupération dynamique de l'URL
    try:
        queue_url = get_queue_url(sqs, QUEUE_NAME)
        print(f" Connexion réussie à : {queue_url}")
    except Exception:
        return

    print(" En attente de tickets... (Ctrl+C pour arrêter)")

    while True:
        # 2. Réception des messages (Long Polling)
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,  # Attend 10s pour réduire les appels API inutilement
        )

        if "Messages" in response:
            for msg in response["Messages"]:
                # Extraction des données
                ticket_data = json.loads(msg["Body"])

                print("\n [TICKET REÇU]")
                print(f"   Sujet : {ticket_data.get('Ticket Subject')}")
                print(f"   Type  : {ticket_data.get('Ticket Type')}")

                # 3. Suppression du message après "traitement"
                sqs.delete_message(
                    QueueUrl=queue_url, ReceiptHandle=msg["ReceiptHandle"]
                )
                print("🗑️ Message traité et supprimé.")
        else:
            print("... file vide ...")
            time.sleep(1)


if __name__ == "__main__":
    try:
        run_consumer()
    except KeyboardInterrupt:
        print("\n Arrêt du consumer.")
