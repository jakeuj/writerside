# Dotnet Core NLog 於 Linux 無法產生 Log 問題

> **原文發布日期:** 2021-06-17
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/06/17/LinuxNLogConfig
> **標籤:** 無

---

Nlog.config 的採坑紀錄

直接下結論

Linux

NLog的設定檔的檔名只會吃以下兩種

- NLog.config
- nlog.config

所以要注意檔名**不能**是以下兩種

- nLog.config
- Nlog.config

---

Windows

因為 OS 本身無視大小寫

所以以上四種都是可以吃得到的

然後放到正式環境如果是 linux

Log 就會難產

---

Git

如果在 Windows

因為改檔案名稱大小寫預設 Git 會無視

有兩種方法可以改完並commit

1. 改 git config
   `git config --local core.ignorecase false`
2. 下 git mv 指令
   `git mv Nlog.config nlog.config`

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- C#
{ignore-vars="true"}
- Git
- Log
- Log
- .Net Core
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
