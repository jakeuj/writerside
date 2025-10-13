# Azure Immersion: Cloud Native 實作坊

> **原文發布日期:** 2021-03-25
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/03/25/AzureCloudNative
> **標籤:** 無

---

雲原生技術工作坊

Kubernetes/Linux/Docker/Container/DevOps

紀錄一下踩的坑

Azure Immersion: Cloud Native 實作坊

https://github.com/Microsoft-CloudRiches/MCW-Cloud-native-applications/blob/master/Hands-on lab/Before the HOL - Cloud-native applications.md

* Task 1: Setup Azure Cloud Shell
  Azure cloud command 一開始一直卡在 request 沒辦法 success
  我是用 Vivaldi 瀏覽器，後來用 Chrome 開就成功了，然後回 Vivaldi 也可以正常用

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/00000000-0000-0000-0000-000000000000/1616666171.jfif)

* Task 6: Deploy ARM Template Step 2 => code azuredeploy.parameters.json
  **Suffix 會影響建立的 DNS 比如填了sol 會嘗試生成 fabmedicalsol.azurecr.io**
  但Demo就是用sol這三個字，導致錯誤：AlreadyInUse
  解決方法是要用沒人用過可以產生唯一的字詞
* Task 7: Create a GitHub repository Step 13 => git push -u origin master
  GitHub 如果有二因素認證會登入失敗，下面有備註說明，要改用 token 當作密碼來登入
  <https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token>
  權限記得勾選 workflow & repo
* [Task 6: Push images to Azure Container Registry](https://github.com/Microsoft-CloudRiches/MCW-Cloud-native-applications/blob/master/Hands-on lab/HOL step-by-step - Cloud-native applications - Infrastructure edition.md#task-6-push-images-to-azure-container-registry)
  ACR 是 Azure Container Registry，然後燒了幾百塊，待續…

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure](/jakeuj/Tags?qq=Azure)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
