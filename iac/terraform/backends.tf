# 
# Backends configuration file
#
# This file contains the configuration for the Terraform backends.
# The backend configuration specifies where the Terraform state file is stored.
# The backend configuration can be stored in a separate file or in the main Terraform configuration file.
#

terraform {
  backend "s3" {
    bucket         = "accountid-bucketname"
    key            = "path/to/terraform.tfstate"
    region         = "eu-south-2"
    encrypt        = true
    dynamodb_table = "dynamodb-locktable"
  }
}
