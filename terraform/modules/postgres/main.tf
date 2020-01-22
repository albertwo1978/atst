resource "azurerm_resource_group" "sql" {
  name     = "${var.name}-${var.environment}-postgres"
  location = var.region
}

resource "azurerm_postgresql_server" "sql" {
  name                = "${var.name}-${var.environment}-sql"
  location            = azurerm_resource_group.sql.location
  resource_group_name = azurerm_resource_group.sql.name

  sku {
    name     = var.sku_name
    capacity = var.sku_capacity
    tier     = var.sku_tier
    family   = var.sku_family
  }

  storage_profile {
    storage_mb            = var.storage_mb
    backup_retention_days = var.storage_backup_retention_days
    geo_redundant_backup  = var.storage_geo_redundant_backup
    auto_grow             = var.storage_auto_grow
  }

  administrator_login          = var.administrator_login
  administrator_login_password = var.administrator_login_password
  version                      = var.postgres_version
  ssl_enforcement              = var.ssl_enforcement
}

resource "azurerm_postgresql_virtual_network_rule" "sql" {
  name                                 = "${var.name}-${var.environment}-rule"
  resource_group_name                  = azurerm_resource_group.sql.name
  server_name                          = azurerm_postgresql_server.sql.name
  subnet_id                            = var.subnet_id
  ignore_missing_vnet_service_endpoint = true
}

resource "azurerm_postgresql_database" "db" {
  name                = "${var.environment}-atat"
  resource_group_name = azurerm_resource_group.sql.name
  server_name         = azurerm_postgresql_server.sql.name
  charset             = "UTF8"
  collation           = "en_US.utf8"
}

provider "postgresql" {
  version  = "=1.4.0"
  alias    = "atat_db"
  host     = azurerm_postgresql_server.sql.fqdn
  port     = 5432
  username = "${var.administrator_login}@${azurerm_postgresql_server.sql.fqdn}"
  password = var.administrator_login_password
  sslmode  = "require"
}

resource "postgresql_role" "atat_role" {
  provider = postgresql.atat_db
  name     = var.user_login
  login    = true
  password = var.user_login_password

  depends_on = [azurerm_postgresql_server.sql]
}

resource "postgresql_grant" "atat_grant" {
  database    = azurerm_postgresql_database.db.name
  role        = var.user_login
  schema      = "public"
  object_type = "table"
  privileges  = ["ALL"]
}
