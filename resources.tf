
# Generate random text for a unique storage account name
resource "random_id" "randomId" {
  keepers = {
    # Generate a new ID only when a new resource group is defined
    resource_group = azurerm_resource_group.ha_cluster.name
  }
  byte_length = 8
}

resource "azurerm_resource_group" "ha_cluster" {
  name     = var.resource_group_name
  location = var.region

  tags = {
    environment = "RHEL ha cluster"
  }
}

# Create storage account for boot diagnostics
resource "azurerm_storage_account" "mystorageaccount" {
  name                     = "${var.prefix}diag${random_id.randomId.hex}"
  resource_group_name      = azurerm_resource_group.ha_cluster.name
  location                 = var.region
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "RHEL ha cluster"
  }
}
