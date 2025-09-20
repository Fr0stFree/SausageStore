resource "yandex_compute_instance" "vm-prod" {
  name        = "vm-prod"
  description = "VM for production"
  zone        = var.zone
  platform_id = "standard-v3"

  resources {
    cores         = 2
    memory        = 2
    core_fraction = 50
  }

  boot_disk {
    initialize_params {
      image_id = "fd8vmcue7aajpmeo39kk" # ubuntu 20-04
      size     = 20
      type     = "network-hdd"
    }
  }

  network_interface {
    subnet_id          = yandex_vpc_subnet.sausage-subnet.id
    nat                = true
    security_group_ids = [yandex_vpc_security_group.sausage-security-group.id]
  }

  metadata = {
    ssh-keys = "${var.vm_username}:${var.vm_authorized_key}"
    user-data = templatefile("${path.module}/templates/cloud-init.yaml.tmpl", {
      authorized_key = var.vm_authorized_key
      user           = var.vm_username
    })
  }

  depends_on = [
    yandex_vpc_network.sausage-network,
    yandex_vpc_subnet.sausage-subnet,
    yandex_vpc_security_group.sausage-security-group,
  ]
}
