## Machine Learning Part
- Fine tuning of a distillbeert model using LoRa (Parameter-Efficient Fine-tunig)
- monitor training on MLFlow

Fine tuning  using LoRa :
-> in_features = 768 : from 768x768 = 589 824 features  parameters to (768x16) + (16x768) = 24,576  -> rank = 16
->  classifier -> Sequence classification -> taskType.Seq_CLS
