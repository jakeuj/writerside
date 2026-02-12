# HSTS (HTTP Strict Transport Security) &amp; HTTPS redirection (Enforce HTTPS in ASP.NET Core) {id="HSTS-And-HTTPS-Redirection-In-ASP-NET-Core"}

> **原文發布日期:** 2019-12-18
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/12/18/HSTS
> **標籤:** 無

---

就簡介一下ASP.NET Core裡頭的Https相關設定
app.UseHsts();
app.UseHttpsRedirection();

app.UseHsts();

就是有https要求的時候建立一個cookie給瀏覽器說以後都要用https來訪問

問題是使用者一直不用https來訪問了話這條等於沒效果

app.UseHttpsRedirection();

這條是伺服器收到http強制重新導向https，配合上面hsts可以解決上述問題

配合上hsts可以達到重定向一次就可以讓client(瀏覽器)以後都發https過來

省得每次重新導向

<https://zh.wikipedia.org/wiki/HTTP%E4%B8%A5%E6%A0%BC%E4%BC%A0%E8%BE%93%E5%AE%89%E5%85%A8>
{ignore-vars="true"}

<https://docs.microsoft.com/en-us/aspnet/core/fundamentals/startup?view=aspnetcore-3.1#the-configure-method>

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- HSTS
- HTTPS

- 回首頁

---

*本文章從點部落遷移至 Writerside*
