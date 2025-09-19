terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }

  required_version = ">= 0.13"
  backend "http" {
    address        = "https://cloud-services-engineer.gitlab.yandexcloud.net/api/v4/projects/47/terraform/state/tfstate"
    lock_address   = "https://cloud-services-engineer.gitlab.yandexcloud.net/api/v4/projects/47/terraform/state/tfstate/lock"
    unlock_address = "https://cloud-services-engineer.gitlab.yandexcloud.net/api/v4/projects/47/terraform/state/tfstate/lock"
    lock_method    = "POST"
    unlock_method  = "DELETE"
    retry_wait_min = 5
    username       = "terraform"
  }
}

provider "yandex" {
  zone                     = var.zone
  service_account_key_file = var.service_account_key_file
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
}