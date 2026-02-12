# the virtual path maps to another application, which is not allowed

> **原文發布日期:** 2024-01-04
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/01/04/the-virtual-path-maps-to-another-application-which-is-not-allowed
> **標籤:** 無

---

紀錄一下坑

## 結論

~~**珍愛生命，遠離 Web Site Project**~~

修改 .sln

`Debug.AspNetCompiler.VirtualPath = "/"`

### 說明

VS 2022 偵錯正常，但 Rider 偵錯會報錯

`the virtual path maps to another application, which is not allowed`

爬文發現原本設定如下

`Debug.AspNetCompiler.VirtualPath = "/localhost_53574"`

按文嘗試修改為

`Debug.AspNetCompiler.VirtualPath = "/"`

就可以跑了

### 參照

[IIS - ASP.NET 虛擬路徑映射到另一個不允許的應用程式 - 堆疊溢出 (stackoverflow.com)](https://stackoverflow.com/questions/19277350/asp-net-virtual-path-maps-to-another-application-which-is-not-allowed)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- WSP

- 回首頁

---

*本文章從點部落遷移至 Writerside*
