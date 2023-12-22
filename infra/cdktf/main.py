#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount
from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # define resources here
        AzurermProvider(
            self, 
            id          = 'Azure',
            features    = {}
        )

        ResourceGroup(
            self,
            id_          = "test_rg",
            name        = "test-rg",
            location    = "westeurope",
        )

        StorageAccount(
            self,
            id_                         = "test_sa",
            name                        = "testcdktfsa",
            resource_group_name         = "test-rg",
            location                    = "westeurope",
            account_tier                = "Standard",
            account_replication_type    = "LRS",
            is_hns_enabled              = True,
        )

app = App()
MyStack(app, "cdktf")

app.synth()
