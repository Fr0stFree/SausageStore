resource "yandex_vpc_network" "sausage-network" {
  name = "sausage-network"
}

resource "yandex_vpc_address" "sausage-static-ip" {
  name = "sausage-static-ip"
  external_ipv4_address {
    zone_id = var.zone
  }
}