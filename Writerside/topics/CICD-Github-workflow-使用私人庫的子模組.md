# CI/CD Github workflow 使用私人庫的子模組

> **原文發布日期:** 2024-02-05
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/02/05/github-action-submodule-pat
> **標籤:** 無

---

Github workflow Submodules from private repositories

## 結論

1. [Fine-grained Personal Access Tokens (github.com)](https://github.com/settings/tokens?type=beta)
2. 從個人設定>開發人員設定>Personal access tokens (PAT) > Fine-grained tokens > 建立新 Token
   - Resource owner > 組織/個人 (視子模組是放在組織或個人選擇對應資源擁有者)
   - Repository access>主倉儲與子模組 (找不到 repo 可能是上模的組織擁有者選錯了)
   - Permissions>Repository permissions> Contents, Metadata > 唯讀權限
3. 從主倉儲>設定>環境(Environments)>Environment secrets>Add secret>將 PAT token 設定進去
4. 將 workflow 的 .yml 中指定環境>簽出子模組>設定 Token ( `token: ${{ secrets.PAT_TOKEN }}` )

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/aefb37fe-3ad9-4086-a7ae-194c924676ef/1707114387.png.png)

personal-access-tokens

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/aefb37fe-3ad9-4086-a7ae-194c924676ef/1707114189.png.png)

Contents, Metadata

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/aefb37fe-3ad9-4086-a7ae-194c924676ef/1707115245.png.png)

Environments

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/aefb37fe-3ad9-4086-a7ae-194c924676ef/1707115313.png.png)

Environment secrets

```
jobs:
  build:
    runs-on: ubuntu-latest
    environment: develop  # 指定 environment 为 develop

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          submodules: recursive
          token: ${{ secrets.PAT_TOKEN }}
```

## 組織

也可以設定成組織通用 Secret，就不用每個 repo 都在建立一次 Secret 來將 PAT 寫進去

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/aefb37fe-3ad9-4086-a7ae-194c924676ef/1707116671.png.png)

Secret

如果要由子模組更新來觸發主 repo CI/CD，可以把主倉儲 workflow 的 .yml 複製一份到子模組

```
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          repository: 組織名稱/Repo名稱
          submodules: recursive
          token: ${{ secrets.OAT_TOKEN }}
```

由於設定了 `repository: 組織名稱/Repo名稱` 觸發後會遷出指定主 repo 來做一次建置與發佈

## Azure

如果是從 Azure Web App Service 部屬中心設定過 Github CI/CD

那麼會發現 workflow 的 .yml 最後的 Deploy 會用到一個 `secrets`名為 `AZUREAPPSERVICE_PUBLISHPROFILE_xxxxx`

如果要讓子模組也可以發布到 Azure

1. 到 Azure Web App Service 下載發行設定檔
2. 到子模組 repo 新增設定 secret `AZUREAPPSERVICE_PUBLISHPROFILE_xxxxx`
3. 將下載回來的 profile.publishsettings 內容全部複製到 `AZUREAPPSERVICE_PUBLISHPROFILE_xxxxx` 的 Value 內

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/aefb37fe-3ad9-4086-a7ae-194c924676ef/1707118945.png.png)![](https://dotblogsfile.blob.core.windows.net/user/小小朱/aefb37fe-3ad9-4086-a7ae-194c924676ef/1707119119.png.png)

```
- name: 'Deploy to Azure Web App'
 uses: azure/webapps-deploy@v2
 id: deploy-to-webapp
 with:
  app-name: 'ai-nb-thermal'
  slot-name: 'develop'
  publish-profile: ${{ secrets.AZUREAPPSERVICE_PUBLISHPROFILE_xxxxx }}
```

參照

[git - How to checkout submodule in GitHub action? - Stack Overflow](https://stackoverflow.com/questions/65077036/how-to-checkout-submodule-in-github-action/75100242#75100242)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Git
- Github

- 回首頁

---

*本文章從點部落遷移至 Writerside*
