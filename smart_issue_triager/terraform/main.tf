# Création du Bucket S3
resource "aws_s3_bucket" "issue_storage" {
  bucket = "smart-issue-triager-storage-sillovv" # Doit être unique au monde
}

# Création de la file SQS avec le Visibility Timeout de 30s
resource "aws_sqs_queue" "issue_queue" {
  name                        = "issue-triaging-queue"
  visibility_timeout_seconds  = 30  
  delay_seconds               = 0
  max_message_size            = 262144
  message_retention_seconds   = 86400 # 1 jour
  receive_wait_time_seconds   = 10    # Long polling pour réduire les coûts
}

# Outputs pour récupérer les informations dans ton code Python
output "s3_bucket_name" {
  value = aws_s3_bucket.issue_storage.id
}

output "sqs_queue_url" {
  value = aws_sqs_queue.issue_queue.id
}