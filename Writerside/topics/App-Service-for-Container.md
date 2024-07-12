# App Service for Container

建立 App service for Container 的時候，部署裡面選不到 Github Actions，所以這邊筆記下
從 Github Actions 部署到 Azure App Service for Container 的步驟。

## 官方文件

[how-cicd-works-with-github-actions](https://learn.microsoft.com/zh-tw/azure/app-service/deploy-ci-cd-custom-container?tabs=acr&pivots=container-linux#how-cicd-works-with-github-actions)

## 建立 Azure Container Registry

登入 Azure Portal，搜尋 `Container Registry` 來建立 ACR。

![acr-bar.png](acr-bar.png)

建立好後可以啟用管理使用者

![acr-mgr.png](acr-mgr.png)

需要時可以用這組帳號密碼來連到 ACR 
[Docker-Registry-settings](Docker-Registry-settings.md)

另外可以到識別裡面啟用系統指派的受控識別

![acr-identity.png](acr-identity.png)

這樣就可以在 Github Actions 中使用這個識別來推送鏡像

## 建立 Azure App Service for Container

登入 Azure Portal，搜尋 `App Service` 來建立 App Service for Container。

![aas-container.png](aas-container.png)

在容器選擇部分沒有 Github 相關選項，所以先選快速入門

![container.png](container.png)

建好之後再來到部署中心，選擇 Github Actions

![github-action.png](github-action.png)

Registry 選擇剛剛建立的 ACR，如果有警告應該是要回去 ACR 設定管理帳號或識別之類的

啟動命令我這邊主程式釋放在 src 資料夾，所以是 `gunicorn main:app --chdir src`

## Github Actions

到 Github repo 裡的 Action 應該就會看到部署的流程

![git-act.png](git-act.png)

## Jetbrains IDEs

如果是用 Jetbrains IDEs 的話，推送後可以看到 Action 狀態

![push-act.png](push-act.png)

## 結果
最後打開 Azure App Service for Container 的 URL 就可以看到部署的網站

![wel-az.png](wel-az.png)

## 參照

[msdocs-python-fastapi-webapp-quickstart](https://github.com/jakeuj/msdocs-python-fastapi-webapp-quickstart)