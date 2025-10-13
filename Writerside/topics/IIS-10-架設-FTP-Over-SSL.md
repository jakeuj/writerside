# IIS 10 架設 FTP Over SSL

> **原文發布日期:** 2019-06-27
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/06/27/IIS10FTPOverSSL
> **標籤:** 無

---

IIS 10 架設 FTP Over SSL

首先照以下文章進行設定...

參照：[IIS 7 架設 FTP Server](http://my-fish-it.blogspot.com/2012/09/ss-iis-7-ftp-server.html)

這篇主要針對過程中額外的錯誤碼進行說明

Error code 534

IIS根結點的FTP SSL Setting 要先設定好證書

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/6a859fa1-0539-4097-bd49-b3d0931e52df/1561625750_91979.PNG)

參照：[534 Local policy on server does not allow TLS secure connections](https://forums.iis.net/p/1147315/1860794.aspx#1860794)

Error code 530

用戶端的帳號前面要加上 "domain|"

比如域名 google.com 帳號 test

則輸入 google.com|test

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/6a859fa1-0539-4097-bd49-b3d0931e52df/1561625617_91844.PNG)

P.S. 預設加密：允許的話就使用外顯式 TLS 就可以了其實

參照：[530 Valid Hostname is expected](https://poychang.github.io/ftp-530-valid-hostname-is-expected/)

Error code 550

FTP授權規則內確認權限 讀取/寫入 有打勾

另外在指向的資料夾右鍵內容安全性

要確保該WINDOWS帳號有權限 讀取/寫入

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/6a859fa1-0539-4097-bd49-b3d0931e52df/1561625808_79574.PNG)

錯誤：讀取目錄列表失敗

防火牆請打開 20-21 PORT

控制連線 21 Port

資料連線 20 Port

被動模式：IIS FTP Firewall Support 裡面設定外網IP跟Ports

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/6a859fa1-0539-4097-bd49-b3d0931e52df/1564561715_68958.png)

防火牆追加開放剛剛設定的Ports範圍

Example:5000-6000

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/6a859fa1-0539-4097-bd49-b3d0931e52df/1564561727_5422.png)

P.S. Windows 10 檔案總管 不支援 SSL 所以要另外裝 FTP Client

參照：[Download FileZilla Client for Windows (64bit)](https://filezilla-project.org/download.php?type=client)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [IIS](/jakeuj/Tags?qq=IIS)
* [FTP](/jakeuj/Tags?qq=FTP)
* [SSL](/jakeuj/Tags?qq=SSL)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
