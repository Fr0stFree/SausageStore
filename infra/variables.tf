# Yandex.Cloud specific variables
variable "zone" {
  description = "The zone where resources will be created"
  type        = string
}

variable "cloud_id" {
  description = "The ID of the Personal Account (cloud) in Yandex.Cloud"
  type        = string
}

variable "folder_id" {
  description = "The ID of the Folder in Yandex.Cloud"
  type        = string
}

variable "service_account_key_file" {
  description = "Path to the Yandex.Cloud service account key file"
  type        = string
}


# VM specific variables
variable "vm_authorized_key" {
  description = "The public SSH key for accessing the VM"
  type        = string
}

variable "vm_username" {
  description = "The username for the VM"
  type        = string
  default     = "ubuntu"
}
