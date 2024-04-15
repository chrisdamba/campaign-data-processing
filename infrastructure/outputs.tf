output "s3_bucket_arn" {
  value       = aws_s3_bucket.data_bucket.arn
  description = "ARN of the S3 bucket"
}

output "emr_cluster_id" {
  value       = aws_emr_cluster.campaign_emr_cluster.id
  description = "ID of the EMR cluster"
}
