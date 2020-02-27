module "keyvault" {
  source           = "../../modules/keyvault"
  name             = "cz"
  region           = var.region
  owner            = var.owner
  environment      = var.environment
  tenant_id        = var.tenant_id
  principal_id     = "02452eee-babc-4757-bbaf-0fd6db0588eb"
  admin_principals = var.admin_users
  policy           = "Deny"
  subnet_ids       = [module.vpc.subnets]
  whitelist        = var.admin_user_whitelist
  workspace_id     = module.logs.workspace_id
}

