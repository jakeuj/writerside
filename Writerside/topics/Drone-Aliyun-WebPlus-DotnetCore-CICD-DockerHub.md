# Drone 阿里雲 Web&#x2B; DotnetCore 3.1 CI/CD &amp; DockerHub Images CI/CD {id="Drone-Aliyun-WebPlus-DotnetCore-CICD-DockerHub"}

> **原文發布日期:** 2021-04-22
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/04/22/DroneAliWebPlusCICD
> **標籤:** 無

---

筆記下最後成功的 yml 心路歷程

## 心路甚麼的可能沒人在意

## 所以先直接下結論

---

## **V1**

### [**.drone.yml**](https://github.com/jakeuj/Drone/blob/main/.drone.yml)

```
kind: pipeline
type: docker
name: default

steps:
- name: build
  image: mcr.microsoft.com/dotnet/sdk:3.1
  environment:
    ALIYUN_ACCESS_KEY_ID:
      from_secret: aliyun_access_key_id
    ALIYUN_ACCESS_KEY_SECRET:
      from_secret: aliyun_access_key_secret
  commands:
    - dotnet publish -c:Release -o ./publish
    - apt-get update -y
    - apt-get install zip -y
    - zip -r webplusdemo.zip ./publish
    - wget https://webplus-cn-shenzhen.oss-cn-shenzhen.aliyuncs.com/cli/install.sh
    - sh ./install.sh
    - wpctl configure --access-key-id $ALIYUN_ACCESS_KEY_ID --access-key-secret $ALIYUN_ACCESS_KEY_SECRET --region cn-shanghai --profile demo
    - wpctl env:apply --package webplusdemo.zip --label ${DRONE_COMMIT_SHA:0:8} --env Test --app Test -q
```

## 環境變數

可能 Drone 1.x 之後跟之前 0.x 版本的設定有些差異

如果參照到 [舊的文章](https://trylife.cn/p/vue-continuous-deploy-to-aliyun-oss.html)，可能會鬼打牆 (secrets與環境變數)

## Cli

另外阿里雲提供的 Cli 安裝方法，直接在linux跑雖然沒問題

`eval "$(curl -s -L https://webplus-cn-shenzhen.oss-cn-shenzhen.aliyuncs.com/cli/install.sh)"`

但是在 drone 跑我是遇到 command not found: complete 的問題

最後分兩段 wget 再 sh

## Zip

要先 update 才裝得到 Zip

## wpctl

記得 -q 不然會卡在 Yes or No

還有 label 不能重複這邊先以

`${DRONE_COMMIT_SHA:0:8}`

產生八碼版號處理

---

## **V2**

### 如果不想每次重裝 zip & wpctl

可以先做一個裝好的 images 放到 repo

**首先準備** [**Dockerfile**](https://github.com/jakeuj/dockerHub/blob/main/Dockerfile)

```
FROM mcr.microsoft.com/dotnet/sdk:3.1 AS base
MAINTAINER jakeuj@hotmail.com

RUN apt-get update;apt-get install -y zip
RUN eval "$(curl -s -L https://webplus-cn-shenzhen.oss-cn-shenzhen.aliyuncs.com/cli/install.sh)"
```

主要就是裝好 zip 跟 wpctl

這邊 wpctl 可以直接用 eval 安裝不會找不到指令了

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/56d9b856-ac65-47db-8135-0ed725004253/1619408878.jfif)

可以手動建置並推送到 docker hub repo

docker build -t aliwpctl . --no-cache

docker push [jakeuj/aliwpctl](https://hub.docker.com/repository/docker/jakeuj/aliwpctl)

也可以將 **Dockerfile 放到 Github**

然後到 docker hub repo 的 Build

去設定 **Automated Builds**

指定對應的 github repo

比如 [jakeuj/dockerhub](https://github.com/jakeuj/dockerHub)

還有分支 預設是 master

但我 github 預設是 main 所以要改一下

之後只要 GitHub repo 有更動

DockerHub 就會自動建置新版 image

最後更新 [.drone.yml](https://github.com/jakeuj/Drone/blob/main/.drone.yml)

```
kind: pipeline
type: docker
name: default

steps:
- name: build
  image: jakeuj/aliwpctl
  environment:
    ALIYUN_ACCESS_KEY_ID:
      from_secret: aliyun_access_key_id
    ALIYUN_ACCESS_KEY_SECRET:
      from_secret: aliyun_access_key_secret
  commands:
    - dotnet publish -c:Release -o ./publish
    - zip -r webplusdemo.zip ./publish
    - wpctl configure --access-key-id $ALIYUN_ACCESS_KEY_ID --access-key-secret $ALIYUN_ACCESS_KEY_SECRET --region cn-shanghai --profile demo
    - wpctl env:apply --package webplusdemo.zip --label ${DRONE_COMMIT_SHA:0:8} --env Test --app Test -q
```

**主要就拿掉安裝 zip 跟 wpctl 的部分**

剩下

1. 建置專案
2. 壓縮打包
3. 設定環境 (如果可以傳環境變數到 images 可能這段可以再精簡？)
4. 上傳雲端

---

## **V3**

Step

將 CI/CD 分成 建置(`build`) & 部署(`deploy`) 兩個階段

```
kind: pipeline
type: docker
name: default

steps:
- name: build
  image: mcr.microsoft.com/dotnet/sdk:3.1
  commands:
    - dotnet publish -c:Release -o ./publish
- name: deploy
  image: jakeuj/aliwpctl
  environment:
    ALIYUN_ACCESS_KEY_ID:
      from_secret: aliyun_access_key_id
    ALIYUN_ACCESS_KEY_SECRET:
      from_secret: aliyun_access_key_secret
  commands:
    - zip -r webplusdemo.zip ./publish
    - wpctl configure --access-key-id $ALIYUN_ACCESS_KEY_ID --access-key-secret $ALIYUN_ACCESS_KEY_SECRET --region cn-shanghai --profile demo
    - wpctl env:apply --package webplusdemo.zip --label ${DRONE_COMMIT_SHA:0:8} --env Test --app Test -q
```

看來資料夾檔案是沿用

有些 CI/CD 要先把 build 的東西上傳到 artifacts

下個階段再下載回來才能繼續往後做 (因為是完全獨立的兩個 container)

至此大致完成！

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/56d9b856-ac65-47db-8135-0ed725004253/1619409252.png)

---

```
Invoke-RestMethod 'https://notify-api.line.me/api/notify'
-Method 'POST'
-Headers @{"Authorization"="Bearer $AccessToken"}
-Body @{"message"="1"}
```

## 延伸閱讀

### [阿里雲 Web+ 使用 Cli 部署 DotnetCore 3.1 專案筆記](https://dotblogs.com.tw/jakeuj/2021/04/22/AliWebPlusDepoly)

### [Drone Cloud Github DotNetCore Build CI/CD Runner Note](https://dotblogs.com.tw/jakeuj/2021/04/20/Drone)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* CI/CD
{ignore-vars="true"}
* .Net Core
{ignore-vars="true"}
* Drone
* 阿里雲
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
