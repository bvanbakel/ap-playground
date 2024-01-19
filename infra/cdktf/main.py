#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount
from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup
from cdktf_cdktf_provider_azurerm.data_factory import DataFactory, DataFactoryGithubConfiguration
from cdktf_cdktf_provider_azurerm.key_vault import KeyVault
from cdktf_cdktf_provider_azurerm.databricks_workspace import DatabricksWorkspace
from dotenv import load_dotenv
import os


class ApSettings():
    def __init__(self, environment: str):
        load_dotenv("infra/cdktf/.env")

        self.tenant_id = os.environ["ARM_TENANT_ID"]
        self.env_long = environment
        self.env_short = environment[0]
        self.prefix = "ap"
        self.project_name = "xprtlab"
        self.resource_group_name = f"{self.prefix}-{self.env_short}-{self.project_name}-rg"
        self.storage_account_name = f"{self.prefix}{self.env_short}datalakesa"
        self.data_factory_name = f"{self.prefix}-{self.env_short}-{self.project_name}-adf"
        self.key_vault_name = f"{self.prefix}-{self.env_short}-{self.project_name}-kv"
        self.databricks_workspace_name = f"{self.prefix}-{self.env_short}-{self.project_name}-adb"
        self.location = "westeurope"

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        settings = ApSettings(environment="dev")

        # define resources here
        azure_provider = AzurermProvider(
            self, 
            id                          = 'Azure',
            features                    = {}
        )

        resource_group = ResourceGroup(
            self,
            id_                         = "ap_rg",
            name                        = settings.resource_group_name,
            location                    = settings.location
        )

        storage_account = StorageAccount(
            self,
            id_                         = "ap_sa",
            name                        = settings.storage_account_name,
            resource_group_name         = resource_group.name,
            location                    = settings.location,
            account_tier                = "Standard",
            account_replication_type    = "LRS",
            is_hns_enabled              = True
        )

        data_factory = DataFactory(
            self,
            id_                         = "ap_adf",
            name                        = settings.data_factory_name,
            location                    = settings.location,
            resource_group_name         = resource_group.name,
            github_configuration        = DataFactoryGithubConfiguration(
                                            self,
                                            account_name= "bvanbakel",
                                            branch_name= "main",
                                            git_url= "https://github.com",
                                            repository_name= "ap-xprtlab-df",
                                            root_folder= "/"
                                        )
        )

        key_vault = KeyVault(
            self,
            id_                         = "ap_kv",
            tenant_id                   = settings.tenant_id,
            name                        = settings.key_vault_name,
            resource_group_name         = resource_group.name,
            location                    = settings.location,
            sku_name                    = "standard"
        )

        databricks_ws = DatabricksWorkspace(
            self,
            id_                         = "ap_adb",
            name                        = settings.databricks_workspace_name,
            location                    = settings.location,
            resource_group_name         = resource_group.name,
            sku                         = "standard"
        )

app = App()
MyStack(app, "cdktf")

app.synth()
