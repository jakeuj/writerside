# ABP.IO Update 關於更新版本時遇到的 Git CRLF 
 問題

> **原文發布日期:** 2023-01-03
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/01/03/abp-git-cr-lf
> **標籤:** 無

---

筆記下 ABP 更新版本使用 GIT 比對差異遇到的問題

原本打完的文章被吃了

直接下結論

abp new 之後都先 commit 然後重新 checkout 讓 git 將 lf 轉成 crlf (\r\n)

否則比對新舊版本的差異時會有很多內容相同但換行符號不同的情況 lf ≠ crlf

Cli

`abp new ProjectVer7 --ui none -csf --no-random-port -sib`

`-slb` 可以略過 yarn install，因為更新時不需要這些檔案，比較快也比較方便後續操作

參照

[Github Pages 裝載和部署 ASP.NET Core Blazor WebAssembly | Jakeuj - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2021/04/09/BlazorWebAssemblyGithubPages)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [ABP](/jakeuj/Tags?qq=ABP)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
