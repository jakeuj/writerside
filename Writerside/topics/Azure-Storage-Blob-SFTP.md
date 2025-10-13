# Azure Storage Blob SFTP

> **原文發布日期:** 2022-10-13
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/10/13/Azure-Storage-SFTP
> **標籤:** 無

---

Azure 儲存體服務 SFTP 功能支援

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/6bb59fed-05af-48d2-b9a5-5c53fe2be4ab/1689068527.png.png)

## 結論

1. SFTP登入帳號格式為：`$"{儲存體帳戶}.{使用者名稱}"`
   EX: 儲存體帳戶=test, 使用者名稱=jake, sftp 登入帳號為 test.jake
2. SFTP Host 格式為：`$"{儲存體帳戶}.blob.core.windows.net"`
   EX: 儲存體帳戶=test, sftp 登入 Host 為 test.blob.core.windows.net
3. 首頁(登陸)目錄格式為：`$"{容器名稱}/{目錄名稱}"`
   EX: 容器=mycontainer, 則首頁目錄為 mycontainer
   EX: 承上，於其中建立目錄 test, 則首頁目錄為 mycontainer/test
   P.S. 這邊我複製貼上時不小心開頭多了一個空格，Azure 不會報錯且可儲存變更，自己小心
4. 以上設定皆為非同步作業，所以即便設定正確可能需要等一下才能正常連線
5. WinSCP 版本需要 5.10 以上，官方文件有列出支援的 Clinet 與最低版本

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/6bb59fed-05af-48d2-b9a5-5c53fe2be4ab/1696228500.png.png)

### 啟用

基本上開儲存體帳號的時候啟用階層式就可以把 SFTP 打勾

費用 = 9.32  *24* 30 = 22320

這邊主要紀錄一下踩坑

P.S. 既有 Storage 沒有開階層的能不能改我沒測試

### 參照

[Azure Blob 儲存體的 SFTP 支援 (預覽) | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/storage/blobs/secure-file-transfer-protocol-support)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure](/jakeuj/Tags?qq=Azure)
* [SFTP](/jakeuj/Tags?qq=SFTP)
* [Storage](/jakeuj/Tags?qq=Storage)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
