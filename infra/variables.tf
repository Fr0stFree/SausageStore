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
    description = "Path to the service account key file"
    type        = string
}
