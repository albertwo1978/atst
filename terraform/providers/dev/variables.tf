variable "environment" {
  default = "gato"
}

variable "region" {
  default = "eastus"

}

variable "backup_region" {
  default = "westus2"
}

variable "owner" {
  default = "gato"
}

variable "name" {
  default = "staging"
}

variable "virtual_network" {
  type    = string
  default = "10.1.0.0/16"
}

variable "networks" {
  type = map
  default = {
    #format
    #name         = "CIDR, route table, Security Group Name"
    public  = "10.1.1.0/24,public"  # LBs
    private = "10.1.2.0/24,private" # k8s, postgres, keyvault
    redis   = "10.1.3.0/24,private" # Redis
  }
}

variable "service_endpoints" {
  type = map
  default = {
    public  = "Microsoft.ContainerRegistry" # Not necessary but added to avoid infinite state loop
    private = "Microsoft.Storage,Microsoft.KeyVault,Microsoft.ContainerRegistry,Microsoft.Sql"
    redis   = "Microsoft.Storage,Microsoft.Sql" # FIXME: There is no Microsoft.Redis
  }
}

variable "gateway_subnet" {
  type    = string
  default = "10.1.20.0/24"
}

variable "route_tables" {
  description = "Route tables and their default routes"
  type        = map
  default = {
    public  = "Internet"
    private = "Internet"
    redis   = "VnetLocal"
    #private = "VnetLocal"
  }
}

variable "dns_servers" {
  type    = list
  default = []
}

variable "k8s_node_size" {
  type    = string
  default = "Standard_A1_v2"
}

variable "k8s_network_plugin" {
  type    = string
  default = "azure"
}

variable "k8s_network_policy" {
  type    = string
  default = "azure"
}

variable "k8s_zones" {
  type    = list(string)
  default = ["1", "2", "3"]
}

variable "k8s_dns_prefix" {
  type    = string
  default = "atat"
}

variable "tenant_id" {
  type    = string
  default = "802690d9-449e-4e9d-b89b-a2519fb4e743"
}

variable "admin_users" {
  type = map
  default = {
    "Albert Wolchesky"      = "bdf1178b-4518-4015-ac70-94eb7a5ebdd4"
  }
}

variable "admin_user_whitelist" {
  type = map
  default = {
    "Albert Wolchesky"           = "216.243.17.14/32"
  }
}

variable "storage_admin_whitelist" {
  type = map
  default = {
    "Albert Wolchesky"           = "216.243.17.14"
  }
}

variable "vpn_client_cidr" {
  type    = list
  default = ["172.16.255.0/24"]
}
