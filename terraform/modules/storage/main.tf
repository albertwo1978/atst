resource "azurerm_resource_group" "storage" {
  name     = "${var.name}-${var.environment}-${var.service_name}"
  location = var.region
}

resource "azurerm_storage_account" "storage" {
  name                     = var.service_name
  resource_group_name      = azurerm_resource_group.storage.name
  location                 = azurerm_resource_group.storage.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_account_network_rules" "acls" {
  resource_group_name  = azurerm_resource_group.storage.name
  storage_account_name = azurerm_storage_account.storage.name

  default_action = var.policy

  # Azure Storage CIDR ACLs do not accept /32 CIDR ranges.
  ip_rules = [
    for cidr in values(var.whitelist) : cidr
  ]
  virtual_network_subnet_ids = var.subnet_ids
  bypass                     = ["AzureServices"]
}

resource "azurerm_storage_container" "storage" {
  name                  = "content"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = var.container_access_type
}

# Added until requisite TF bugs are fixed. Typically this would be configured in the 
# storage_account resource
resource "null_resource" "retention" {
  provisioner "local-exec" {
    command = "az storage logging update --account-name ${azurerm_storage_account.storage.name} --log rwd --services bqt --retention 90"
  }
}