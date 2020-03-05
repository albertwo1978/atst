module "keyvault" {
  source           = "../../modules/keyvault"
  name             = "cz"
  region           = var.region
  owner            = var.owner
  environment      = var.environment
  tenant_id        = var.tenant_id
  principal_id     = ""
  admin_principals = var.admin_users
  policy           = "Deny"
  subnet_ids       = [module.vnet.subnets]
  whitelist        = var.admin_user_whitelist
  workspace_id     = module.logs.workspace_id
}

