variable "environment" {
  description = "Environment (Prod,Dev,etc)"
}

variable "region" {
  description = "Region (useast2, etc)"

}

variable "name" {
  description = "Name or prefix to use for all resources created by this module"
}

variable "owner" {
  description = "Owner of these resources"

}

variable "ddos_enabled" {
  description = "Enable or disable DDoS Protection (1,0)"
  default     = "0"
}

variable "virtual_network" {
  description = "The supernet used for this Virtual Network"
  type        = string
}

variable "networks" {
  description = "A map of lists describing the network topology"
  type        = map
}

variable "dns_servers" {
  description = "DNS Server IPs for internal and public DNS lookups (must be on a defined subnet)"
  type        = list
}

variable "routes" {
  type        = map
  description = "Routes for next hop types: VirtualNetworkGateway, VirtualNetwork, Internet and None"
}

variable "virtual_appliance_routes" {
  type        = map
  description = "Routes for next hop types: VirtualAppliance"
}

variable "service_endpoints" {
  type        = map
  description = "A map of the service endpoints and its mapping to subnets"

}
