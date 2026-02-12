# Azure SFTP Container ARM Template 新增使用者

> **原文發布日期:** 2023-10-24
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/10/24/Azure-SFTP-Container-ARM-Template
> **標籤:** 無

---

發財啦，終於從兩個使用者變成四個使用者了！

結論

聲明式，即使建過 Storage，下一版範本也還是要保留 Storage 的聲明

更新

```
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "containerGroupDNSLabel": {
            "defaultValue": "my-sftp",
            "type": "String",
            "metadata": {
                "description": "既有容器 DNS Label"
            }
        },
        "containerIP": {
            "defaultValue": "201.247.244.37",
            "type": "String",
            "metadata": {
                "description": "既有容器 IP"
            }
        },
        "storageAccountName": {
            "defaultValue": "sftpstgqvzlilkzsngya",
            "type": "String",
            "metadata": {
                "description": "既有儲存體帳號名稱"
            }
        },
        "storageAccountType": {
            "type": "string",
            "defaultValue": "Standard_LRS",
            "allowedValues": [
                "Standard_LRS",
                "Standard_GRS",
                "Premium_LRS"
            ],
            "metadata": {
                "description": "既有 Storage account type"
            }
        },
        "fileShareAccessTier": {
            "type": "string",
            "defaultValue": "Hot",
                "allowedValues": [
                "Hot",
                "Cool",
                "TransactionOptimized"
            ],
            "metadata": {
                "description": "既有 File Share Access Tier to be created"
            }
        },
        "location": {
            "type": "string",
            "defaultValue": "[resourceGroup().location]",
            "metadata": {
                "description": "既有 Primary location for resources"
            }
        },
        "sftpUser1": {
            "type": "string",
            "defaultValue": "jakeuj01",
            "metadata": {
                "description": "既有帳號1"
            }
        },
        "sftpPassword1": {
            "type": "securestring",
            "defaultValue": "Aa1plkmnbfg",
            "metadata": {
                "description": "既有密碼1"
            }
        },
        "sftpUser2": {
            "type": "string",
            "defaultValue": "jakeuj02",
            "metadata": {
                "description": "既有帳號2"
            }
        },
        "sftpPassword2": {
            "type": "securestring",
            "defaultValue": "Aa1plkmnbfg",
            "metadata": {
                "description": "既有密碼2"
            }
        },
        "sftpUser3": {
            "type": "string",
            "defaultValue": "jakeuj03",
            "metadata": {
                "description": "Usernames to be used for SFTP access in lower case"
            }
        },
        "sftpPassword3": {
            "type": "securestring",
            "defaultValue": "Aa1plkmnbfg",
            "metadata": {
                "description": "Password for the first user to use for SFTP access"
            }
        },
        "sftpUser4": {
            "type": "string",
            "defaultValue": "jakeuj04",
            "metadata": {
                "description": "Usernames to be used for SFTP access in lower case"
            }
        },
        "sftpPassword4": {
            "type": "securestring",
            "defaultValue": "Aa1plkmnbfg",
            "metadata": {
                "description": "Password for the second user to use for SFTP access"
            }
        },
        "sftpUser5": {
            "type": "string",
            "defaultValue": "jakeuj05",
            "metadata": {
                "description": "Usernames to be used for SFTP access in lower case"
            }
        },
        "sftpPassword5": {
            "type": "securestring",
            "defaultValue": "Aa1plkmnbfg",
            "metadata": {
                "description": "Password for the user 3 to use for SFTP access"
            }
        }
    },
    "variables": {
        "sftpContainerName": "sftp",
        "sftpContainerGroupName": "sftp-group",
        "storageKind": "StorageV2",
        "storageAccessTier": "Hot",
        "supportsHttpsTrafficOnly": true,
        "sftpEnvVariable": "[concat(parameters('sftpUser1'), ':', parameters('sftpPassword1'), ' ', parameters('sftpUser2'), ':', parameters('sftpPassword2'), ' ', parameters('sftpUser3'), ':', parameters('sftpPassword3'), ' ', parameters('sftpUser4'), ':', parameters('sftpPassword4'), ' ', parameters('sftpUser5'), ':', parameters('sftpPassword5'))]"
    },
    "resources": [
        {
            "type": "Microsoft.Storage/storageAccounts",
            "name": "[parameters('storageAccountName')]",
            "apiVersion": "2019-06-01",
            "location": "[parameters('location')]",
            "sku": {
                "name": "[parameters('storageAccountType')]"
            },
            "kind": "[variables('storageKind')]",
            "properties": {
                "accessTier": "[variables('storageAccessTier')]",
                "supportsHttpsTrafficOnly": "[variables('supportsHttpsTrafficOnly')]"
            }
        },
        {
            "type": "Microsoft.Storage/storageAccounts/fileServices/shares",
            "apiVersion": "2019-06-01",
            "name": "[concat(parameters('storageAccountName'), '/default/', parameters('sftpUser1'))]",
            "dependsOn": [
                "[parameters('storageAccountName')]"
            ],
            "properties": {
                "accessTier": "[parameters('fileShareAccessTier')]"
            }
        },
        {
            "type": "Microsoft.Storage/storageAccounts/fileServices/shares",
            "apiVersion": "2019-06-01",
            "name": "[concat(parameters('storageAccountName'), '/default/', parameters('sftpUser2'))]",
            "dependsOn": [
                "[parameters('storageAccountName')]"
            ],
            "properties": {
                "accessTier": "[parameters('fileShareAccessTier')]"
            }
        },
        {
            "type": "Microsoft.Storage/storageAccounts/fileServices/shares",
            "apiVersion": "2019-06-01",
            "name": "[concat(parameters('storageAccountName'), '/default/', parameters('sftpUser3'))]",
            "dependsOn": [
                "[parameters('storageAccountName')]"
            ],
            "properties": {
                "accessTier": "[parameters('fileShareAccessTier')]"
            }
        },
        {
            "type": "Microsoft.Storage/storageAccounts/fileServices/shares",
            "apiVersion": "2019-06-01",
            "name": "[concat(parameters('storageAccountName'), '/default/', parameters('sftpUser4'))]",
            "dependsOn": [
                "[parameters('storageAccountName')]"
            ],
            "properties": {
                "accessTier": "[parameters('fileShareAccessTier')]"
            }
        },
        {
            "type": "Microsoft.Storage/storageAccounts/fileServices/shares",
            "apiVersion": "2019-06-01",
            "name": "[concat(parameters('storageAccountName'), '/default/', parameters('sftpUser5'))]",
            "dependsOn": [
                "[parameters('storageAccountName')]"
            ],
            "properties": {
                "accessTier": "[parameters('fileShareAccessTier')]"
            }
        },
        {
            "type": "Microsoft.ContainerInstance/containerGroups",
            "apiVersion": "2023-05-01",
            "name": "[variables('sftpContainerGroupName')]",
            "location": "southeastasia",
            "dependsOn": [
                "[resourceId('Microsoft.Storage/storageAccounts/fileServices/shares', parameters('storageAccountName'), 'default', parameters('sftpUser1'))]",
                "[resourceId('Microsoft.Storage/storageAccounts/fileServices/shares', parameters('storageAccountName'), 'default', parameters('sftpUser2'))]",
                "[resourceId('Microsoft.Storage/storageAccounts/fileServices/shares', parameters('storageAccountName'), 'default', parameters('sftpUser3'))]",
                "[resourceId('Microsoft.Storage/storageAccounts/fileServices/shares', parameters('storageAccountName'), 'default', parameters('sftpUser4'))]",
                "[resourceId('Microsoft.Storage/storageAccounts/fileServices/shares', parameters('storageAccountName'), 'default', parameters('sftpUser5'))]"
            ],
            "properties": {
                "sku": "Standard",
                "containers": [
                    {
                        "name": "[variables('sftpContainerName')]",
                        "properties": {
                            "image": "atmoz/sftp:latest",
                            "ports": [
                                {
                                    "port": 22
                                }
                            ],
                            "environmentVariables": [
                                {
                                    "name": "SFTP_USERS",
                                    "secureValue": "[variables('sftpEnvVariable')]"
                                }
                            ],
                            "resources": {
                                "requests": {
                                    "memoryInGB": 1,
                                    "cpu": 2
                                }
                            },
                            "volumeMounts": [
                                {
                                    "mountPath": "[concat('/home/', parameters('sftpUser1'), '/', parameters('sftpUser1'))]",
                                    "name": "[parameters('sftpUser1')]",
                                    "readOnly": false
                                },
                                {
                                    "mountPath": "[concat('/home/', parameters('sftpUser2'), '/', parameters('sftpUser2'))]",
                                    "name": "[parameters('sftpUser2')]",
                                    "readOnly": false
                                },
                                {
                                    "mountPath": "[concat('/home/', parameters('sftpUser3'), '/', parameters('sftpUser3'))]",
                                    "name": "[parameters('sftpUser3')]",
                                    "readOnly": false
                                } ,
                                {
                                    "mountPath": "[concat('/home/', parameters('sftpUser4'), '/', parameters('sftpUser4'))]",
                                    "name": "[parameters('sftpUser4')]",
                                    "readOnly": false
                                } ,
                                {
                                    "mountPath": "[concat('/home/', parameters('sftpUser5'), '/', parameters('sftpUser5'))]",
                                    "name": "[parameters('sftpUser5')]",
                                    "readOnly": false
                                }
                            ]
                        }
                    }
                ],
                "initContainers": [],
                "restartPolicy": "OnFailure",
                "ipAddress": {
                    "ports": [
                        {
                            "protocol": "TCP",
                            "port": 22
                        }
                    ],
                    "ip": "[parameters('containerIP')]",
                    "type": "Public",
                    "dnsNameLabel": "[parameters('containerGroupDNSLabel')]",
                    "autoGeneratedDomainNameLabelScope": "Unsecure"
                },
                "osType": "Linux",
                "volumes": [
                    {
                        "name": "[parameters('sftpUser1')]",
                        "azureFile": {
                            "readOnly": false,
                            "shareName": "[parameters('sftpUser1')]",
                            "storageAccountName": "[parameters('storageAccountName')]",
                            "storageAccountKey": "[listKeys(parameters('storageAccountName'),'2019-06-01').keys[0].value]"
                        }
                    },
                    {
                        "name": "[parameters('sftpUser2')]",
                        "azureFile": {
                            "readOnly": false,
                            "shareName": "[parameters('sftpUser2')]",
                            "storageAccountName": "[parameters('storageAccountName')]",
                            "storageAccountKey": "[listKeys(parameters('storageAccountName'),'2019-06-01').keys[0].value]"
                        }
                    },
                    {
                        "name": "[parameters('sftpUser3')]",
                        "azureFile": {
                            "readOnly": false,
                            "shareName": "[parameters('sftpUser3')]",
                            "storageAccountName": "[parameters('storageAccountName')]",
                            "storageAccountKey": "[listKeys(parameters('storageAccountName'),'2019-06-01').keys[0].value]"
                        }
                    } ,
                    {
                        "name": "[parameters('sftpUser4')]",
                        "azureFile": {
                            "readOnly": false,
                            "shareName": "[parameters('sftpUser4')]",
                            "storageAccountName": "[parameters('storageAccountName')]",
                            "storageAccountKey": "[listKeys(parameters('storageAccountName'),'2019-06-01').keys[0].value]"
                        }
                    }  ,
                    {
                        "name": "[parameters('sftpUser5')]",
                        "azureFile": {
                            "readOnly": false,
                            "shareName": "[parameters('sftpUser5')]",
                            "storageAccountName": "[parameters('storageAccountName')]",
                            "storageAccountKey": "[listKeys(parameters('storageAccountName'),'2019-06-01').keys[0].value]"
                        }
                    }
                ]
            }
        }
    ]
}
```

原始

```
{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "storageAccountType": {
            "type": "string",
            "defaultValue": "Standard_LRS",
            "allowedValues": [
                "Standard_LRS",
                "Standard_GRS",
                "Premium_LRS"
            ],
            "metadata": {
                "description": "Storage account type"
            }
        },
        "fileShareName1": {
            "type": "string",
            "defaultValue": "sftpfileshare01",
            "metadata": {
                "description": "Name of the first file share to be created"
            }
        },
        "fileShareName2": {
            "type": "string",
            "defaultValue": "sftpfileshare02",
            "metadata": {
                "description": "Name of the second file share to be created"
            }
        },
         "fileShareAccessTier": {
            "type": "string",
            "defaultValue": "Hot",
                "allowedValues": [
                "Hot",
                "Cool",
                "TransactionOptimized"
            ],
            "metadata": {
                "description": "File Share Access Tier to be created"
            }
        },
        "sftpUser1": {
            "type": "string",
            "metadata": {
                "description": "First username to use for SFTP"
            }
        },
        "sftpPassword1": {
            "type": "securestring",
            "metadata": {
                "description": "Password for the first user to use for SFTP access"
            }
        },
         "sftpUser2": {
            "type": "string",
            "metadata": {
                "description": "Second username to use for SFTP"
            }
        },
        "sftpPassword2": {
            "type": "securestring",
            "metadata": {
                "description": "Password for the second user to use for SFTP access"
            }
        },
        "location": {
            "type": "string",
            "defaultValue": "[resourceGroup().location]",
            "metadata": {
                "description": "Primary location for resources"
            }
        },
        "containerGroupDNSLabel": {
            "type": "string",
            "defaultValue": "az-sftp",
            "metadata": {
                "description": "DNS label for container group"
            }
        }
    },
    "variables": {
        "sftpContainerName": "sftp",
        "sftpContainerGroupName": "sftp-group",
        "sftpContainerImage": "atmoz/sftp:latest",
        "sftpEnvVariable": "[concat(parameters('sftpUser1'), ':', parameters('sftpPassword1'), ' ', parameters('sftpUser2'), ':', parameters('sftpPassword2') )]",
        "storageAccountName": "[concat('sftpstg', uniqueString(resourceGroup().id))]",
        "storageKind": "StorageV2",
        "storageAccessTier": "Hot",
        "supportsHttpsTrafficOnly": true
    },
    "resources": [
        {
            "type": "Microsoft.Storage/storageAccounts",
            "name": "[variables('storageAccountName')]",
            "apiVersion": "2019-06-01",
            "location": "[parameters('location')]",
            "sku": {
                "name": "[parameters('storageAccountType')]"
            },
            "kind": "[variables('storageKind')]",
            "properties": {
                "accessTier": "[variables('storageAccessTier')]",
                "supportsHttpsTrafficOnly": "[variables('supportsHttpsTrafficOnly')]"
            }
        },
        {
            "type": "Microsoft.Storage/storageAccounts/fileServices/shares",
            "apiVersion": "2019-06-01",
            "name": "[concat(variables('storageAccountName'), '/default/', parameters('fileShareName1'))]",
             "dependsOn": [
                "[variables('storageAccountName')]"
            ],
            "properties": {
                "accessTier": "[parameters('fileShareAccessTier')]"
            }
        },
         {
            "type": "Microsoft.Storage/storageAccounts/fileServices/shares",
            "apiVersion": "2019-06-01",
            "name": "[concat(variables('storageAccountName'), '/default/', parameters('fileShareName2'))]",
             "dependsOn": [
                "[variables('storageAccountName')]"
            ],
            "properties": {
                "accessTier": "[parameters('fileShareAccessTier')]"
            }
        },
        {
            "type": "Microsoft.ContainerInstance/containerGroups",
            "name": "[variables('sftpContainerGroupName')]",
            "apiVersion": "2019-12-01",
            "location": "[parameters('location')]",
            "dependsOn": [
                "[resourceId('Microsoft.Storage/storageAccounts/fileServices/shares', variables('storageAccountName'), 'default', parameters('fileShareName1'))]",
                "[resourceId('Microsoft.Storage/storageAccounts/fileServices/shares', variables('storageAccountName'), 'default', parameters('fileShareName2'))]"
            ],
            "properties": {
                "containers": [
                    {
                        "name": "[variables('sftpContainerName')]",
                        "properties": {
                            "image": "[variables('sftpContainerImage')]",
                            "environmentVariables": [
                                {
                                    "name": "SFTP_USERS",
                                    "secureValue": "[variables('sftpEnvVariable')]"
                                }
                            ],
                            "resources": {
                                "requests": {
                                    "cpu": 2,
                                    "memoryInGB": 1
                                }
                            },
                            "ports": [
                                {
                                    "port": 22
                                }
                            ],
                            "volumeMounts": [
                                {
                                    "mountPath": "[concat('/home/', parameters('sftpUser1'), '/', parameters('fileShareName1'))]",
                                    "name": "[parameters('fileShareName1')]",
                                    "readOnly": false
                                },
                                {
                                    "mountPath": "[concat('/home/', parameters('sftpUser2'), '/', parameters('fileShareName2'))]",
                                    "name": "[parameters('fileShareName2')]",
                                    "readOnly": false
                                }
                            ]
                        }
                    }
                ],
                "osType": "Linux",
                "ipAddress": {
                    "type": "Public",
                    "ports": [
                        {
                            "protocol": "TCP",
                            "port": 22
                        }
                    ],
                    "dnsNameLabel": "[parameters('containerGroupDNSLabel')]"
                },
                "restartPolicy": "OnFailure",
                "volumes": [
                    {
                        "name": "[parameters('fileShareName1')]",
                        "azureFile": {
                            "readOnly": false,
                            "shareName": "[parameters('fileShareName1')]",
                            "storageAccountName": "[variables('storageAccountName')]",
                            "storageAccountKey": "[listKeys(variables('storageAccountName'),'2019-06-01').keys[0].value]"
                        }
                    },
                    {
                        "name": "[parameters('fileShareName2')]",
                        "azureFile": {
                            "readOnly": false,
                            "shareName": "[parameters('fileShareName2')]",
                            "storageAccountName": "[variables('storageAccountName')]",
                            "storageAccountKey": "[listKeys(variables('storageAccountName'),'2019-06-01').keys[0].value]"
                        }
                    }
                ]
            }
        }
    ],
    "outputs": {
        "containerIPv4Address": {
            "type": "string",
            "value": "[reference(resourceId('Microsoft.ContainerInstance/containerGroups/', variables('sftpContainerGroupName'))).ipAddress.ip]"
        },
        "containerDNSLabel": {
            "type": "string",
            "value": "[concat(parameters('containerGroupDNSLabel'), '.', parameters('location'), '.azurecontainer.io')]"
        }
    }
}
```

參照

[How to Deploy a Secure FTP (SFTP) Service on Microsoft Azure - CHARBEL NEMNOM - MVP | MCT | CCSP - Cloud & CyberSecurity](https://charbelnemnom.com/how-to-deploy-sftp-service-on-microsoft-azure/#Deploy_SFTP_Service_on_Azure)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- SFTP

- 回首頁

---

*本文章從點部落遷移至 Writerside*
