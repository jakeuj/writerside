# Windows 11 Windows Defender 打不開

> **原文發布日期:** 2021-09-03
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/09/03/Windows11WindowsDefender
> **標籤:** 無

---

Windows 11 Windows Update 之後打不開 Windows Defender

嚇得我先把網路給斷了以為中毒了

了一下才發現不是只有我有這個問題

筆記下解決方法跟注意事項

## 結論

Windows PowerShell

```
Get-AppxPackage Microsoft.SecHealthUI -AllUsers | Reset-AppxPackage
```

## 注意

* 須以管理員身分執行
* 須以 "Windows PowerShell" 執行
  不是 "PowerShell" 當然也不是其他甚麼亂七八糟的東西

不確定是只有 Win 11 會發生還是 Win 10 也會

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Win 11](/jakeuj/Tags?qq=Win%2011)
{ignore-vars="true"}
* [Windows Defender](/jakeuj/Tags?qq=Windows%20Defender)
{ignore-vars="true"}

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
