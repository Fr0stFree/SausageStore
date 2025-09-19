terraform {
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