# Angular woff json 404 &amp; the web.config asset path must start with the project source root {id="Angular-Woff-Json-404-And-Web-Config-Asset-Path"}

> **原文發布日期:** 2019-02-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/02/19/angularwebconfig
> **標籤:** 無

---

Angular woff json 404 & the web.config asset path must start with the project source root

這篇背景是Anguar上Azure之後開不起來

主要兩個問題

1.不支援靜態檔案：字型檔、設定檔...等等

.woff .woff2 .json

這邊主要是因為host是iis

要加上mime了話要寫在web.config裡面給iis讀取設定

```

<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <staticContent>
      <remove fileExtension=".json" />
      <mimeMap fileExtension=".json" mimeType="application/json" />
   <mimeMap fileExtension="woff" mimeType="application/font-woff" />
      <mimeMap fileExtension="woff2" mimeType="application/font-woff" />
    </staticContent>
  </system.webServer>
</configuration>
```

參考：[Angular - 從Github部署Azure App Service](https://ithelp.ithome.com.tw/articles/10198310)

2.ng build 沒有輸出 web.config

這是延伸自上面第一個問題

加上本身對Angular不熟悉

首先依樣先參照上面那個連結內的教學

angular.json內build的assets要加上web.config

```

"assets": [
    "web.config",
    "src/assets",
```

但這邊有個問題是你可能會得到一個錯誤

The web.config asset path must start with the project source root

英文主要是說web.config這檔案必須在我們定義的sourceRoot路徑裡頭

然後找一下相關設定如下

```

"root": "",
"sourceRoot": "src",
```

嗯就是說我web.config沒有放在src目錄所以不給我設定

但src裡面是原始碼所以要改用別的設定方式

```

"assets": [
    "src/assets",
    "src/favicon.ico",
    {
        "glob": "web.config",
        "input": "",
        "output": "/"
    },
```

單獨設定該檔輸入/輸出路徑，就不用受sourceRoot限制

以上

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Angular

- 回首頁

---

*本文章從點部落遷移至 Writerside*
