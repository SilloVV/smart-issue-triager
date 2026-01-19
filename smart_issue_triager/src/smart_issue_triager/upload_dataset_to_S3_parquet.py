import boto3
import io
from datasets import load_dataset


def transfer_new_dataset():
    # 1. Nouveau nom du dataset
    DATASET_NAME = "gorkemsevinc/customer_support_tickets"
    BUCKET_NAME = "smart-issue-triager-storage-sillovv"

    # On change aussi le nom du dossier pour rester organisé
    S3_KEY = "datasets/customer-support/tickets.parquet"

    print(f"📥 Chargement du dataset {DATASET_NAME}...")
    try:
        # Pas besoin de token spécifique ici car c'est public
        dataset = load_dataset(DATASET_NAME, split="train")

        df = dataset.to_pandas()
        print(f"✅ Données chargées : {len(df)} lignes.")
        print(f"Colonnes disponibles : {list(df.columns)}")

        # 2. Conversion en Parquet
        print("🔄 Conversion en format Parquet...")
        parquet_buffer = io.BytesIO()
        df.to_parquet(parquet_buffer, index=False, engine="pyarrow")

        # 3. Upload vers S3
        print(f"📤 Upload vers S3 : {BUCKET_NAME}/{S3_KEY}...")
        s3 = boto3.client("s3")
        s3.put_object(Bucket=BUCKET_NAME, Key=S3_KEY, Body=parquet_buffer.getvalue())

        print("\n✨ Succès ! Le nouveau dataset est sur S3.")

    except Exception as e:
        print(f"❌ Erreur : {e}")


if __name__ == "__main__":
    transfer_new_dataset()
