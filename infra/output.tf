
output "vm-prod-ip" {
  description = "The external IP address of the production VM"
  value       = yandex_compute_instance.vm-prod.network_interface.0.nat_ip_address
}

output "vm-dev-ip" {
  description = "The external IP address of the development VM"
  value       = yandex_compute_instance.vm-dev.network_interface.0.nat_ip_address
}
