# SignalR 2.0 與 Unity Game 的 WebSocket&#xA0;連線筆記

> **原文發布日期:** 2016-07-07
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/07/07/UnitySignalR
> **標籤:** 無

---

SignalR 2.0 與 Unity Game 的 WebSocket 連線筆記

這篇主要是記錄利用SignalR來與Unity建立WebSocket連線的相關筆記

SignalR：[SignalR 2.0 Web 聊天室 Demo](https://dotblogs.com.tw/jakeuj/2016/02/15/signalr)

有需要可以參考我之前的這篇

---

WebSocket特點：[漫談polling 和Websocket](http://blog.jobbole.com/72172/#article-comment)

朋友貼給我的不錯簡介

---

Server端：[USING SIGNALR WITH UNITY](https://damienbod.com/2013/11/05/using-signalr-with-unity/)

建議下載範例程式來看，因為文章沒有寫得很清楚

套件部分是使用NuGet取得

1. Microsoft.AspNet.SignalR.SelfHost
2. Microsoft.Owin.Cors
3. Unity

範例Server開起來是8089 port

---

Client端：[SignalR und Unity in euren Multiplayer-Indie-Games](https://blogs.msdn.microsoft.com/codefest/2014/09/11/signalr-und-unity-in-euren-multiplayer-indie-games/)

重點是有一個使用.Net 2.0建立的SignalR Client 專案下載點

[SignalR.Client.20](https://github.com/jenyayel/SignalR.Client.20)

因為Unity似乎只完整支援到.Net 2.0

下載編譯後把

1. SignalR.Client.20.dll
2. Newtonsoft.Json.dll

丟進Unity專案\Assets\Plugins\

然後 using SignalR.Client.\_20.Hubs;

把範例code裡面的port改成8089就可以測試連線

---

控制反轉：[signalr-with-an-ioc-container](https://cockneycoder.wordpress.com/2013/10/19/signalr-with-an-ioc-container/)

關於SignalR修改成Unity版本的參考文章

---

基本連線完成之後就可以開始做些別的作業了

因為有點懶所以筆記就提供連結參考文了

只是稍微註記一下

有機會再看看是不是重寫個圖文步驟吧

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* C#
{ignore-vars="true"}
* SignalR
* Unity
* WebSocket

* 回首頁

---

*本文章從點部落遷移至 Writerside*
