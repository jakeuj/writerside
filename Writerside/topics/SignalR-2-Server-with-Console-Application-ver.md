# SignalR 2 Console Server

> **原文發布日期:** 2019-08-12
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/08/12/tutorial-signalr-self-host
> **標籤:** 無

---

SignalR 2 伺服器 主控台應用程式 版本

教學課程：SignalR 自我裝載

https://docs.microsoft.com/zh-tw/aspnet/signalr/overview/deployment/tutorial-signalr-self-host

如何從Hub類外部調用客戶端方法和管理組

https://docs.microsoft.com/en-us/aspnet/signalr/overview/guide-to-the-api/hubs-api-guide-server#how-to-call-client-methods-and-manage-groups-from-outside-the-hub-class

System.Net.HttpListenerException: 指定的网络名格式无效

netsh http add urlacl url=http://\*:7800/ user=Everyone

P.S. http://\*:7800/ 必須跟 WebApp.Start(URL) 裡頭的 URL 一模一樣!! (這東西坑了我好幾小時)

SSL

```
netsh http add sslcert ipport=0.0.0.0:8082
appid={12345678-db90-4b66-8b01-88f7af2e36bf}
certhash=d37b844594e5c23702ef4e6bd17719a079b9bdf
```

https://weblog.west-wind.com/posts/2013/Sep/23/Hosting-SignalR-under-SSLhttps

---

## **SignalR Scaleout with Redis**

https://docs.microsoft.com/en-us/aspnet/signalr/overview/performance/scaleout-with-redis

## **使用中的 MessagePack Hub 通訊協定 SignalR 進行 ASP.NET Core**

https://docs.microsoft.com/zh-tw/aspnet/core/signalr/messagepackhubprotocol?view=aspnetcore-2.2

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- SignalR
- WebSocket

- 回首頁

---

*本文章從點部落遷移至 Writerside*
