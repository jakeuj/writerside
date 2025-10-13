# 跨網域 Iframe 建立 cookies

> **原文發布日期:** 2021-08-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/08/19/sameSiteCookie
> **標籤:** 無

---

筆記一下跨網域 cookies 建立注意事項

※ .NET Framework 4.7 才有內建 SameSite 屬性可以設定 SameSite.None

總之就是建立 cookies 的時候要設定以下屬性

```
sameSiteCookie.Secure = true;

sameSiteCookie.HttpOnly = true;
sameSiteCookie.SameSite = SameSiteMode.None;
```

完整範例

```
// Create the cookie
HttpCookie sameSiteCookie = new HttpCookie("SameSiteSample");

// Set a value for the cookie
sameSiteCookie.Value = "sample";

// Set the secure flag, which Chrome's changes will require for SameSite none.
// Note this will also require you to be running on HTTPS
sameSiteCookie.Secure = true;

// Set the cookie to HTTP only which is good practice unless you really do need
// to access it client side in scripts.
sameSiteCookie.HttpOnly = true;

// Add the SameSite attribute, this will emit the attribute with a value of none.
// To not emit the attribute at all set the SameSite property to -1.
sameSiteCookie.SameSite = SameSiteMode.None;

// Add the cookie to the response cookie collection
Response.Cookies.Add(sameSiteCookie);
```

參照

[SameSite cookie sample for ASP.NET 4.7.2 C# WebForms | Microsoft Docs](https://docs.microsoft.com/en-us/aspnet/samesite/csharpwebforms)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Cookies](/jakeuj/Tags?qq=Cookies)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
