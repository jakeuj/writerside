# 無法刪除 Azure 虛擬網路 (VNet)

> **原文發布日期:** 2023-10-24
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/10/24/azure-vnet-cant-delete
> **標籤:** 無

---

刪除已啟用 VNet 整合的 AppService 後會無法刪除該 VNet

## 徵狀

無法刪除子網路 'OutSubNet'。錯誤:  正在使用子網路 OutSubNet，且無法予以刪除。若要刪除子網路，請刪除該子網路中的所有資源。請參閱 aka.ms/deletesubnet。

## 結論

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/71a15c51-ab6a-4c3f-ad17-ad0a70e52726/1698129212.png.png)

下載消費明細

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/71a15c51-ab6a-4c3f-ad17-ad0a70e52726/1698129545.png.png)

有名稱後，按照官方作法重建當初的環境，中斷 VNet 整合，即可刪除該子網或整個資源群組

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/71a15c51-ab6a-4c3f-ad17-ad0a70e52726/1698129739.png.png)

小訣竅是重建 App Service 時，直接啟用 VNet 整合，如果可以選舊的 (刪不掉的) VNet 子網，那就代表 App 名稱是對的 (當初舊的名稱)

## 解決方法

### **移除已刪除 App Service 的 App Service 相關聯連結**

1. 使用與已刪除的 App Service 方案相同的名稱建立 App Service 方案。
2. 使用與已刪除的 App Service 相同的名稱建立 App Service。
3. 連結 App Service 與 VNet 子網路。
4. 中斷 VNet 的連線：[App Service] > [網路] > [VNet 整合] > [中斷連線]。
5. 刪除子網路。
6. 刪除虛擬網路。
7. 刪除 App Service 和 App Service 方案。

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [App Service](/jakeuj/Tags?qq=App%20Service)
* [Azure](/jakeuj/Tags?qq=Azure)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
