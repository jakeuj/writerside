#  Docker Jenkins Agent Dotnetcore Drone

> **原文發布日期:** 2021-04-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/04/19/Jenkins
> **標籤:** 無

---

Azure Devops Pipeline CI/CD 被拿去挖礦

導致現在要寫信申請才能用

等信之餘來試做一下 Jenkins

沒幾分鐘我就放棄了改看 Drone

基本上我也沒用過 Jenkins 所以先照著前人的足跡做做看

<https://ithelp.ithome.com.tw/articles/10200621>

其中筆記下踩到的坑

* 第一次安裝時記得把內網 IP 給打上去
  因為接著會新增子節點來做 build 的工作
  這是在不同 container 作業
  所以彼此的網路不是共通的
  打 localhost:8080 在子結點是不會找到 Master 的
  雖然建個 switch 打通他們可能也不是不行啦
  但就簡單測試嘛，打上 Lan IP 省事！
* 看到要自己弄一個包含 sdk 的 slave 環境
  我就懷念 yaml 設定好 docker 就會自動 pull 然後 build
  於是乎想起其實我原本是打算研究用 Drone 來做 CI/CD
  https://blog.wu-boy.com/drone-devops/

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [CI/CD](/jakeuj/Tags?qq=CI%2FCD)
{ignore-vars="true"}
* [Container](/jakeuj/Tags?qq=Container)
* [Docker](/jakeuj/Tags?qq=Docker)
* [.Net Core](/jakeuj/Tags?qq=.Net%20Core)
{ignore-vars="true"}
* [Drone](/jakeuj/Tags?qq=Drone)
* [Jenkins](/jakeuj/Tags?qq=Jenkins)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
