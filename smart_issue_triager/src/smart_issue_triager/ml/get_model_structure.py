from transformers import AutoModelForSequenceClassification

# Charger le modèle de base
model_id = "distilbert-base-uncased"
model = AutoModelForSequenceClassification.from_pretrained(model_id)

# Afficher la structure
print(model)
