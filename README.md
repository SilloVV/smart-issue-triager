# MLOPS Project : Ticket Sorter using Hybric Cloud and Trunk Based Development

The idea is to sort issues ticket automatically by Machine Learning using Trunk-based Development methodologies.

Datasets used :
- Alinea, Arns Vhinzy C. (2024). Support Ticketing Data (January - July 2024). https://huggingface.co/datasets/nerofinal012/TicketingToolDataset. Hugging Face.
 trunk


Encountered Difficulties :
- Dependencies management : mlflow wanted pyarrow v22.0.0 and datasets wanted pyarrov v23.0.0 -> used 'uv tree | findstr "pyarrow' to find and unlock uv.lock to let him recalculate librairies versions .
