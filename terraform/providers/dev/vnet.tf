module "vnet" {
  source                    = "../../modules/vnet/"
  environment               = var.environment
  region                    = var.region
  virtual_network           = var.virtual_network
  networks                  = var.networks
  routes                    = var.routes
  virtual_appliance_routes  = var.virtual_appliance_routes
  owner                     = var.owner
  name                      = var.name
  dns_servers               = var.dns_servers
  service_endpoints         = var.service_endpoints
}
