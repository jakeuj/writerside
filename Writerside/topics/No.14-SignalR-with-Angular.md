# No.14 SignalR with Angular

> **原文發布日期:** 2019-08-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/08/26/abp14
> **標籤:** 無

---

建立自訂 SignalR Hub 並使用 Angular 前端呼叫與回傳

.Web.Host.Hubs.ChatHub.cs

```
public class ChatHub : AbpCommonHub
{
    public ChatHub(IOnlineClientManager onlineClientManager, IClientInfoProvider clientInfoProvider) : base(onlineClientManager, clientInfoProvider)
    {
    }

    public async Task SendMessage(string message)
    {
        Logger.Debug($"User {AbpSession.UserId}: {message}");
        await Clients.All.SendAsync("getMessage", $"User {AbpSession.UserId}: {message}");
    }

    public override async Task OnConnectedAsync()
    {
        await base.OnConnectedAsync();
        Logger.Debug("A client connected to MyChatHub: " + Context.ConnectionId);
    }

    public override async Task OnDisconnectedAsync(Exception exception)
    {
        await base.OnDisconnectedAsync(exception);
        Logger.Debug("A client disconnected from MyChatHub: " + Context.ConnectionId);
    }
}
```

原本Zero是直接使用AbpCommonHub

這邊我繼承該類別來擴充自定義方法 SendMessage 來給前端呼叫

.Web.Host.Startup

```
public void Configure(IApplicationBuilder app, IHostingEnvironment env, ILoggerFactory loggerFactory)
{
    //...

    app.UseSignalR(routes =>
    {
        routes.MapHub<ChatHub>("/signalr");
    });

    //...
}
```

這邊將 AbpCommonHub 改成該做好的 ChatHub

前端在 Chrome F12 Console 輸入

```
abp.signalr.hubs.common.on('getMessage', function (message) {
    // Register for incoming messages
    console.log('received message: ' + message);
});
```

就可以接收 getMessage 傳過來的訊息

接著輸入以下指令就可以呼叫伺服器端sendMessage

```
abp.signalr.hubs.common.invoke('sendMessage', "Hi everybody, I'm connected to the chat!");
```

前端也會透過getMessage收到訊息

甚麼，你說Angular呢？

.Web.Host.Hubs.ChatHub.cs

```
public async Task SendNotification(string message)
{
    var getNotification = new UserNotification
    {
        Notification = new TenantNotification {Data = new MessageNotificationData(message)}
    };
    await Clients.All.SendAsync("getNotification", getNotification);
}
```

Zero 樣板的 Angular 內建通知系統

所以用上面的方法就可以傳訊息給前端

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ABP
- SignalR
- WebSocket

- 回首頁

---

*本文章從點部落遷移至 Writerside*
