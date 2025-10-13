# Github Pages 裝載和部署 ASP.NET Core Blazor WebAssembly

> **原文發布日期:** 2021-04-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/04/09/BlazorWebAssemblyGithubPages
> **標籤:** 無

---

筆記下各種問題 404 Hash Decode … ETC.

Failed to find a valid digest in the 'integrity' in Blazor WASM

[裝載和部署 ASP.NET Core Blazor WebAssembly](https://github.com/dotnet/AspNetCore.Docs.zh-tw/blob/live/aspnetcore/blazor/host-and-deploy/webassembly.md#github-%E9%A0%81%E9%9D%A2)
{ignore-vars="true"}

首先將 publish 出來的 wwwroot 當作 root push 到 github 的 {yourname}.github.io 倉儲

以我為例子 push 到 https://github.com/jakeuj/BlazorOnGitHubPages

然後就可以打開 Github Pages https://jakeuj.github.io/BlazorOnGitHubPages/

然後就會遇到一連串問題…

* 404

\_framework/blazor.webassembly.js

404 NotFound

這是因為 git 使用 Jekyll 會忽略底線開頭的資料夾導致找不到檔案

解法：於 root 加入 .nojekyll 這個檔案，內容保持空白即可

* Hash

然後會遇到卡在 Loading…的問題，查看 console 會發現是 Hash 校驗失敗

這是因為 git 在 windows 會自動將換行符號 CRLF 轉成 LF

導致 Hash 計算時因為少了一個 CR (看不到的控制字元) 所以結果會不一樣

解法：於 root 加入 .gitattributes 這個檔案，內容輸入一行 \* binary

然後輸入以下 git 命令來重新套用正規化後提交並推送回 github

`git add --renormalize .`

* UrlRewrite

再來參照以下文檔將 UrlRewrite 用 JS 替代

[使用Github Pages託管Blazor應用](https://dotnet9.com/13324.html)

這邊會新增 wwwroot/404.html 並修改 wwwroot/index.html

* BR Decode

再來參照以下文檔引用 decode.js 來對 br 進行解碼

[裝載和部署 ASP.NET Core Blazor WebAssembly](https://docs.microsoft.com/zh-tw/aspnet/core/blazor/host-and-deploy/webassembly?view=aspnetcore-5.0#compression)

這邊會新增 wwwroot/decode.js 並修改 wwwroot/index.html 來引用 decode.js

* Hash

如果遇到 index.html 的 Hash 驗證失敗

可能是直接修改了 publish 出來的 index.html 這個檔案

解法：從專案的 wwwroot/index.html 開始改並重新發布一次

或是將 console 出現的新 hash 值更新到 root 下的 service-worker-assets.js

```
{
    "hash": "sha256-Eb5dFznqwMb/jb9shi278KGCYpxylEj333x6RV8gyRI=",
    "url": "index.html"
}
```

再 commit & push to Github

* Error: Blazor has already started.

最後看 console 應該剩一個例外

但可以成功看到畫面並正常運作

<https://jakeuj.github.io/BlazorOnGitHubPages/>

* 如果 Github Pages 是使用專案模式 (每個專案一個網站)
  需要把 index.html 裡面的 baseUrl 加上專案名稱
  `<base href="/BlazorOnGitHubPages/" />`
* 如果要用 GitHub Actions 做 CI/CD
  需要設定 [.github/workflows/main.yml](https://github.com/jakeuj/BlazorOnGitHubPages/blob/master/.github/workflows/main.yml)
  我這份是用 .Net 5.0 如果是 3.x 需要行修改 PUBLISH\_DIR
  push 到 master 會自動 publish 到 gh-pages 分支給 github pages 吃
* 結論：所有需要變更的東西請參考這個 [commit](https://github.com/jakeuj/BlazorOnGitHubPages/commit/937f1bd52ba9e5964475174d6c801ce91761ae34#diff-7829468e86c1cc5d5133195b5cb48e1ff6c75e3e9203777f6b2e379d9e4882b3)

參照：https://github.com/jakeuj/BlazorOnGitHubPages

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Blazor](/jakeuj/Tags?qq=Blazor)
* [GitHubPages](/jakeuj/Tags?qq=GitHubPages)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
