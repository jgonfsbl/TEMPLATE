#
# Variables
#
# Define the variables that will be used in the Terraform configuration
# These variables can be set in the terraform.tfvars file or passed in as environment variables
# The default value is used if no value is provided
#
variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "eu-south-2" # Spain
}
