# Drone Cloud Github DotNetCore Build CI/CD Runner Note

> **原文發布日期:** 2021-04-20
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/04/20/Drone
> **標籤:** 無

---

Drone 可以用容器來做 CI/CD

目測官方有提供雲端環境可以直接用

也可以自建環境到公司內部自己用

筆記一下注意事項

[Drone](https://www.drone.io) 官方網站有 Cloud 與 Docs 的連結

不得不說個人認為網站UX做得很差

點過去 Cloud/Docs 是回不來主頁 Www 欸？

首先建議先從 Cloud 的 Ready 環境先跑一遍新手任務

我是接 GitHub 的教學任務 因為解完了好像看不到原本的任務內容

大致上跟自建環境的流程一樣吧

<https://docs.drone.io/server/provider/github/>

看圖說故事應該是沒有甚麼太大的問題才是

解完應該可以在 Cloud 大廳看到 Github 上的專案列表

接著可以在 Github 開一個新倉儲來試跑一下 Drone 的 CI/CD

建立一個 dotnet core web application 專案 (我這邊是用 3.1 版本)

Push 到 Github Repo 然後到 Drone Cloud 點一下 SYNC

找到剛建立的倉儲 點進去之後 按 ACTIVATE REPOSITORY > SAVE CHANGES

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9744a47c-a66d-42fa-88da-158194f860bc/1618912494.png)

畫面稍微看一下會發現 Configuration 是 .drone.yml 這個檔案

有用過 Gitthub Action 或 Azure Pipeline 之類的應該知道該怎麼做

總之到專案根目錄建立該 .drone.yml 檔案

內容先試打一下建置 dotnet core 的描述

```
kind: pipeline
name: dev_depoly
workspace:
  base: /data/netcore
  path: istr

steps:
- name: build
  image: mcr.microsoft.com/dotnet/sdk:3.1
  commands:
    - dotnet publish -c:Release -o ./publish
    - echo '>>> 建置完成，使用 ls 顯示一下目錄，看看結果 <<<'
    - ls -la
```

Ref: https://github.com/jakeuj/Drone/blob/main/.drone.yml

到這邊 commit & push to  master 之後應該會觸發 CI/CD

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9744a47c-a66d-42fa-88da-158194f860bc/1618912476.png)

可以到 Drone Cloud 裡面看看建置過程/結果

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9744a47c-a66d-42fa-88da-158194f860bc/1618912597.png)

參照：<https://www.istr.cn/archives/93/>

再來是自建 Drone Server & Runner 的部分

Server 的部分就是主要頁面與全局控制器

Runner 的部分類似 Jenkins 的 Agent

就是觸發 CI/CD 後，會交給他幫你去跑你的 yml 裡面要他做的事情

參照：https://www.tpisoftware.com/tpu/articleDetails/1884

前置作業

首先你需要安裝 [Docker](https://docs.docker.com/docker-for-windows/install/)

因為 Drone Server 是直接用 container 跑的

包含後續的 runner 也是

再來還需要安裝 [ngrok](https://dashboard.ngrok.com/get-started/setup)

ngrok 是幫你的 localhost 生出一個 domain 來給 github webhook 呼叫用的

感覺類似在你電腦起一個轉發器

`localhost:8081 ← http://randomcode.ngrok.io`

不然外部 (github) 是沒辦法 callback你 local 的 Drone server 位置的

然後可以開始用 docker 裝 Drone Server

[官方 Drone Server (Github) 文件](https://docs.drone.io/server/provider/github/)

主要就 pull & run

```
docker run \
  --volume=/var/lib/drone:/data \
  --env=DRONE_GITHUB_CLIENT_ID=456c14e7ed5e418a1ccd \
  --env=DRONE_GITHUB_CLIENT_SECRET=789797177215d9e39854177428f2b3cdc33f3291 \
  --env=DRONE_RPC_SECRET=123f11ca2cabbc1b47cc2fa281eba25c \
  --env=DRONE_SERVER_HOST=45652a865bcf.ngrok.io \
  --env=DRONE_SERVER_PROTO=https \
  --publish=8081:80 \
  --publish=443:443 \
  --restart=always \
  --detach=true \
  --name=drone \
  drone/drone:1
```

跑起來應該是看得到畫面可以授權 github 存取權給他

看起來跟 Drone Cloud 應該有個八十七分像

也可以成功看到你的倉儲才對

甚至也會觸發 CI/CD

只是會發現觸發後她永遠在 pending

然後我也找不到地方看他為什麼 pending

總之就是還沒有 runner 可以去處理這個事件

P.S. 接下來的 runner 如果執行失敗也會造成一樣的結果

再來就一樣把 runner 給裝起來

[Drone Runner Docs](https://docs.drone.io/runner/docker/installation/linux/)

這裡要注意的是 Docker Windows 版

預設跑的是 linux 環境

所以你如果從 Server 那邊接著下一步 Runner 會要你選 Linux or Windows

你要選 Linux 不然 socket 對應會失敗

導致 Runner 連不回 Server

然後 CI/CD 觸發事件會一直卡在 Pending…

```
docker run -d \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e DRONE_RPC_PROTO=https \
  -e DRONE_RPC_HOST=45652a865bcf.ngrok.io \
  -e DRONE_RPC_SECRET=123f11ca2cabbc1b47cc2fa281eba25c \
  -e DRONE_RUNNER_CAPACITY=2 \
  -e DRONE_RUNNER_NAME=dev_depoly \
  -p 3000:3000 \
  --restart always \
  --name runner \
  drone/drone-runner-docker:1
```

注意一下 -v 的參數 (指定掛載卷)

WIndows 會長這樣

`-v //./pipe/docker_engine://./pipe/docker_engine`

除非你去 docker 那邊手動切到 windows 才需要改

不然應該都是要用 linux 的設定才對哦

到這邊就應該都裝好了

跟原本 Drone Cloud 一樣去 Active Repo

然後隨便 push master 看看應該可以觸發 CI/CD

也可以看到建置過程及時 Log

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9744a47c-a66d-42fa-88da-158194f860bc/1618914759.png)

Drone

如果跟我一樣卡 Pending

可以去 Docker 看一下 Runner Container Log

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9744a47c-a66d-42fa-88da-158194f860bc/1618914874.png)

上面是正常畫面

有問題再拿錯誤訊息去找一下古哥囉~

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- CI/CD
{ignore-vars="true"}
- Cloud
- .Net Core
{ignore-vars="true"}
- Drone
- Github

- 回首頁

---

*本文章從點部落遷移至 Writerside*
