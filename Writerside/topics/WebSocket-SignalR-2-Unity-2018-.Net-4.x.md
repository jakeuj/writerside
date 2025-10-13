# WebSocket SignalR 2 Unity 2018 .Net 4.x

> **原文發布日期:** 2019-06-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/06/19/UnitySignalR2
> **標籤:** 無

---

WebSocket SignalR 2 Unity 2018 .Net 4.x

結論：

1.下載以下兩個套件

[Microsoft.AspNet.SignalR.Client](https://www.nuget.org/packages/Microsoft.AspNet.SignalR.Client/)

[Newtonsoft.Json](https://www.nuget.org/packages/Newtonsoft.Json/)

2.提取Dll

下載的.nupkg改成.zip後解壓縮

把 \lib\net45\\*.dll 放進Unity專案\Assets\Plugins

Ex：newtonsoft.json.12.0.2\lib\net45\Newtonsoft.Json.dll

3.建立\Assets\link.xml

```

<linker>
  <assembly fullname="System.Core">
    <type fullname="System.Linq.Expressions.Interpreter.LightLambda" preserve="all" />
  </assembly>
</linker>
```

4.建立Script

```

async void Start()
{
    var hubConnection = new HubConnection("http://192.168.0.62:7800/");
    IHubProxy _chatHubProxy = hubConnection.CreateHubProxy("ChatHub");
    chatHubProxy.On<string,string>("BroadcastMessage", (cname, message) =>
    {
        // do something
        Debug.Log($"{cname} say {message}.");
    });
    // connect
    await hubConnection.Start();

    // send something to server
    await _chatHubProxy.Invoke("Send", "JAKE","測試訊息" );
}
```

5.確認腳本執行版本與API相容性是 4.x

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/47289ff2-d752-4b3a-8a62-ab7f2a5b2616/1560928740_73125.PNG)

SignalR Client API 相關說明文件請到下面連結查詢

[ASP.NET SignalR Hubs API Guide - .NET Client (C#)](https://docs.microsoft.com/zh-tw/aspnet/signalr/overview/guide-to-the-api/hubs-api-guide-net-client)

參照：[在 Unity 中使用 .NET 4.x](https://docs.microsoft.com/zh-tw/visualstudio/cross-platform/unity-scripting-upgrade?view=vs-2019)

測試環境：[Unity 2018.3.7f1](https://unity3d.com/get-unity/download/archive)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* SignalR
* Unity
* WebSocket

* 回首頁

---

*本文章從點部落遷移至 Writerside*
