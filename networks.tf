

module "ha_network" {
  source         = "./modules/ha_network"
  network_name   = "ha_network"
  region         = var.region
  resource_group = azurerm_resource_group.ha_cluster.name
  localip        = var.localip
  cidr           = "10.0.1.0/24"
  cidr_bits      = var.cidr_bits
}

#resource "azurerm_route_table" "cluster_udrs" {
#  name                          = "cluster_routes_udr"
#  location                      = azurerm_resource_group.ha_cluster.location
#  resource_group_name           = azurerm_resource_group.ha_cluster.name
#  disable_bgp_route_propagation = false
#
#  route {
#    name           = "internet_access"
#    address_prefix = "0.0.0.0"
#    next_hop_type  = "Internet"
#  }
#}

#resource "azurerm_subnet_route_table_association" "udr_assoc" {
#  subnet_id       = module.ha_network.subnets_ids[0].id
#  route_table_id  = azurerm_route_table.cluster_udrs.id
#}

