# RedHat OpenShift SandBox 流程筆記

> **原文發布日期:** 2021-02-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/02/23/OpenShiftSandBox
> **標籤:** 無

---

紅帽於2021/2/18開放OpenShift免費使用兩周，藉此機會了解該產品功能，並紀錄一下使用心得。

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/bbd22fd4-8ba2-48ac-90b7-36a4b8a60704/1614050678.jpg)

教學影片
[tech-talks](https://developers.redhat.com/devnation/tech-talks/dev-sandbox)

沙盒申請
[developer-sandbox](https://developers.redhat.com/developer-sandbox)

命令列下載
登入後右上角有個問號，點進去下載，然後把解壓縮後的oc路徑加進環境變數path
`Command Line Tools` > `Download oc for Windows for x86_64`

命令列登入

![file](https://dotblogsfile.blob.core.windows.net/user/jakeuj/bbd22fd4-8ba2-48ac-90b7-36a4b8a60704/1614050714.png)

Example:

* oc login --token=sha256~EfumjEgIpAkCjkFjuXMEgtKKF3M\_gkxatCK69NhVR55 --server=https://api.sandbox.x8i5.p1.openshiftapps.com:6443

建立前端服務

新建應用 前端站台
`oc new-app joellord/urlshortener-front`

* 應用視圖

![file](https://dotblogsfile.blob.core.windows.net/user/jakeuj/bbd22fd4-8ba2-48ac-90b7-36a4b8a60704/1614050724.png)

* 開放外部連線 前端站台
  `oc expose svc/urlshortener-front --port=8080`

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/bbd22fd4-8ba2-48ac-90b7-36a4b8a60704/1614134993.png)

建立後端服務

* 用 Centos7 NodeJS 映像檔 來跑 後端API站台

  `oc new-app quay.io/centos7/nodejs-12-centos7~https://github.com/joellord/urlshortener --context-dir=back`

建立DB

* 建立臨時DB (MongoDB (Ephemeral)
  + Database Service Name=mongo
  + Service Name=shorties
  + Connection Username=shorties
  + Connection Password=shorties
  + DataBase Name=urls
  + Admin Password==shorties

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/bbd22fd4-8ba2-48ac-90b7-36a4b8a60704/1614136441.png)

* 開放外部連線 後端API站台

  `oc expose service/urlshortener`
* 編輯 後端API站台 部屬設定中的環境變數
  + PORT=8080
  + MONGO\_USER=shorties
  + MONGO\_PASSWORD=shorties
  + MONGO\_SERVER=mongo
  + MONGO\_VERSION=3.6

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/bbd22fd4-8ba2-48ac-90b7-36a4b8a60704/1614137270.png)

* 存檔後會自動重新佈署，即可正常取得API回應
  `{"msg":"Hello"}`
* 健康檢查 API /health

  `{"msg":"Hello"}{"server":true,"database":true}`
* 健康檢查如果開不起來或 database 為 false
  請確認 MONGO\_SERVER 與當初設定資料庫的 Database Service Name 相同
* 設定健康檢查

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/bbd22fd4-8ba2-48ac-90b7-36a4b8a60704/1614145305.png)

* 設定完記得打勾後按Add才會生效
  之後在 API Pod Log 裡面會發現每十秒或有一個 request 紀錄
* 前端網站 About 頁面內的 後端 API 與 DB 狀態 API 設定
  + 編輯 前端站台 部屬設定中的環境變數
  + BASE\_URL={你的後端API網址(不包含最後面的 / )}
  + 範例
    BASE\_URL=http://urlshortener-jakeuj-code.apps.sandbox.x8i5.p1.openshiftapps.com
  + 回到前端網站的 about 頁面 應該會看到

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/bbd22fd4-8ba2-48ac-90b7-36a4b8a60704/1614147081.png)

* 如果沒看到可以按看看 Ctrl+F5 看看
* 再沒有可以到前端 Pods 狀態看新部屬有沒有成功跑起來
* 設定短網址
  + 到前端 Add 畫面設定短網址
  + 最回到首頁 Current 應該要可以看到剛剛設定的資料

建立轉址服務

* +Add > Deploy Image
  + Image Name=joellord/urlshortener-redirector
    如果顯示 Request 超過上限可能暫時拉不了這個 Image
  + Runtime Icon=PHP
    討厭PHP了話不選也沒關係？
  + Create
* 回到拓樸視圖可以把原本其他服務拖拉到新的這個服務(按住Shift)
  將前後端與資料庫加到這個新服務群組
* 設定 轉址服務 環境變數
  `oc set env deployment/urlshortener-redirector MONGO_USER=shorties MONGO_PASSWORD=shorties MONGO_SERVER=mongo MONGO_VERSION=3.6`
* 設定 前端頁面 環境變數
  `oc set env deployment/urlshortener-front REDIRECTOR_URL=http://$(oc get route urlshortener-redirector | awk 'NR>1 {print $2}')`
  awk是linux指令，可以安裝Windoin Linux 子系統 WSL (Windows Subsystem for Linux)
  [Windows 10 上適用於 Linux 的 Windows 子系統安裝指南](https://docs.microsoft.com/zh-tw/windows/wsl/install-win10)
  [Ubuntu 20.04 LTS](https://www.microsoft.com/zh-tw/p/ubuntu-2004-lts/9n6svws3rx71?activetab=pivot:overviewtab)
  + 下載 oc
    `wget https://downloads-openshift-console.apps.sandbox.x8i5.p1.openshiftapps.com/amd64/linux/oc.tar`
  + 解壓oc
    `tar -xf oc.tar`
  + 沒把 oc 路徑加到 ENV，直接用 oc.exe 時
    `oc.exe set env deployment/urlshortener-front REDIRECTOR_URL=http://$(oc.exe get route urlshortener-redirector | awk 'NR>1 {print $2}')`
  + 好像有 awk for windows 版本的可以安裝看看
* 開放外部連線 轉址服務 由 80改為8080
  urlshortener-redirector > Route Detail > YAML > spec > port: 8080-tcp > Save

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/bbd22fd4-8ba2-48ac-90b7-36a4b8a60704/1614152204.png)

* 到這邊應該設定完成了，回到前端頁面的首頁點先前設定的轉址最右邊的連結按鈕，應該可以正常連回去長網址

延伸閱讀：[OKD (OpenShift Origin) 3.11 與 Ubuntu 18.04 LTS 建置筆記](https://blog.miniasp.com/post/2020/10/11/Install-OpenShift-Origin-OKD-311-on-Ubuntu-Linux)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [CI/CD](/jakeuj/Tags?qq=CI%2FCD)
* [Container](/jakeuj/Tags?qq=Container)
* [OpenShift](/jakeuj/Tags?qq=OpenShift)
* [WSL](/jakeuj/Tags?qq=WSL)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
