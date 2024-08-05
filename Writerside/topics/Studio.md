# Studio

ABP 最近整了一個圖形化介面工具箱，叫做 Studio，可以用來快速建立專案、模組、頁面、服務等等。

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
![abp-studio.png](abp-studio.png)