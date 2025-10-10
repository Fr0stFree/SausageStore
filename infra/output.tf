
output "vm_dev_address" {
  description = "The external IP address of the development VM"
  value       = yandex_compute_instance.vm-dev.network_interface.0.nat_ip_address
}

output "vm_dev_name" {
  description = "The name of the development VM"
  value       = yandex_compute_instance.vm-dev.name
}

output "vm_dev_user" {
  description = "Username of the development VM"
  value       = var.vm_username
}

output "vm_prod_user" {
  description = "Username of the production VM"
  value       = var.vm_username
}

output "vm_prod_address" {
  description = "The external IP address of the production VM"
  value       = yandex_compute_instance.vm-prod.network_interface.0.nat_ip_address
}

output "vm_prod_name" {
  description = "The name of the production VM"
  value       = yandex_compute_instance.vm-prod.name
}
