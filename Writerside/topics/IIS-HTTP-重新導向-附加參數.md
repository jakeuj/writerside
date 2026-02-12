# IIS HTTP 重新導向 附加參數

> **原文發布日期:** 2014-10-14
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2014/10/14/146941
> **標籤:** 無

---

IIS HTTP 重新導向

當網站換Domain之類的需求時

我們會用到HTPP重新導向

(此功能需在伺服器管理員的IIS功能中啟用)

之後可以在網站中設定要重新導向的Url

比如：

我有一個網站叫做：http://www.google.com/

今天要換網址為：http://tw.yahoo.com/

我可以在網站設定重新導向至 http://tw.yahoo.com/

但如果 我今天輸入 http://www.google.com/?id=1

實際上會轉到 http://tw.yahoo.com/

也就是 id這個參數會遺失

這時候我們可以把重新導向網址設定為 http://tw.yahoo.com$S$Q

※ 並且勾選下方導至切確位置(而非相對位置)

就可以達到我們的需求

勾選項目的意思是

當我輸入 http://www.google.com/AAA/

不勾選此項目時會導到 http://tw.yahoo.com/AAA/

勾選之後會導到 http://tw.yahoo.com/

而我們要附加參數時所加上的 $S$Q

相當於 /AAA/?id=1

此時我們如果不勾選第一項

會變成 http://tw.yahoo.com/AAA/?id=1/AAA/

勾選之後她會變成 http://tw.yahoo.com + /AAA/?id=1 =>  http://tw.yahoo.com /AAA/?id=1

也就會是我們要的結果

純筆記 很亂 待整理~

Ref：http://www.izhangheng.com/iis-301-permanent-redirect-settings-and-parameters-introduced

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- IIS

- 回首頁

---

*本文章從點部落遷移至 Writerside*
