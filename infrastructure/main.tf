# S3 Buckets for input, output, and internal state storage
resource "aws_s3_bucket" "data_bucket" {
  bucket = var.bucket_name

  tags = {
    Name    = "${var.project}-Data"
    Project = var.project
  }
}

# EMR Cluster configuration
resource "aws_emr_cluster" "campaign_emr_cluster" {
  name          = var.emr_cluster_name
  release_label = "emr-6.3.0"
  applications  = ["Spark"]
  ec2_attributes {
    instance_profile = "EMR_EC2_DefaultRole"
    subnet_id        = "subnet-123456" # Replace with your subnet ID
  }

  master_instance_type = var.instance_type
  core_instance_type   = var.instance_type
  core_instance_count  = var.instance_count
  service_role         = "EMR_DefaultRole"

  tags = {
    Name    = "${var.project}-EMR"
    Project = var.project
  }
}

resource "aws_iam_role" "spark_job_role" {
  name = "${var.project}-spark-job-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": [
          "ec2.amazonaws.com",
          "elasticmapreduce.amazonaws.com"
        ]
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "spark_s3_access" {
  name = "${var.project}-spark-s3-access-policy"
  role = aws_iam_role.spark_job_role.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": [
        "${aws_s3_bucket.data_bucket.arn}",
        "${aws_s3_bucket.data_bucket.arn}/*"
      ],
      "Effect": "Allow"
    }
  ]
}
EOF
}
