import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

BUCKET_NAME = "smart-issue-triager-storage-sillovv"
TEST_FILE_NAME = "test_connection.txt"


def test_s3():
    # 1. Initialisation du client S3
    # Boto3 utilise automatiquement les clés configurées via 'aws configure'
    s3 = boto3.client("s3")

    try:
        print(f"🔍 Test de connexion au bucket : {BUCKET_NAME}")

        # 2. Création d'un contenu de test
        content = "Connexion réussie ! Ce fichier a été généré par Boto3."

        # 3. Upload du fichier vers S3
        print("📤 Tentative d'upload...")
        s3.put_object(Bucket=BUCKET_NAME, Key=TEST_FILE_NAME, Body=content)
        print("✅ Upload réussi.")

        # 4. Vérification de l'existence du fichier
        print("📁 Vérification de la présence du fichier sur S3...")
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=TEST_FILE_NAME)

        if "Contents" in response:
            print(f"✨ Confirmation : Le fichier '{TEST_FILE_NAME}' est bien sur S3.")
        else:
            print("❌ Le fichier n'a pas été trouvé après l'upload.")

        # 5. Nettoyage (suppression du fichier de test)
        print("🧹 Nettoyage du fichier de test...")
        s3.delete_object(Bucket=BUCKET_NAME, Key=TEST_FILE_NAME)
        print("✅ Nettoyage terminé. Votre S3 est propre.")

    except NoCredentialsError:
        print(
            "❌ Erreur : Clés AWS introuvables. Lancez 'aws configure' dans votre terminal."
        )
    except PartialCredentialsError:
        print("❌ Erreur : Clés AWS incomplètes. Vérifiez votre configuration.")
    except Exception as e:
        print(f"❌ Une erreur est survenue : {e}")


if __name__ == "__main__":
    test_s3()
