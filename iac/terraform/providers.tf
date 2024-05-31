#
# Providers configuration
#
# Define the provider configuration for the AWS provider
# The region is set to the value of the aws_region variable
# The region can be overridden by setting the AWS_REGION environment variable
#

terraform {
  required_providers {

    aws = {
      source  = "hashicorp/aws"
      version = "5.52.0"
    }

    null = {
      source  = "hashicorp/null"
      version = "3.2.2"
    }

  }
}

provider "aws" {
  region = var.aws_region
}
