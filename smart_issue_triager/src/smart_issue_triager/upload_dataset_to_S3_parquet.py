import boto3
import io
from datasets import load_dataset


def create_parquet_and_upload():
    # 1. Configuration des noms
    DATASET_NAME = "nerofinal012/TicketingToolDataset"
    BUCKET_NAME = "smart-issue-triager-storage-sillovv"

    # On crée le "sous-dossier" en l'incluant dans le nom du fichier (Key)
    S3_KEY = "datasets/ticketing-tool/jan_jul_2024.parquet"

    print("📥 Chargement du dataset depuis Hugging Face...")
    try:
        # On charge le dataset (pense à avoir fait 'huggingface-cli login' avant)
        dataset = load_dataset(DATASET_NAME, split="train")

        # 2. Conversion en DataFrame Pandas
        df = dataset.to_pandas()
        print(f"✅ Données chargées : {len(df)} lignes.")

        # 3. Transformation en Parquet en mémoire (RAM)
        print("🔄 Conversion en format Parquet...")
        parquet_buffer = io.BytesIO()
        df.to_parquet(parquet_buffer, index=False, engine="pyarrow")

        # 4. Connexion à S3 et Upload
        print(f"📤 Upload vers S3 : {BUCKET_NAME}/{S3_KEY}...")
        s3 = boto3.client("s3")

        # .getvalue() récupère les octets du fichier Parquet
        s3.put_object(Bucket=BUCKET_NAME, Key=S3_KEY, Body=parquet_buffer.getvalue())

        print("\n✨ Succès !")
        print(f"Le fichier est disponible ici : s3://{BUCKET_NAME}/{S3_KEY}")

    except Exception as e:
        print(f"❌ Erreur : {e}")


if __name__ == "__main__":
    create_parquet_and_upload()
