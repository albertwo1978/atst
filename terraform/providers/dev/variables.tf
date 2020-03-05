variable "environment" {
  default = "walker"
}

variable "region" {
  default = "eastus"

}

variable "backup_region" {
  default = "westus2"
}

variable "owner" {
  default = "walker"
}

variable "name" {
  default = "east"
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
  description = "Routes for next hop types: VirtualNetworkGateway, VnetLocal, Internet or None"
  type        = map
  default = {
    # public1 = "public,firewall,52.139.8.215/32,Internet" 
    # public2 = "public,vnet,10.1.0.0/16,VnetLocal" 
    # private1 = "private,firewall,52.139.8.215/32,Internet" 
    # private2 = "private,vnet,10.1.0.0/16,VnetLocal" 
    # redis1 = "redis,firewall,52.139.8.215/32,Internet" 
    # redis2 = "redis,vnet,10.1.0.0/16,VnetLocal" 
    # apps1 = "apps,firewall,52.139.8.215/32,Internet" 
    # apps2 = "apps,vnet,10.1.0.0/16,VnetLocal" 
  }
}

variable "virtual_appliance_routes" {
  description = "Routes for next hop types VirtualAppliance"
  type        = map
  default = {
    # public1 = "public,default,0.0.0.0/0,VirtualAppliance,10.0.1.4"
    # private1 = "private,default,0.0.0.0/0,VirtualAppliance,10.0.1.4"
    # redis1 = "redis,default,0.0.0.0/0,VirtualAppliance,10.0.1.4"
    # app1 = "apps,default,0.0.0.0/0,VirtualAppliance,10.0.1.4"
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
  default = "walker"
}

variable "k8s_client_app_id" {
  type    = string
  default = "8e16a898-b96e-4bca-9a15-a67feb3753aa"
}

variable "k8s_server_app_id" {
  type    = string
  default = "cd2b0e95-27ba-4777-bf42-dcfd957d0d95"
}

variable "k8s_server_app_secret" {
  type    = string
  default = "f4d9c108-fb2f-419a-b2bf-45e8cde40bf0"
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