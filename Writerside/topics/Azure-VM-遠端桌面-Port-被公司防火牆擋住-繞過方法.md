# Azure VM 遠端桌面繞過防火牆

> **原文發布日期:** 2021-03-22
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/03/22/SetRDPPort
> **標籤:** 無

---

筆記下 主要就改遠端預設 Port 到一個沒被封的 Port

開完 VM 到左邊菜單找

執行命令

裡面找到這個指令點擊

SetRDPPort (Set Remote Desktop port)

進去輸入沒被擋的 Port (8080 or 80 … ETC.)

改完到左邊菜單>連線>RDP>把你改的Port輸入進去再下載打開輸入帳密登入

VM應該是用上面方法就可以了

其他服務可能可以試試用 load blance

網路>負載平衡>去設前端Port跟後端對應

但 Azure SQL好像不能用這機制繞過 1433

好像要裝一個類似中轉的程式

身為開發只覺得連外擋這些 Port 令人困擾

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Azure

* 回首頁

---

*本文章從點部落遷移至 Writerside*
