# 阿里雲 Web&#x2B; 使用 Cli  部署 DotnetCore 3.1 專案筆記 {id="Aliyun-Web-Plus-CLI-Deploy-DotnetCore-3-1"}

> **原文發布日期:** 2021-04-22
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/04/22/AliWebPlusDepoly
> **標籤:** 無

---

首先剛剛打到一半的文章不見了

一次性草稿也沒東西

不知道是不是這原因

我現在感覺有點上火

置頂補充一件事

使用 Web+ 服務預設會幫你開通 22 Port 給全世界連

Web+ 服務預設會幫你開通 22 Port 給全世界連

會幫你開通 22 Port 給全世界連

這是回音你懂嗎？

然後阿里雲有個防火牆服務可以幫你掃描安全性問題

會跟你說22 Port 全開暴露給外面很危險

問你要不要付費一鍵修補漏洞

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/6c006c4c-493e-47b9-b091-8e6876ada30b/1619431121.jfif)

雖然去 安全組 把 22 的來源從 0.0.0.0 改成公司 IP 就可以了

我還是滿肚子的邪火…

---

本文開始

總之先參考我上一篇準備環境

<https://dotblogs.com.tw/jakeuj/2021/04/22/UbuntuDotNetCore>

然後參照官方文件

<https://help.aliyun.com/document_detail/119566.htm>

- Cli

`eval "$(curl -s -L https://webplus-cn-shenzhen.oss-cn-shenzhen.aliyuncs.com/cli/install.sh)"`

這邊如果跑出權限拒絕存取可以先 `sudo su` 切到 root

eval 是 linux 用來執行後面 script 的語法

而 $ 是變數，這邊這變數是從後面網址下載回來的 script

就結果來說就是執行網路上指令碼的意思

作用大概就是安裝阿里雲的 cli

- 變數
  Linux 設定變數的方式就是直接 變數名稱=值
  例如要設定 ALICLOUD\_ACCESS\_KEY 是 123
  `$ ALICLOUD_ACCESS_KEY=123`
  這樣就設定好了，可以用 echo 看看結果
  `$ echo $ALICLOUD_ACCESS_KEY`
  123
- wpctl
  安裝完之後就可以使用 wptcl 來對阿里雲進行操作
  首先要先設定 Secret 相關的東西來取得操作權限
  沒有 Secret 要先去 [RMA](https://ram.console.aliyun.com/) 新增才會拿到
  Region 參照 [阿里雲 地域與可用區 Region ID](https://www.alibabacloud.com/help/zh/doc-detail/40654.htm)
  比如：華東2 上海 ID = cn-shanghai

- ALICLOUD\_ACCESS\_KEY={Your AccessKey ID}
- ALICLOUD\_SECRET\_KEY={Your AccessKey Secret}
- ALICLOUD\_REGION={Your Region ID}

設定好以上三個變數之後可以執行設定命令

`wpctl configure --access-key-id "$ALICLOUD_ACCESS_KEY" --access-key-secret "$ALICLOUD_SECRET_KEY" --region "$ALICLOUD_REGION"  --profile demo`

設定完成會顯示這樣的畫面

```
Configuring profile 'demo' in '' authenticate mode...

Saving profile[demo] ...Done.
Configure Done!!!

#
#      Welcome to use WEBPLUS of Alibaba Cloud
#             ---------------------
#        Command Line Interface version 0.1.0
#   ____________________________________________
#   _|  |___/  /  /  ___/  /  __  /     /  /  __
#   _|  |__/  /  /  /_    /  /_/ /  ___/  /__ __
#   _|   /   /  /  __/   /  __  /  /__   ___/ __
#   _|  /|  /  /  /__   /  /_/ /     /  /     __
#   _|_/_|_/__/_____/__/______/_____/__/________
#
```

- 建置

`dotnet publish -c:Release -o ./publish`

- Zip

`apt-get install zip unzip`

`zip -r webplusdemo.zip ./publish/`

- 部署：上傳並更新
  `wpctl env:apply --package webplusdemo.zip --label webplusVersion0.1 --env Test --app Test -q`
  -q 是安靜模式，沒加會提示是否真的要更新[Y/n]，CI/CD 無人職守時會需要加
- 完成

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/6c006c4c-493e-47b9-b091-8e6876ada30b/1619074893.png)

- 取得最新狀態

1. `wpctl env:use Test --app Test`
2. `wpctl env:events`
3. `wpctl env:info`

```
EnvName:        Test
EnvId:          we-123ce75d8ec33f6ed3adaea0
AppId:          wa-123ce75cf968dd14cea1267d
AppName:        Test
Status:         RUNNING
Stack:          ASP.NET Core 3.1 / Alibaba Cloud Linux 2.1903
PackageLabel:   webplusVersion0.1
CreateUser:     Tester
CreateTime:     2021-04-19 10:13:49 AM
UpdateUser:     vscode
UpdateTime:     2021-04-22 02:59:19 PM
Resources:
+-----------+----+---------------------------+-------------+
|   TYPE    | NO |            ID             | INFORMATION |
+-----------+----+---------------------------+-------------+
| VSwitches |  1 | vsw-456gq4ab8vbd0bosngdor |             |
| VSwitches |  2 | vsw-456ii8zad9vcvzl8d9d6x |             |
| Instance  |  1 | i-7893i7mmbm5dttpl1u4i    |             |
+-----------+----+---------------------------+-------------+
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- .Net Core
{ignore-vars="true"}
- Ubuntu
- 阿里雲
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
