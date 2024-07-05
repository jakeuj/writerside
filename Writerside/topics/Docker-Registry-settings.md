# Docker Registry settings

如何連到 Container Registry 並且使用它。

## Azure Container Registry

從 ACR 設定中的存取金鑰取得登入伺服器、`username` 和 `password`。

![azure-acr.png](azure-acr.png)

打開設定中的 Docker 註冊表，選擇`Docker V2`，並輸入登入伺服器、`username` 和 `password`。

![acr.png](acr.png)

也能從服務裡面新建設定

![service-bar.png](service-bar.png)

選擇`Docker V2`，並輸入 Azure Container Registry 的登入伺服器和帳號密碼

![acr-settings.png](acr-settings.png)

## 參照

[Docker Registry settings](https://www.jetbrains.com/help/pycharm/settings-docker-registry.html)

[tutorial-containerize-simple-web-app-for-app-service](https://learn.microsoft.com/zh-tw/azure/developer/python/tutorial-containerize-simple-web-app-for-app-service?tabs=web-app-fastapi)