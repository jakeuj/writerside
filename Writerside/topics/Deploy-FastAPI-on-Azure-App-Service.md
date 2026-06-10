# Azure App Service 部署 FastAPI 的 Startup Command 設定

<web-summary>在 Azure App Service 部署 FastAPI 時，設定 Startup Command 使用 gunicorn 搭配 uvicorn worker，並用 --chdir 指到正確 src 目錄。</web-summary>

> **原文發布日期:** 2023-05-30
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/05/30/deploy-fastapi-on-azure
> **標籤:** 無

---

筆記下部屬 Python Code 到 App Service 的正確姿勢

## 結論

```
gunicorn -w 4 -k uvicorn.workers.UvicornWorker --chdir src main:app
```

## 說明

### Configure Azure App Service

Open the App Service that you have created by manually navigating to it.

`Under Settings -> Configuration` open tab `General Settings` of App Service

Give the Startup Command with the command to start FastAPI on Azure App Service

`gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`

## 參照

[Deploy FastAPI on Azure App Service – TutLinks](https://tutlinks.com/deploy-fastapi-on-azure/)

![PSNProfiles 卡片](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- App Service
{ignore-vars="true"}
- Azure
- FastAPI

- 回首頁

---

*本文章從點部落遷移至 Writerside*
