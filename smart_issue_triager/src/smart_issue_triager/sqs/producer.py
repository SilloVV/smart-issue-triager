import boto3
import pandas as pd
import json
import io
import time

# --- Configuration ---
BUCKET_NAME = "smart-issue-triager-storage-sillovv"
S3_KEY = "datasets/customer-support/tickets.parquet"
QUEUE_NAME = "issue-triaging-queue"
REGION = "eu-west-3"  # Paris


def get_queue_url(sqs_client, queue_name):
    """Récupère l'URL de la queue à partir de son nom"""
    response = sqs_client.get_queue_url(QueueName=queue_name)
    return response["QueueUrl"]


def run_producer():
    # Initialisation des clients AWS
    s3 = boto3.client("s3", region_name=REGION)
    sqs = boto3.client("sqs", region_name=REGION)

    print("--- 🚀 Démarrage du Producer ---")

    # 1. Récupérer l'URL SQS
    try:
        queue_url = get_queue_url(sqs, QUEUE_NAME)
        print(f" Queue connectée : {queue_url}")
    except Exception:
        print(
            f" Erreur : Impossible de trouver la queue '{QUEUE_NAME}'. Vérifie le nom et la région."
        )
        return

    # 2. Lire le fichier Parquet depuis S3
    print(f" Téléchargement du dataset depuis S3 ({S3_KEY})...")
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=S3_KEY)
        # On lit le binaire directement en DataFrame Pandas
        df = pd.read_parquet(io.BytesIO(obj["Body"].read()))
        print(f" Dataset chargé : {len(df)} tickets disponibles.")
    except Exception as e:
        print(f" Erreur S3 : {e}")
        return

    # 3. Envoyer des tickets (Simulation)
    # On prend juste les 5 premiers pour tester, sinon ça va spammer ta queue !
    nb_tickets_to_send = 5
    print(f" Envoi de {nb_tickets_to_send} tickets dans la file...")

    for i in range(nb_tickets_to_send):
        # Conversion de la ligne en dictionnaire
        ticket = df.iloc[i].to_dict()

        # Transformation en JSON (default=str gère les dates si besoin)
        message_body = json.dumps(ticket, default=str)

        # Envoi à SQS
        sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)

        # Petit affichage sympa
        subject = ticket.get("Ticket Subject", "Sujet inconnu")
        print(f"    [Ticket #{i+1}] Envoyé : {subject}")

        # Petite pause pour faire réaliste (optionnel)
        time.sleep(0.5)

    print("\n✨ Terminé ! Les tickets sont en attente dans SQS.")


if __name__ == "__main__":
    run_producer()
