# EDGE 刪除 localhost 的 HSTS

> **原文發布日期:** 2024-01-03
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/01/03/EDGE-localhost-HSTS
> **標籤:** 無

---

最近舊網站開發時常開不起來的筆記

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/b2d2194f-342e-4057-879f-12690d90ebef/1704261878.png.png)

## 結論

1. edge://net-internals/#hsts
2. Delete domain security policies
3. **localhost**

## 注意

填入的是 `localhost` 不含 port, 不含 port, 不含 port！

很重要所以說三次！

## 延伸閱讀

[HSTS (HTTP Strict Transport Security) & HTTPS redirection (Enforce HTTPS in ASP.NET Core) | 御用小本本 - 點部落 (dotblogs.com.tw)](https://dotblogs.com.tw/jakeuj/2019/12/18/HSTS)

### 參照

[解決Edge chromium http強制導向https問題 | No.18 - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/ian/2019/12/19/edge_http_autoredirect_https)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [HSTS](/jakeuj/Tags?qq=HSTS)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
