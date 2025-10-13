# Jetbrains Writerside CI/CD 自動化部署 Markdown 到 GIthub Pages

> **原文發布日期:** 2024-02-06
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/02/06/deploy-docs-to-github-pages
> **標籤:** 無

---

筆記下流程跟修正官方文件中的錯誤

## 結論

1. 下載安裝 Writerside
   [Download Writerside - a documentation authoring tool (jetbrains.com)](https://www.jetbrains.com/writerside/download/#section=windows)
2. 打開 Writerside 並建立一個新專案
3. 到 Github 建立一個 repo 來放該專案
4. 編輯 Writerside > writerside.cfg > ihp > images > web-path > 改成上面建立的 repo 名稱
5. 在專案中建立 .github/workflows/deploy.yml
   [writerside/.github/workflows/deploy.yml at master · jakeuj/writerside](https://github.com/jakeuj/writerside/blob/master/.github/workflows/deploy.yml)
6. 更新 yml 中的 env
   1. INSTANCE：更新為 module/instanceID，預設為：Writerside/hiWritWritersideerside
      * instanceID：Writerside > hi.tree > instance-profile > id > 預設是 hi
      * module：writerside.cfg 的所在目錄名稱即為 module 名稱
   2. ARTIFACT：須將 instanceID 轉大寫之後填入 $"webhelp{ID}2-all.zip"
      * 預設 instanceID 為 hi, 因此預設值為： webhelpHI2-all.zip
      * 例如 instanceID 為 fh, 因此須跟新為： webhelpFH2-all.zip
   3. DOCKER\_VERSION：需更新到程式版本對應的 Docker image 版號
      * [2024.01.233.14389 - Writerside | JetBrains Marketplace](https://plugins.jetbrains.com/plugin/20158-writerside/docs/2024.01.233.14389.html)
   4. ALGOLIA\_ARTIFACT：須將 instanceID 轉大寫之後填入 $"algolia-indexes-{ID}.zip"
      * 預設 instanceID 為 hi, 因此預設值為： algolia-indexes-ID.zip
      * 例如 instanceID 為 fh, 因此須跟新為： algolia-indexes-FH.zip
7. 到 Github > repo > 設定 > Pages > Build and deployment > Source > GitHub Actions > Save
8. 之後應該只要 push 就會觸發 Action 更新 Github Pages
   * [This is the first topic | Help Instance (jakeuj.github.io)](https://jakeuj.github.io/writerside/default-topic.html)

## 參考

deploy.yml

```
name: Build documentation

on:
# If specified, the workflow will be triggered automatically once you push to the `main` branch.
# Replace `main` with your branch’s name
  push:
    branches: ["main"]
# Specify to run a workflow manually from the Actions tab on GitHub
  workflow_dispatch:

# Gives the workflow permissions to clone the repo and create a page deployment
permissions:
  id-token: write
  pages: write

env:
  # Name of module and id separated by a slash
  INSTANCE: Writerside/hi
  # Replace HI with the ID of the instance in capital letters
  ARTIFACT: webHelpHI2-all.zip
  # Writerside docker image version
  DOCKER_VERSION: 233.14389
  # Add the variable below to upload Algolia indexes
  # Replace HI with the ID of the instance in capital letters
  ALGOLIA_ARTIFACT: algolia-indexes-HI.zip

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Build Writerside docs using Docker
        uses: JetBrains/writerside-github-action@v4
        with:
          instance: ${{ env.INSTANCE }}
          artifact: ${{ env.ARTIFACT }}
          docker-version: ${{ env.DOCKER_VERSION }}

      - name: Upload documentation
        uses: actions/upload-artifact@v3
        with:
          name: docs
          path: |
            artifacts/${{ env.ARTIFACT }}
            artifacts/report.json
          retention-days: 7

      # Add the step below to upload Algolia indexes
      - name: Upload algolia-indexes
        uses: actions/upload-artifact@v3
        with:
          name: algolia-indexes
          path: artifacts/${{ env.ALGOLIA_ARTIFACT }}
          retention-days: 7

# Add the job below and artifacts/report.json on Upload documentation step above if you want to fail the build when documentation contains errors
  test:
# Requires build job results
    needs: build
    runs-on: ubuntu-latest

    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v1
        with:
          name: docs
          path: artifacts

      - name: Test documentation
        uses: JetBrains/writerside-checker-action@v1
        with:
          instance: ${{ env.INSTANCE }}

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    # Requires the build job results
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Download artifact
      uses: actions/download-artifact@v3
      with:
        name: docs

    - name: Unzip artifact
      run: unzip -O UTF-8 -qq ${{ env.ARTIFACT }} -d dir

    - name: Setup Pages
      uses: actions/configure-pages@v2

    - name: Upload artifact
      uses: actions/upload-pages-artifact@v1
      with:
        path: dir

    - name: Deploy to GitHub Pages
      id: deployment
      uses: actions/deploy-pages@v1
```

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/21ffcb21-7990-4684-ad40-36cd35a0a19f/1707207652.png.png)![](https://dotblogsfile.blob.core.windows.net/user/小小朱/21ffcb21-7990-4684-ad40-36cd35a0a19f/1707207569.png.png)![](https://dotblogsfile.blob.core.windows.net/user/小小朱/21ffcb21-7990-4684-ad40-36cd35a0a19f/1707207591.png.png)![](https://dotblogsfile.blob.core.windows.net/user/小小朱/21ffcb21-7990-4684-ad40-36cd35a0a19f/1707207507.png.png)![](https://dotblogsfile.blob.core.windows.net/user/小小朱/21ffcb21-7990-4684-ad40-36cd35a0a19f/1707207607.png.png)![](https://dotblogsfile.blob.core.windows.net/user/小小朱/21ffcb21-7990-4684-ad40-36cd35a0a19f/1707207729.png.png)

## 來源

[Build and publish on GitHub | Writerside (jetbrains.com)](https://www.jetbrains.com/help/writerside/deploy-docs-to-github-pages.html#publish-github-pages)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* CI/CD
{ignore-vars="true"}
* GitHubPages
* JetBrains
* Writerside

* 回首頁

---

*本文章從點部落遷移至 Writerside*
