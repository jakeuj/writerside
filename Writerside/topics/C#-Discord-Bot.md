# C# Discord Bot

> **原文發布日期:** 2023-03-20
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/03/20/CSharp-Discord-Bot
> **標籤:** 無

---

簡單記錄一下 DC 私聊機器人

![](https://dotblogsfile.blob.core.windows.net/user/御用/621a0c42-0db1-42de-af22-d4643b92a191/1679278254.png.png)

Rider

結論

```
using Discord;
using Discord.WebSocket;

var client = new DiscordSocketClient();

client.Log += (message) =>
{
    Console.WriteLine(message);
    return Task.CompletedTask;
};

client.Ready += () =>
{
    Console.WriteLine("Bot is ready!");
    return Task.CompletedTask;
};

client.MessageReceived += async (message) =>
{
    Console.WriteLine(message);
    // Ignore messages sent by the bot itself
    if (message.Author.Id == client.CurrentUser.Id)
        return;

    // Respond to messages that contain "hello"
    if (message.Content.Contains("hello"))
    {
        await message.Channel.SendMessageAsync("Hi there!");
    }
};

await client.LoginAsync(TokenType.Bot, "YourTokenXxxxxxxx");
await client.StartAsync();
await Task.Delay(-1);
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Discord

- 回首頁

---

*本文章從點部落遷移至 Writerside*
