Système de Messagerie SQS (Producer & Consumer)
Ce module gère le flux de données entre notre Data Lake (S3) et le moteur de traitement (IA) via une file d'attente AWS SQS.

🏗️ Architecture du flux
Producer : Lit le dataset Parquet sur S3 et injecte les tickets dans la file SQS.

SQS Queue : Stocke temporairement les tickets de manière persistante.

Consumer : Récupère les tickets, les traite (IA), puis les supprime de la file.
