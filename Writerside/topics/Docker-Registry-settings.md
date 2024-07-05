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

## 推送

右鍵點擊 Dockerfile

![dockerfile-right.png](dockerfile-right.png)

運行或直接修改運行配置，鏡像標記中輸入一下名稱，方便以後識別，不然會是 sha256 (簡稱亂碼)

![dockerfile.png](dockerfile.png)

運行後到服務 Docker 鏡像中會有剛剛的鏡像名稱的 image，右鍵可以推送鏡像

![images.png](images.png)

選擇 ACR

![docker-push.png](docker-push.png)

到 Azure Web App for Containers 裡面可以看到剛剛推送的鏡像

![wac.png](wac.png)

## 參照

[Docker Registry settings](https://www.jetbrains.com/help/pycharm/settings-docker-registry.html)

[tutorial-containerize-simple-web-app-for-app-service](https://learn.microsoft.com/zh-tw/azure/developer/python/tutorial-containerize-simple-web-app-for-app-service?tabs=web-app-fastapi)