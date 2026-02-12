# Github

筆記下流程跟修正官方文件中的錯誤

## 版號

[The current latest version is 2025.04.8412](https://www.jetbrains.com/help/writerside/deploy-docs-to-github-pages.html#env.DOCKER_VERSION)

## 結論

{collapsible="true"}

1. 下載安裝
[Writerside](https://www.jetbrains.com/writerside/download/#section=windows)
2. 打開 Writerside 並建立一個新專案
3. 到 Github 建立一個 repo 來放該專案
4. 編輯 Writerside > writerside.cfg > ihp > images > web-path > 改成上面建立的 repo 名稱
5. 在專案中建立
[.github/workflows/deploy.yml](https://github.com/jakeuj/writerside/blob/master/.github/workflows/deploy.yml)
6. 更新 yml 中的 env
   - INSTANCE：更新為 module/instanceID，預設為：Writerside/hi
      - instanceID：Writerside > hi.tree > instance-profile > id > 預設是 hi
      - module：writerside.cfg 的所在目錄名稱即為 module 名稱
   - ARTIFACT：須將 instanceID 轉大寫之後填入 $"webhelp{ID}2-all.zip"
      - 預設 instanceID 為 hi, 因此預設值為： webhelpHI2-all.zip
      - 例如 instanceID 為 fh, 因此須跟新為： webhelpFH2-all.zip
   - DOCKER_VERSION：需更新到程式版本對應的 Docker image 版號
     - 2024.01.233.14389 - [DOCKER_VERSION](https://www.jetbrains.com/help/writerside/deploy-docs-to-github-pages.html#env.DOCKER_VERSION)
   - ALGOLIA_ARTIFACT：須將 instanceID 轉大寫之後填入 $"algolia-indexes-{ID}.zip"
     - 預設 instanceID 為 hi, 因此預設值為： algolia-indexes-ID.zip
     - 例如 instanceID 為 fh, 因此須跟新為： algolia-indexes-FH.zip

- 到 Github > repo > 設定 > Pages > Build and deployment > Source > GitHub Actions > Save
- 之後應該只要 push 就會觸發 Action 更新 Github Pages
  - This is the first topic | Help Instance (jakeuj.github.io)

## 參考

deploy.yml

```yaml
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
  DOCKER_VERSION: 2025.04.8412
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
        uses: actions/upload-artifact@v4
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

![Writerside1.png](Writerside1.png){style="block"}

![writerside2.png](writerside2.png){style="block"}

![ws3.png](ws3.png){style="block"}

![ws4.png](ws4.png){style="block"}

![ws5.png](ws5.png){style="block"}

![ws6.png](ws6.png){style="block"}

![1707207729.png](1707207729.png){style="block"}

## 來源

- [Writerside](https://www.jetbrains.com/help/writerside/deploy-docs-to-github-pages.html#publish-github-pages)
