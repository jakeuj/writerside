# ACI (Azure Container Instance) 部屬失敗

> **原文發布日期:** 2022-06-20
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/06/20/aci-quota-p100-limit
> **標籤:** 無

---

區域 'southeastasia' 已超出資源類型 'Microsoft.ContainerInstance/containerGroups' 容器群組配額 'P100Cores'。

結論

1若要要求提高限制，請建立 Azure 支援要求。 包括 Azure 免費帳戶和 Azure 學生版在內的免費訂用帳戶沒有資格增加限制或配額。 如果您有免費訂用帳戶，則可以升級到隨用隨付訂用帳戶。

|  |  |
| --- | --- |
| 資源 | 配額 |
| 每個訂用帳戶每個區域 P100 或 V100 GPU 的標準 sku 核心 (CPU) | 0 |

參照

[Azure 訂用帳戶限制與配額 - Azure Resource Manager | Microsoft Docs](https://docs.microsoft.com/zh-tw/azure/azure-resource-manager/management/azure-subscription-service-limits#container-instances-limits)

[Resource availability by region - Azure Container Instances | Microsoft Docs](https://docs.microsoft.com/en-us/azure/container-instances/container-instances-region-availability#linux-container-groups)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Container](/jakeuj/Tags?qq=Container)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
