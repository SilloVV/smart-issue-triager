import os
import boto3

# Config
BUCKET_NAME = "smart-issue-triager-storage-sillovv"
TEMP_DIR = "./temp_fine_tuned_model"  # (Sera utilisé plus tard pour l'entrainement)

# utils


def get_client():
    """Get AWS S3 Client"""
    # Boto3 va chercher tes credentials AWS automatiquement
    return boto3.client("s3")


def create_s3_folder_placeholder(s3, bucket, folder_path):
    """
    Simule la création d'un dossier sur S3 en y plaçant un fichier README.
    S3 ne gère pas les vrais dossiers vides, il faut un objet dedans.
    """
    print(f" Création du dossier virtuel : s3://{bucket}/{folder_path}")

    # 1. Création d'un fichier temporaire local
    readme_name = "README.txt"
    with open(readme_name, "w", encoding="utf-8") as f:
        f.write(f"Ce dossier '{folder_path}' est réservé pour le modèle finetuned.\n")
        f.write(
            "Les fichiers (model.safetensors, config.json) seront uploadés ici après l'entraînement."
        )

    # 2. Construction de la clé S3 (ex: finetuned/README.txt)
    # On s'assure que folder_path ne commence ni ne finit par des slashs inutiles pour la concaténation
    clean_folder = folder_path.strip("/")
    s3_key = f"{clean_folder}/{readme_name}"

    try:
        # 3. Upload du fichier
        s3.upload_file(readme_name, bucket, s3_key)
        print(f" Dossier '{folder_path}' créé avec succès (via {s3_key}).")
    except Exception as e:
        print(f" Erreur lors de la création du dossier : {e}")
    finally:
        # 4. Nettoyage local
        if os.path.exists(readme_name):
            os.remove(readme_name)


# --- EXÉCUTION ---

if __name__ == "__main__":
    # 1. Connexion
    s3 = get_client()

    # 2. Création du dossier vide pour le futur modèle
    create_s3_folder_placeholder(s3, BUCKET_NAME, "finetuned")

    # (Optionnel) Tu peux aussi créer le dossier baseline si tu veux la structure complète
    # create_s3_folder_placeholder(s3, BUCKET_NAME, "baseline")

    print("\n Structure S3 prête. .")
