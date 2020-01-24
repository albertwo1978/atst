output "subnets" {
  value = azurerm_subnet.subnet["private"].id #FIXED: this is now legacy, use subnet_list
}

output "subnet_list" {
  value = {
    for k, id in azurerm_subnet.subnet : k => id
  }
}