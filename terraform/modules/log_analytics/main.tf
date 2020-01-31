resource "azurerm_resource_group" "log_workspace" {
  name     = "${var.name}-${var.environment}-log-workspace"
  location = var.region
}

resource "azurerm_log_analytics_workspace" "log_workspace" {
  name                = "${var.name}-${var.environment}-log-workspace"
  location            = azurerm_resource_group.log_workspace.location
  resource_group_name = azurerm_resource_group.log_workspace.name
  sku                 = "Premium"
  tags = {
    environment = var.environment
    owner       = var.owner
  }
}
