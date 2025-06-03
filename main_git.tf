provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
  client_id       = var.client_id
  client_secret   = var.client_secret
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}

data "azurerm_resource_group" "existing_rg" {
  name = "Data_Domain_Predictive_Models"
}

output "dockerconfigjson_raw" {
  value = local.dockerconfigjson
}

resource "azurerm_storage_account" "rsx_storage" {
  name                     = "storagepredictivedata"
  resource_group_name      = data.azurerm_resource_group.existing_rg.name
  location                 = "North Europe"
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_storage_container" "rsx_container" {
  name                  = "telemetry-data"
  storage_account_id    = azurerm_storage_account.rsx_storage.id
  container_access_type = "private"
}

resource "null_resource" "build_and_push_docker" {
  provisioner "local-exec" {
    command = <<EOT
      cd ../..
      docker build -t railsimulator:latest .
      docker tag railsimulator:latest railsightregistry.azurecr.io/railsimulator:latest
      az acr login --name railsightregistry
      docker push railsightregistry.azurecr.io/railsimulator:latest
    EOT
  }
}

resource "null_resource" "init_blob_folders" {
  provisioner "local-exec" {
    command     = "python ./utils/blob_initializer.py"
    working_dir = "../../"
  }
}

resource "null_resource" "run_domain_simulators" {
  provisioner "local-exec" {
    command     = "python ../../simulate_domain_cli.py"
    working_dir = "../../"
  }
}

resource "null_resource" "run_blob_uploader" {
  provisioner "local-exec" {
    command     = "python ./utils/blob_uploader.py"
    working_dir = "../../"
  }
}

resource "null_resource" "apply_kubernetes_jobs" {
  provisioner "local-exec" {
    command = "kubectl apply -f ../k8s/"
  }
}

locals {
  dockerconfigjson = jsonencode({
    auths = {
      "railsightregistry.azurecr.io" = {
        username = var.acr_username
        password = var.acr_password
        email    = var.acr_email
        auth     = base64encode("${var.acr_username}:${var.acr_password}")
      }
    }
  })
}

resource "kubernetes_secret" "acr_secret" {
  metadata {
    name      = "acr-secret"
    namespace = "default"
  }

  type = "kubernetes.io/dockerconfigjson"

  data = {
    ".dockerconfigjson" = base64encode(local.dockerconfigjson)
  }
}

variable "subscription_id" {}
variable "tenant_id" {}
variable "client_id" {}
variable "client_secret" {}

variable "acr_username" {}
variable "acr_password" {}
variable "acr_email" {}

