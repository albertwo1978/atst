resource "azurerm_resource_group" "k8s" {
  name     = "${var.name}-${var.environment}-vpc"
  location = var.region
}

resource "azurerm_kubernetes_cluster" "k8s" {
  name                = "${var.name}-${var.environment}-k8s"
  location            = azurerm_resource_group.k8s.location
  resource_group_name = azurerm_resource_group.k8s.name
  dns_prefix          = var.k8s_dns_prefix

  service_principal {
    client_id     = "c344ac0e-e09e-4f19-8257-a3fa3d737692"
    client_secret = "262a8fcc-07d6-4929-8c74-b2df467464c8"
  }

  default_node_pool {
    name                  = "default"
    vm_size               = "Standard_D1_v2"
    os_disk_size_gb       = 30
#    availability_zones    = var.k8s_zones
    vnet_subnet_id        = var.vnet_subnet_id
#    enable_node_public_ip = true # Nodes need a public IP for external resources. FIXME: Switch to NAT Gateway if its available in our subscription
    enable_auto_scaling   = var.enable_auto_scaling
    max_count             = var.max_count # FIXME: if auto_scaling disabled, set to 0
    min_count             = var.min_count # FIXME: if auto_scaling disabled, set to 0
  }

  network_profile {
    load_balancer_sku     = "standard"
    network_plugin        = var.k8s_network_plugin
  }

  role_based_access_control {
    enabled = true
  }

  #identity {
  #  type = "SystemAssigned"
  #}

  lifecycle {
    ignore_changes = [
      default_node_pool.0.node_count
    ]
  }

  tags = {
    environment = var.environment
    owner       = var.owner
  }
}

resource "azurerm_monitor_diagnostic_setting" "k8s_diagnostic-1" {
  name                       = "${var.name}-${var.environment}-k8s-diag"
  target_resource_id         = azurerm_kubernetes_cluster.k8s.id
  log_analytics_workspace_id = var.workspace_id
  log {
    category = "kube-apiserver"
    retention_policy {
      enabled = true
    }
  }
  log {
    category = "kube-controller-manager"
    retention_policy {
      enabled = true
    }
  }
  log {
    category = "kube-scheduler"
    retention_policy {
      enabled = true
    }
  }
  log {
    category = "kube-audit"
    retention_policy {
      enabled = true
    }
  }
  log {
    category = "cluster-autoscaler"
    retention_policy {
      enabled = true
    }
  }
  metric {
    category = "AllMetrics"
    retention_policy {
      enabled = true
    }
  }
}

resource "azurerm_role_assignment" "k8s_network_contrib" {
  scope                             = var.vnet_id
  role_definition_name              = "Network Contributor"
  principal_id                      = "c344ac0e-e09e-4f19-8257-a3fa3d737692"
  skip_service_principal_aad_check  = true
}