import os
import boto3
import shutil
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# ==========================================
# 🔧 CONFIGURATION AWS
# ==========================================
BUCKET_NAME = "smart-issue-triager-storage-sillovv"
MODEL_ID = "distilbert-base-uncased"
TEMP_DIR = "./temp_baseline_model"

# ==========================================
# 🛠️ FONCTIONS
# ==========================================


def get_s3_client():
    """
    Initialise le client S3.
    """
    return boto3.client("s3")


def upload_folder(s3, local_folder, bucket, s3_prefix):
    """Envoie tout un dossier vers un chemin S3 spécifique"""
    print(f" Envoi vers s3://{bucket}/{s3_prefix} ...")

    file_count = 0
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            # Calcul du chemin relatif (ex: config.json)
            relative_path = os.path.relpath(local_path, local_folder)
            # Construction de la clé S3 (ex: baseline/config.json)
            # .replace("\\", "/") est vital pour Windows
            s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")

            try:
                s3.upload_file(local_path, bucket, s3_key)
                print(f"    Uploadé : {file}")
                file_count += 1
            except Exception as e:
                print(f"    Erreur sur {file} : {e}")

    print(f" Terminé : {file_count} fichiers envoyés dans '{s3_prefix}'.")


# ==========================================
# 🚀 EXÉCUTION
# ==========================================


def main():
    s3 = get_s3_client()

    # 1. Vérification simple que le bucket existe (via ton script de test)
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
        print(f"✅ Bucket '{BUCKET_NAME}' détecté.")
    except Exception as e:
        print(
            f"❌ Impossible d'accéder au bucket '{BUCKET_NAME}'. Vérifie le nom ou tes droits."
        )
        print(f"Erreur : {e}")
        return

    # 2. Téléchargement du modèle "Vierge" (Baseline)
    print(f"\n⬇️ Téléchargement local de {MODEL_ID} (Reference)...")
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID, num_labels=3)

    model.save_pretrained(TEMP_DIR)
    tokenizer.save_pretrained(TEMP_DIR)

    # 3. Upload vers le dossier 'baseline'
    upload_folder(s3, TEMP_DIR, BUCKET_NAME, "baseline")

    print("\n🎉 Architecture prête sur AWS S3 !")
    print(f"   📂 s3://{BUCKET_NAME}/baseline/  (Référence)")


if __name__ == "__main__":
    main()
