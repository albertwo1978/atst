provider "azurerm" {
  version = "=1.40.0"
}

provider "azuread" {
  # Whilst version is optional, we /strongly recommend/ using it to pin the version of the Provider being used
  version = "=0.7.0"
}

terraform {
  backend "azurerm" {
    resource_group_name  = "staging-walker-tfstate"
    storage_account_name = "alwstagingwalkertfstate"
    container_name       = "tfstate"
    key                  = "staging.terraform.tfstate"
  }
}
