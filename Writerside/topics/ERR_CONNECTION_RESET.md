# ERR_CONNECTION_RESET

> **原文發布日期:** 2019-11-29
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/11/29/ERR_CONNECTION_RESET
> **標籤:** 無

---

IIS刪除網站之後可能會造成原本網站異常

總之檢查網站繫結的憑證有沒有跑掉

感覺類似原本第四個網站有綁SSL

但後來刪除第三個網站

這時原本第四個網站的索引就變成第三個網站

然後憑證就跑掉了

沒仔細回憶印象中感覺是類似這樣的IIS刪除網站Bug

總之就是原本的網站忽然出現 ERR\_CONNECTION\_RESET

回憶一下最近又剛好有刪除該伺服器的某站台

就先檢查一下壞的的站台的SSL繫結是不是變成未指定狀態

好像遇到不只一次

特此筆記

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [IIS](/jakeuj/Tags?qq=IIS)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
