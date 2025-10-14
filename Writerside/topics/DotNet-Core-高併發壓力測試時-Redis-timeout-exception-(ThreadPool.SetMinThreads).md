# DotNet Core Redis Timeout

> **原文發布日期:** 2018-07-18
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2018/07/18/DotNetCoreRedis
> **標籤:** 無

---

主要紀錄 DevOps 壓力測試 1000 request 失敗

追根究柢是 dotnet core 預設不像 IIS 會預先生一堆線程

而 OS 每秒又限制只能生 2 thread 出來

導致瞬間湧入連線時 thread 跟不上最後拒絕連線

最後要去設定 ThreadPool.SetMinThreads(...)

Redis 在瞬間大量 Request 逾時問題

把站台從 Apache 搬到 IIS 也一樣

查了半天最後參照 Redis 文章

https://stackexchange.github.io/StackExchange.Redis/Timeouts

其中 DotNet Core 要用程式碼設定

https://msdn.microsoft.com/library/system.threading.threadpool.setminthreads.aspx

雖然有環境變數跟登錄檔的設定方式

但我實測沒作用

也可能是哪邊弄錯了

但最後乖乖更新程式

壓測一台一千有過

監看dotnet.exe的thread數

可以瞬間來到九百多一千

原本每秒只會增加2條thread

導致逾時

* In ASP.NET, use the [“minIoThreads” configuration setting](https://msdn.microsoft.com/en-us/library/7w2sway1(v=vs.71).aspx) under the `<processModel>` configuration element in `machine.config`. According to Microsoft, you can’t change this value per site by editing your web.config (even when you could do it in the past), so the value that you choose here is the value that all your .NET sites will use. Please note that you don’t need to add every property if you put autoConfig in false, just putting autoConfig=”false” and overriding the value is enough:

```

<processModel autoConfig="false" minIoThreads="250" />
```

> **Important Note:** the value specified in this configuration element is a *per-core* setting. For example, if you have a 4 core machine and want your minIOThreads setting to be 200 at runtime, you would use `<processModel minIoThreads="50"/>`.

* Outside of ASP.NET, use the [ThreadPool.SetMinThreads(…)](https://docs.microsoft.com/en-us/dotnet/api/system.threading.threadpool.setminthreads?view=netcore-2.0#System_Threading_ThreadPool_SetMinThreads_System_Int32_System_Int32_) API.
* In .Net Core, add Environment Variable COMPlus\_ThreadPool\_ForceMinWorkerThreads to overwrite default MinThreads setting, according to [Environment/Registry Configuration Knobs](https://github.com/dotnet/coreclr/blob/master/Documentation/project-docs/clr-configuration-knobs.md) - You can also use the same ThreadPool.SetMinThreads() Method as described above.

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* .Net Core
{ignore-vars="true"}
* Redis

* 回首頁

---

*本文章從點部落遷移至 Writerside*
