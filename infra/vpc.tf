resource "yandex_vpc_network" "sausage-network" {
  name = "sausage-network"
}

resource "yandex_vpc_subnet" "sausage-subnet" {
  name           = "sausage-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.sausage-network.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

resource "yandex_vpc_security_group" "sausage-security-group" {
  name        = "sausage-security-group"
  description = "Allow SSH and HTTP"
  network_id  = yandex_vpc_network.sausage-network.id

  egress {
    description    = "Allow all outgoing traffic"
    protocol       = "ANY"
    from_port      = 0
    to_port        = 65535
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description    = "Allow SSH"
    protocol       = "TCP"
    port           = 22
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description    = "Allow HTTP"
    protocol       = "TCP"
    port           = 8200
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
}
