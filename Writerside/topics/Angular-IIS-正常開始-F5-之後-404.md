# Angular IIS 正常開始 F5 之後 404

> **原文發布日期:** 2019-06-04
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/06/04/Angular404
> **標籤:** 無

---

Angular IIS 正常開始 F5 之後 404

[http://127.0.0.1:4200/](http://139.9.52.196:4200/app/home) => OK

=> [http://127.0.0.1:4200/app/home](http://139.9.52.196:4200/app/home) => OK

=> F5或網址列ENTER重新讀取URL => 404

結論：應用程式池=>無託管代碼

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/809f5006-22b4-4e10-97bf-43dc611c403a/1559642303_32501.PNG)

不然Angular路由好像無法作用

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Angular](/jakeuj/Tags?qq=Angular)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
