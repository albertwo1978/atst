variable "environment" {
  default = "e2e2"
}

variable "region" {
  default = "canadacentral"

}

variable "backup_region" {
  default = "westus2"
}

variable "owner" {
  default = "e2e2"
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
    apps    = "10.1.4.0/24,private" # Apps
  }
}

variable "service_endpoints" {
  type = map
  default = {
    public  = "Microsoft.ContainerRegistry" # Not necessary but added to avoid infinite state loop
    private = "Microsoft.Storage,Microsoft.KeyVault,Microsoft.ContainerRegistry,Microsoft.Sql"
    redis   = "Microsoft.Storage,Microsoft.Sql" # FIXME: There is no Microsoft.Redis
    apps    = "Microsoft.Storage,Microsoft.KeyVault,Microsoft.ContainerRegistry,Microsoft.Sql"
  }
}

variable "routes" {
  description = "Routes for next hop types: VirtualNetworkGateway, VirtualNetwork, Internet and None"
  type        = map
  default = {
    private1 = "private,firewall,52.139.8.215/32,Internet" 
  }
}

variable "virtual_appliance_routes" {
  description = "Routes for next hop types VirtualAppliance"
  type        = map
  default = {
    private1 = "private,default,0.0.0.0/0,VirtualAppliance,10.0.1.4"
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

variable "k8s_zones" {
  type    = list(string)
  default = ["1", "2"]
}

variable "k8s_dns_prefix" {
  type    = string
  default = "atat"
}

variable "tenant_id" {
  type    = string
  default = "72f988bf-86f1-41af-91ab-2d7cd011db47"
}

variable "admin_users" {
  type = map
  default = {
    "Albert Wolchesky"      = "ec452237-8913-48c1-8b7d-ed60599eef32"
  }
}

variable "admin_user_whitelist" {
  type = map
  default = {
    "Albert Wolchesky"           = "75.27.237.179/32"
  }
}

variable "storage_admin_whitelist" {
  type = map
  default = {
    "Albert Wolchesky"           = "75.27.237.179"
  }
}

variable "vpn_client_cidr" {
  type    = list
  default = ["172.16.255.0/24"]
}