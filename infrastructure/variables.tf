variable "project" {
  description = "Project name used for resource tagging"
  default     = "CampaignDataProcessing"
}

variable "bucket_name" {
  description = "S3 bucket name for storing input and output data"
  type        = string
  default     = "campaign-crm-bucket"
}

variable "emr_cluster_name" {
  description = "Name of the EMR cluster"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type for EMR cluster nodes"
  default     = "m5.xlarge"
}

variable "instance_count" {
  description = "Number of EC2 instances for the EMR cluster"
  default     = 3
}
