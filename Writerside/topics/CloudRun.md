# CloudRun

## 情境

.sln 檔案結構如下

```
.
├── Platform
│   ├── Platform.csproj
│   ├── Dockerfile
│   └── ...
├── Platform.sln
├── NuGet.Config
└── ...
```

於 GCP 設定 Cloud Run 服務，並使用 Cloud Build 進行 CI/CD。

## 問題

於 Cloud Build 中，指定 Dockerfile 為 Platform/Dockerfile 時，如何指定 Docker build 的 context 為根目錄？

## 結論

於 Cloud Build 中，指定 Dockerfile 為 Platform/Dockerfile 時，可使用 `.` 指定 context 為根目錄。

自動產生的 cloudbuild.yaml 如下

```yaml
steps:
  - name: gcr.io/cloud-builders/docker
    args:
      - build
      - '--no-cache'
      - '-t'
      - >-
        $_AR_HOSTNAME/$PROJECT_ID/cloud-run-source-deploy/$REPO_NAME/$_SERVICE_NAME:$COMMIT_SHA
      - Platform
      - '-f'
      - Platform/Dockerfile
```

修改為

```yaml
steps:
  - name: gcr.io/cloud-builders/docker
    args:
      - build
      - '--no-cache'
      - '-t'
      - >-
        $_AR_HOSTNAME/$PROJECT_ID/cloud-run-source-deploy/$REPO_NAME/$_SERVICE_NAME:$COMMIT_SHA
      - .
      - '-f'
      - ./Platform/Dockerfile
```

## 解釋

於 `cloudbuild.yaml` 中，`- Platform` 指定 context 為 `Platform` 目錄，修改為 `- .` 即可指定 context 為根目錄。

## 參考圖

![CloudRun.png](CloudRun.png){style="block"}

## REF

[google-cloud-build-how-to-send-context-with-different-path-to-docker-build](https://stackoverflow.com/questions/68303511/google-cloud-build-how-to-send-context-with-different-path-to-docker-build)