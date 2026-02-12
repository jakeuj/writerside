# RedHat OKD 建置筆記

> **原文發布日期:** 2021-02-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/02/09/OpenShift
> **標籤:** 無

---

Openshift 免費社群版 (OKD) 的建置筆記

主要提供一個類雲端介面來管理容器相關服務

包含程式碼到容器部屬的CI/CD圖形化介面設定

也包含RBAC(基於角色存取控制)與一些公有雲常見的Pass

Openshift 目前共提供三種產品

- 免費社群版(開源專案)=OKD=OpenShift Origin
- 收費企業版=OpenShift Container Platform=OCP=OpenShift Enterprise
- 雲端 OpenShift Online=普通開發者跟小微企業用的現成公有雲端服務

付費版多了官方技術支持24x7跟一些功能，似乎還比較方便安裝？

官方有提供測試用的Container (local sandbox)

[CodeReady Containers for OKD](https://www.okd.io/crc.html)

[CodeReady Containers for OCP](https://cloud.redhat.com/openshift/create)

第一步下載你目前作業系統的image

然後下方有個 secret 可以下載或等等複製貼上

第二步是照著文件跑安裝設定流程

[Getting Started Guide](https://access.redhat.com/documentation/en-us/red_hat_codeready_containers/)

踩坑紀錄：

- crc oc-env
  這邊會要你執行

  ```batch
  SET PATH=C:\Users\yourName\.crc\bin\oc;%PATH%
  @FOR /f "tokens=*" %i IN ('crc oc-env') DO @call %i
  ```

  {ignore-vars="true"}

  這段是在CMD跑，要用PS可能要自己去系統環境變數PATH自己加oc路徑
  然後還要重開機，重開完要重新 crc setup > crc start (有問題crc stop再重跑)
  或是先不管oc，直接從這拿帳密由 `PM> crc console` 開出 web 直接登入管理介面

以上裝完會有個web可以登入來測試 OpenShift 4

管理功能：

- OperatorHub 類似雲端提供服務：GitLab, MongoDB, ELK, Redis...ETC.
- Workloads：Posa,Cron Jobs
- 網路：服務、路由、政策
- 儲存體：硬碟空間綁定、硬碟快照
- Builds：容器印象檔管理(Image Streams)、Build Configs自動建置設定(根據映象檔或設定檔更新觸發自動Build)
- 監控：警報、儀錶板、指標(監視應用程序指標，創建自定義指標查詢)
- 運算：節點、機器、機器組、自動擴展、健康檢查
- 使用者管理：使用者、群組、角色、服務帳號
- 管理：叢集管理、資源配額、限制範圍(容器可用記憶體上下限)

開發者功能

- 新增：
  - 從Git建置與部屬
  - 部屬映像檔到容器
  - 從 Dockerfile 建置並部屬
  - 從 Yaml 建立資源
  - DB：從官方映像檔新增資料庫服務(MariaDB、MySql、PostgreSQL)
- Topology：將各類資源變成視圖顯示
- 監控：儀錶板、指標、警報、事件檢視
- 建置：建立 Build Configs 自動建置新容器 (根據映象檔或設定檔更新觸發自動Build)
- 專案：專案總覽、細節、存取權限控制(何人可以參與此專案)
- Config Map：分離設定檔與映像黨之間的耦合，提供項容器注入配置的機制
- Secret：金鑰管理，與前項類似，旨在抽離敏感字段

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/670c8bc8-e078-4975-ab60-008be1a6ed03/1612863601.png)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/670c8bc8-e078-4975-ab60-008be1a6ed03/1612863784.png)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/670c8bc8-e078-4975-ab60-008be1a6ed03/1612863622.png)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/670c8bc8-e078-4975-ab60-008be1a6ed03/1613523675.png)

---

下面是不用官方測試容器自己從頭裝環境的筆記

Hint

- pull-secret
  4.6 建立叢集時 install-config.yaml 內會需要填 pull-secret
  要到雲端拿 https://cloud.redhat.com/openshift/install/pull-secret
  `pullSecret: '{"auths": ...}'`
  好像也可以用假的
  `{"auths":{"fake":{"auth": "bar"}}}`​

- 查詢 Ubuntu 版本
  `lsb_release -a`
- 查 VM IP
  `ip a`
- 建立金鑰並改用金鑰登入取代打密碼
  1. ​建立公私鑰
     `PS> ssh-keygen`
  2. 上傳公鑰`id_rsa.pub`至遠端VM
     `PS> type $env:USERPROFILE\.ssh\id_rsa.pub | ssh {IP-ADDRESS-OR-FQDN} "cat >> .ssh/authorized_keys"`
     Example: userName=jakeuj, IP=172.29.101.131
     `PS> type $env:USERPROFILE\.ssh\id_rsa.pub | ssh jakeuj@172.29.101.131 "cat >> .ssh/authorized_keys"`
  3. 改用私鑰登入
     `PS> ssh -i $env:USERPROFILE\.ssh\id_rsa jakeuj@172.29.101.131`

參照

[OpenShift](https://www.openshift.com/)

[OKD](https://www.okd.io/)

[Will保哥OKD (OpenShift Origin) 3.11 與 Ubuntu 18.04 LTS 建置筆記](https://blog.miniasp.com/post/2020/10/11/Install-OpenShift-Origin-OKD-311-on-Ubuntu-Linux)

[安裝一個OpenShift 4準生產叢集](https://www.jianshu.com/p/be2ca468f981)

[Windows 10 OpenSSH Equivalent of "ssh-copy-id"](https://www.chrisjhart.com/Windows-10-ssh-copy-id/)

[Windows 10 上適用於 Linux 的 Windows 子系統安裝指南](https://docs.microsoft.com/zh-tw/windows/wsl/install-win10)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- CI/CD
{ignore-vars="true"}
- OKD
- OpenShift
- PowerShell
- Ubuntu

- 回首頁

---

*本文章從點部落遷移至 Writerside*
