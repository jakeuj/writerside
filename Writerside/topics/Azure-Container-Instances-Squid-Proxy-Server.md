# Azure Container Instances Squid Proxy Server

> **原文發布日期:** 2022-11-24
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/11/24/Azure-Container-Instances-Squid-Proxy-Server
> **標籤:** 無

---

筆記下如何突破 IT 封鎖？

1. 建立 ACI

```
az group create --name myResourceGroup --location southeastasia
az container create --resource-group myResourceGroup --name mycontainer --image ubuntu/squid --dns-name-label aci-demo --ports 80
```

參照

[快速入門 - 將 Docker 容器部署至容器執行個體 - Azure CLI - Azure Container Instances | Microsoft Learn](https://learn.microsoft.com/zh-tw/azure/container-instances/container-instances-quickstart)

     2. 安裝工具

```
apt-get update
apt-get install vim -y
apt-get install apache2-utils -y
apt-get install curl -y
curl -x http://127.0.0.1:3128 -L http://google.com
```

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/33840f72-0efb-417b-8412-1b87707e655b/1669279373.png.png)

    3. 編輯設定擋 squid.conf

`vim /etc/squid/squid.conf`

    3.1 允許外部連線

搜尋 `http_access allow localnet`

取消註解 #http\_access allow localnet

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/33840f72-0efb-417b-8412-1b87707e655b/1669279676.png.png)

    3.2 更改 Port

搜尋 `http_port 3128`

改成 `http_port 80`

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/33840f72-0efb-417b-8412-1b87707e655b/1669279934.png.png)

參照

[How to Setup Squid Proxy Cache in Azure (Secure Your Network/Internet) (cloudinfrastructureservices.co.uk)](https://cloudinfrastructureservices.co.uk/how-to-setup-squid-proxy-cache-in-azure/)

    3.3 啟用 SFTP

搜尋 `acl SSL_ports port`

新增以下字段

```
acl SSL_ports port 22
acl Safe_ports port 22          # ssh/sftp
```

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/33840f72-0efb-417b-8412-1b87707e655b/1669281158.png.png)

參照

[通過 Squid 代理隧道傳輸 SSH/SFTP (seniorlinuxadmin.co.uk)](https://www.seniorlinuxadmin.co.uk/ssh-over-proxy.html)

    3.4 設定密碼 (Optional)

`apt-get install apache2-utils -y`

搜尋 `auth_param basic program`

加入

```
auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/passwords
auth_param basic realm proxy
acl authenticated proxy_auth REQUIRED
http_access allow authenticated
```

設定帳號密碼 (Example: jakeuj)

```
htpasswd -c /etc/squid/passwords jakeuj
```

參照

[How to set up a squid Proxy with basic username and password authentication? - Stack Overflow](https://stackoverflow.com/questions/3297196/how-to-set-up-a-squid-proxy-with-basic-username-and-password-authentication)

    4. 重啟服務

`` kill -HUP `cat /run/squid.pid` ``

參照

[pid 文件有哪些作用？ - 知乎 (zhihu.com)](https://www.zhihu.com/question/20289583)

    5. 本地測試 80 Port

```
apt-get install curl -y
curl -x http://127.0.0.1:80 -L http://google.com
```

參照

[設定 CURL 透過 Proxy 抓取資料 – Tsung's Blog (longwin.com.tw)](https://blog.longwin.com.tw/2014/04/curl-cli-use-proxy-2014/)

    6. 遠端測試

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/33840f72-0efb-417b-8412-1b87707e655b/1669280521.png.png)

驗證帳號密碼

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/33840f72-0efb-417b-8412-1b87707e655b/1669285340.png.png)

確認 IP 是否從台灣換成新加坡 (資源群組 東南亞 資料中心 位於 SG)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/33840f72-0efb-417b-8412-1b87707e655b/1669280578.png.png)

## 測試 SFTP

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/33840f72-0efb-417b-8412-1b87707e655b/1669281376.png.png)

沒意外了話可以成功取得檔案

### 規格

CPU cores 1

Memory 1.5 GiB

### 價格

記憶體 每 GB NT$129.4533

vCPU 每 vCPU NT$1,184.5094

### 小計

1184+258=1442/月

## 結論

IT 何苦為難 RD？

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Azure
* Container
* Proxy
* Squid

* 回首頁

---

*本文章從點部落遷移至 Writerside*
