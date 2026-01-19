import mlflow
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
)
from peft import LoraConfig, get_peft_model, TaskType

# 1. Données de test (On reste simple pour valider le stack)
data = {
    "text": [
        "My screen is flickering",
        "Blue screen of death on laptop",
        "Forgot my Windows password",
        "Need to reset my MFA",
        "VPN connection is dropping",
        "Cannot access the wifi",
    ],
    "label": [0, 0, 1, 1, 2, 2],  # 0: Hardware, 1: Access, 2: Network
}
dataset = Dataset.from_pandas(pd.DataFrame(data))

# 2. Préparation du Modèle & Tokenizer
model_id = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_id)


def tokenize_function(examples):
    return tokenizer(
        examples["text"], padding="max_length", truncation=True, max_length=128
    )


tokenized_ds = dataset.map(tokenize_function, batched=True)

# 3. Configuration LoRA (Tes paramètres)
lora_config = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    r=16,  # Ton choix de rang
    lora_alpha=32,  # Scaling factor (2 * r)
    target_modules=["q_lin", "v_lin"],  # Ciblage des couches d'attention
    lora_dropout=0.1,
    bias="none",
)

# Charger le modèle de base pour 3 catégories
base_model = AutoModelForSequenceClassification.from_pretrained(model_id, num_labels=3)
# Injecter les adaptateurs LoRA
model = get_peft_model(base_model, lora_config)
model.print_trainable_parameters()  # Pour voir le % de paramètres entraînés

# 4. Configuration MLflow & Trainer
mlflow.set_experiment("LoRA_DistilBERT_Triage")

training_args = TrainingArguments(
    output_dir="./lora_results",
    learning_rate=2e-4,  # Un peu plus haut que d'habitude car LoRA est robuste
    per_device_train_batch_size=2,
    num_train_epochs=20,
    weight_decay=0.01,
    logging_steps=1,
    report_to="none",  # Liaison automatique avec MLflow
    push_to_hub=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_ds,
)

# 5. Lancement de l'entraînement
with mlflow.start_run() as run:
    trainer.train()
    # Sauvegarde locale (Méthode la plus sûre)
save_path = "./mon_super_adaptateur"

print(f"💾 Sauvegarde de l'adaptateur LoRA dans {save_path}...")
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print("✅ Sauvegarde réussie ! Tu peux maintenant tester ton modèle.")
print(f" Entraînement terminé ! Run ID: {run.info.run_id}")
