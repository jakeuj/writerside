# 阿里雲 Web&#x2B; (Aliyun Cloud Web Plus) 使用筆記 {id="Aliyun-Cloud-Web-Plus-Usage-Notes"}

> **原文發布日期:** 2021-04-29
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/04/29/AliCloudWebPlus
> **標籤:** 無

---

Alibaba Cloud web+ 紀錄使用心得

## 專案命名原則

* Web+ 應用架構
  同一個應用會共用上傳的部屬包版本
  也就是說如果你專案 TestProject 有分前後端 Web 與 API
  應該是要開兩個不同的應用 Web App 與 API App
  然後各自應用裡面去分不同的部屬環境 Prod 與 Staging
  + ABC-Web/Prod
  + ABC-Web/Staging
  + ABC-API/Prod
  + ABC-API/Staging
* 部屬環境命名
  部屬環境名稱會被拿來當作實例名稱中的某一段字節
  假設你有兩個應用 TestProject-Web 與 TestProject-API
  分別有各自的兩個環境 Prod 與 Staging
  自動生成的實例名稱會長程以下這樣
  + ECS
    - `ABC-Web/Prod => WebPlus-Prod`
    - `ABC-API/Prod => WebPlus-Prod`
    - `ABC-Web/Staging => WebPlus-Staging`
    - `ABC-API/Staging => WebPlus-Staging`
  + SLB
    - `ABC-Web/Prod => WebPlus-slb-Prod`
    - `ABC-API/Prod => WebPlus-slb-Prod`
    - `ABC-Web/Staging => WebPlus-slb-Staging`
    - `ABC-API/Staging => WebPlus-slb-Staging`

這樣會導致很多地方的名稱都會長一樣
想像一下你有一百個應用，環境都有Prod與Staging
你就會看到一百個ESC都叫一樣的名字

目前傾向 應用名稱/環境名稱 都把專案名稱放進去

* ABC-Web/ABC-Web-Prod
* ABC-Web/ABC-Web-Staging
* ABC-API/ABC-API-Prod
* ABC-API/ABC-API-Staging

## 踩坑紀錄

* RDS
  從WEB+配置介面內啟用RDS代購時選擇 標準 MSSQL 2019 高可用版 會建立失敗
  目前開工單得到的回應是，要自己去RDS產品頁面購買後，再來配置這邊選擇導入
* SLB
  從WEB+控制台點擊SLB時，都會導到北京區域的SLB頁面，
  如果SLB其實不在北京區域，可能會產生找不到資源的問題，
  比如：綁定上海EIP時找不到已購買EIP，因為她是列出北京EIP
* SLB 502
  配置 SLB 後可能會得到 502 Bad Gateway 錯誤，
  預設健康檢查會去訪問 Web 根目錄
  如果無法正確回傳 2xx 或 3xx 狀態
  SLB 會視為服務不可用，而得到 502
  解決辦法：到 SLB 設定 健康檢查網址 改到可以正常回傳 2xx 或 3xx 的 URL
* 主機實例 公網IP
  此時，主機實例將能夠訪問公網也可以被公網訪問，請注意網絡安全。
  配置主機時預設會配一組外網 IP，如果不需要給外網呼叫，可以選擇關閉外網 IP
  But, 關閉外網 IP 同時也會無法訪問外網！
  所以如果應用不需要訪問外網，只需要提供內網IP給其他服務呼叫，才能關閉外部 IP
* 新建環境失敗
  (失败原因为通过云助手安装Web+ Agent失败，
  系统等待超过1分钟仍然没有收到Agent的心跳，
  可能是由于通过云助手下发命令失败。)
  解決辦法：Web+ 控制台 右上角 重建
* 安全組
  預設 22 Port 對外全開？
  解決辦法：到安全組移除 0.0.0.0，改為公司 IP
* 日誌
  日誌檔案路徑設定一個以上時會無法蒐集日誌

## 專案設定

* Dotnet Core
  目前版本最新只支援到 3.1
* HTTPS Redirect
  SLB 往後拋時預設走 HTTP，強制轉 HTTPS 會連不到
  解決辦法：Startup.cs 中移除 app.UseHttpsRedirection
* Port
  反向代理預設會將 80 Port 導到 5000 Port (dotnet core default port)
  更改 Web Application listen port 可能會造成連不到的情況
  解決辦法：移除 appsettings.json 中的 Kestrel.EndPoints.Http(s).Url
  改用 LaunchSettings.json 或 appsettings.Development.json 來指定 Port
* 發布 目標執行階段
  因為 Runtime 環境是 linux，預設 目標執行階段 Portable 可能會啟動失敗
  解決辦法：發布時將目標執行階段，改成 linux-x64

## 備註

* Web+ 預設硬碟 100G，用不到那摸多可以設到40G
* Web+ 主機實例最小可以設到共享型 1 Core 0.5 G Ram
* SLB 如果不想重建時 IP 跑掉，可以綁定 EIP
  但是 EIP 只能綁到沒有外網 IP 且為 專有網路 的 內網 SLB
  由 Web+ 代購的公網 SLB 是經典網路且已預分配公網 IP 無法再綁定 EIP
  結論：配置內網 SLB 後再綁定 EIP 來固定 IP 位置

## 缺點

* 不太成熟的產品
  配置RDS代購有問題，連結SLB的地區也有問題，甚至新建環境還會失敗
* 不太靈活
  配置外網SLB無法綁定EIP來固定IP，反而要藉由內網SLB才能達成，
  無法自動依照負載彈性伸縮ECS，一定要外網IP才能連外
* 自家服務新版本整合不易
  無法搭配SLB新版ALB來使用，RDS 最新版 MSSQL 2019 無法代購只能導入
* 工具支援度低
  Web+ 專用命令操作 Cli 不支援 Windows，VsCode的 Ali 擴充功能也不支援 Web+

## 結論

還有蠻多進步的空間

## 延伸閱讀

### 阿里雲 Web+ 使用 Cli 部署 DotnetCore 3.1 專案筆記

參考文件：[阿里雲 Web+ 使用 Cli 部署 DotnetCore 3.1 專案筆記](https://dotblogs.com.tw/jakeuj/2021/04/22/AliWebPlusDepoly)

### Drone 阿里雲 Web+ DotnetCore 3.1 CI/CD & DockerHub Images CI/CD

參考文件：[Drone 阿里雲 Web+ DotnetCore 3.1 CI/CD & DockerHub Images CI/CD](https://dotblogs.com.tw/jakeuj/2021/04/22/DroneAliWebPlusCICD)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* 阿里雲
{ignore-vars="true"}
* Web+
{ignore-vars="true"}
* 阿里雲
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
