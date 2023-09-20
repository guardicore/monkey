// This file is used to create the S3 bucket and DynamoDB table to store Terraform state
// Required AWS permissions:
// - s3:CreateBucket
// - s3:PutEncryptionConfiguration
// - s3:PutBucketVersioning
// - s3:PutBucketPublicAccessBlock
// - dynamodb:CreateTable
// - dynamodb:PutItem

variable "s3_region" {
  description = "The AWS region to deploy to"
}

variable "s3_state_bucket" {
  description = "The name of the S3 bucket to store Terraform state"
}

variable "s3_state_lock_table" {
  description = "The name of the DynamoDB table to store Terraform locks"
}

provider "aws" {
  region = var.s3_region
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = var.s3_state_bucket

  # Prevent accidental deletion of this S3 bucket
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "enabled" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "default" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.terraform_state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = var.s3_state_lock_table
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
