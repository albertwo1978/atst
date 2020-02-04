module "keyvault" {
  source           = "../../modules/keyvault"
  name             = "cz"
  region           = var.region
  owner            = var.owner
  environment      = var.environment
  tenant_id        = var.tenant_id
  principal_id     = "aaa48c52-f855-48fe-86d0-856d12357581"
  admin_principals = var.admin_users
  policy           = "Deny"
  subnet_ids       = [module.vpc.subnets]
  whitelist        = var.admin_user_whitelist
  workspace_id     = module.logs.workspace_id
}

