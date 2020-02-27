data "azurerm_key_vault_secret" "k8s_client_id" {
  name         = "k8s-client-id"
  key_vault_id = module.operator_keyvault.id
}

data "azurerm_key_vault_secret" "k8s_client_secret" {
  name         = "k8s-client-secret"
  key_vault_id = module.operator_keyvault.id
}

module "k8s" {
  source              = "../../modules/k8s"
  location            = var.region
  name                = var.name
  environment         = var.environment
  owner               = var.owner
  k8s_dns_prefix      = var.k8s_dns_prefix
  k8s_node_size       = var.k8s_node_size
  k8s_network_plugin  = var.k8s_network_plugin
  vnet_id             = module.vpc.id 
  vnet_subnet_id      = module.vpc.subnets #FIXME - output from module.vpc.subnets should be map
  enable_auto_scaling = true
  max_count           = 5
  min_count           = 3
#  node_count               = 3
  client_id           = data.azurerm_key_vault_secret.k8s_client_id.value
  client_secret       = data.azurerm_key_vault_secret.k8s_client_secret.value
#  principal_object_id = "73639624-35ba-4491-b0f7-dde03b2e9435"  
  workspace_id        = module.logs.workspace_id
}


# module "k8s-arm" {
#   source                 = "../../modules/k8s-arm"
#   location               = var.region
#   name                   = var.name
#   environment            = var.environment
#   owner                  = var.owner
#   k8s_dns_prefix         = var.k8s_dns_prefix
#   k8s_node_size          = var.k8s_node_size
#   k8s_network_plugin     = var.k8s_network_plugin
#   vnet_subnet_id         = module.vpc.subnets #FIXME - output from module.vpc.subnets should be map
#   enable_auto_scaling    = true
#   enable_private_cluster = true
#   enable_rbac            = true
#   max_count              = 5
#   min_count              = 3
#   node_count             = 3

#   client_id           = data.azurerm_key_vault_secret.k8s_client_id.value
#   client_secret       = data.azurerm_key_vault_secret.k8s_client_secret.value
#   principal_object_id = "73639624-35ba-4491-b0f7-dde03b2e9435"
#   workspace_id        = "tobedone" # Need to fix this

#   service_cidr       = "10.0.0.0/16"  # Need to decide these values for advanced networking
#   dns_service_ip     = "10.0.0.10"
#   docker_bridge_cidr = "172.16.0.1/16"

# }


#module "main_lb" {
#  source      = "../../modules/lb"
#  region      = var.region
#  name        = "main-${var.name}"
#  environment = var.environment
#  owner       = var.owner
#}

#module "auth_lb" {
#  source      = "../../modules/lb"
#  region      = var.region
#  name        = "auth-${var.name}"
#  environment = var.environment
#  owner       = var.owner
#}
