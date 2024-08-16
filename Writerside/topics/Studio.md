# Studio

ABP 最近整了一個圖形化介面工具箱，叫做 Studio，可以用來快速建立專案、模組、頁面、服務等等。

## 需求

* [Rider](https://www.jetbrains.com/rider/download/#section=windows) / Visual Studio 2022 (v17.3+) for Windows / Visual Studio for Mac. 1
* [.NET 8.0+](https://dotnet.microsoft.com/zh-tw/download/dotnet/8.0)
* [Node](Node-js.md) v16 or v18
* [Yarn v1.20+](https://classic.yarnpkg.com/lang/en/docs/install/#windows-stable) (not v2) 2 or npm v6+ (already installed with Node)
* Docker

以上需求沒有達成則會導致建立專案實缺胳膊少腿，比如無法用 Yarn 安裝 js lib，無法建立 Redis 服務...等等

## Redis
用 Studio 建立專案會自動使用 Docker 執行 Redis 並建立 network，所以不用自己跑 docker run redis 相關指令來起 Redis 服務

前提是有先把 Docker Engine 跑起來，以 Windows 來說就是開機要先打開 Docker Desktop

如果自己建立 redis container，會導致 Studio 的 docker 相依性作業失敗 (無法建立同名容器 `Redis`)

這可能是為了使用 K8S，所以 Studio 會用一個 ps1 腳本來自動建立 Redis 容器與網路

如果沒有用 Business 版本以上，自己 docker run redis 也是可以的 (記得 -p 6379:6379 開放訪問 Redis Server)

## Node.js
ABP Studio 需要 Node.js 版本為 v16 或 v18

- 單一版本：僅需一個版本可以直接從 [Node.js 官方](https://nodejs.org/zh-cn/download/prebuilt-installer) 下載安裝
![nodejs18.png](nodejs18.png)
- 多版本切換：有其他專案會用到不同版本可以使用 NVM，可以參考此篇筆記 [Vue](Vue.md)
![nvm18.png](nvm18.png)

## WireGuard (選擇性)
WireGuard 是一個快速、現代、安全的 VPN 協議，可以用來連接到公司內部網路，或是在公共網路上保護隱私。

ABP Studio 需要 WireGuard 來執行 Kubernetes 作業

[WireGuard 官方下載](https://www.wireguard.com/install/#windows-7-81-10-11-2008r2-2012r2-2016-2019-2022)

## Docker (選擇性)
ABP Studio 需要 Docker 來執行 Kubernetes 作業。

[Docker 安裝](https://docs.docker.com/get-docker/)

## 安裝
從 ABP 官方網站下載 [ABP Studio](https://abp.io/studio)

![abp-studio-download-page](https://raw.githubusercontent.com/abpframework/abp/rel-8.2/docs/en/studio/images/abp-studio-download-page.png)

## 登入
安裝 ABP Studio 後，您可登錄以訪問所有功能。要登錄，請遵循以下步驟：

1. **Launch ABP Studio:** Open ABP Studio on your desktop.

2. **Login Credentials:** 當提示時輸入您的 [abp.io](https://abp.io/) 登錄憑證。

## 更改 UI 主題
ABP Studio 允許您根據您的偏好自訂使用者介面主題。您可更改 UI 主題，如下圖所示：

![preference-theme-change](https://raw.githubusercontent.com/abpframework/abp/rel-8.2/docs/en/studio/images/preference-theme-change.png)

## 升級
ABP Studio 在背景中定期檢查更新，當ABP Studio的新版本可用時，將通過模態通知您。
該模態將提示您更新至最新版本，如下所示：

![new-version-available-window](https://raw.githubusercontent.com/abpframework/abp/rel-8.2/docs/en/studio/images/new-version-available-window.png)

當您看到 "New Version Available "視窗時，請按照以下步驟無縫升級 ABP Studio：

1. 單擊模態視窗中的 "OK "按鈕啟動新版本下載。
2. 進度指示器將顯示下載狀態。
3. 下載完成後，會出現新的模組，並顯示「安裝和重新啟動」按鈕。
4. 按一下「安裝並重新啟動」按鈕以完成安裝程序。

## 結果
![abp-studio-rider.png](abp-studio-rider.png)