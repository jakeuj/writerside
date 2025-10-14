# Dapr Kubernetes 部署

> **原文發布日期:** 2021-03-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/03/23/minikube
> **標籤:** 無

---

原本用 Docker 開發

部屬到 GCP 的 K8S

以為懂了甚麼實際卻還有很多不熟的地方

於是乎筆記一下所見所聞

首先參照 Will 保哥的文章

「快速體驗建構在 Dapr 架構下的微服務應用程式並部署到 Kubernetes 叢集」

```
// 使用 chcoc 安裝套件
choco install minikube kubernetes-cli kubernetes-helm k9s -y

// 使用 minikube 設定使用 hyperv

// 對照一下 Docker 啟動 minikube start --driver=docker
minikube config set driver hyperv
// 以指定的K8S版本為基底映像檔來安裝並啟動K8S伺服器端虛擬機
minikube start --cpus=4 --memory=4096 --kubernetes-version=1.20.5 --extra-config=apiserver.authorization-mode=RBAC
// 安裝插件 儀錶板
minikube addons enable dashboard
// 安裝插件 入口？
minikube addons enable ingress

// 使用 chcoc 安裝套件 K8S客戶端 (版本須符合上面K8S伺服器端虛擬機的版本)
choco install kubernetes-cli --version=1.20.5 --allow-downgrade

// 使用 K8S客戶端 查詢版本看是否安裝正確
kubectl version
```

然後我就卡關了

Unable to connect to the server: dial tcp [::1]:8080: connectex: No connection could be made because the target machine actively refused it.

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/00000000-0000-0000-0000-000000000000/1616493400.jfif)

讓我看一下

stderr:
       [WARNING SystemVerification]: this Docker version is not on the list of validated versions: 20.10.3. Latest validated version: 19.03
       [WARNING Service-Kubelet]: kubelet service is not enabled, please run 'systemctl enable kubelet.service'

* Minikube
  記得用管理者開終端機不然會沒有權限開 HyperV
  Minikube 開不了 HyperV 有時候可能需要重開機

未完待續…

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* choco
* DAPR
* Docker
* hyperV
* K8S
* Kubernetes
* MicroService
* minikube

* 回首頁

---

*本文章從點部落遷移至 Writerside*
