module "keyvault" {
  source           = "../../modules/keyvault"
  name             = "cz"
  region           = var.region
  owner            = var.owner
  environment      = var.environment
  tenant_id        = var.tenant_id
  principal_id     = "f998e5d1-df0f-4679-a878-d1799b6e1886"
  admin_principals = var.admin_users
  policy           = "Deny"
  subnet_ids       = [module.vnet.subnets]
  whitelist        = var.admin_user_whitelist
  workspace_id     = module.logs.workspace_id
}

