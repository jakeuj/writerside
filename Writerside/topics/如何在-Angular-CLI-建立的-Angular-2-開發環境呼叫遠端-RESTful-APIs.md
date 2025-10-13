# 如何在 Angular CLI 建立的 Angular 2 開發環境呼叫遠端 RESTful APIs

> **原文發布日期:** 2019-01-07
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/01/07/Setup-proxy-to-backend-in-Angular-CLI
> **標籤:** 無

---

# Angular Configure Proxy for API calls

最近試了 Angular 的 --proxy-config 一直失敗

If you need to access a backend that is not on localhost, you will need to add the changeOrigin option as follows:

結論，加上這行設定即可

```

"changeOrigin": true
```

```

 {
  "/stationnames": {
    "target": "http://tcgmetro.blob.core.windows.net",
    "secure": false,
    "changeOrigin": true
  }
}
```

BTW, Angular 7 好像又有新的做法

```

var HttpsProxyAgent = require('https-proxy-agent');
var proxyConfig = [{
  context: '/api',
  target: 'http://your-remote-server.com:3000',
  secure: false
}];

function setupForCorporateProxy(proxyConfig) {
  var proxyServer = process.env.http_proxy || process.env.HTTP_PROXY;
  if (proxyServer) {
    var agent = new HttpsProxyAgent(proxyServer);
    console.log('Using corporate proxy server: ' + proxyServer);
    proxyConfig.forEach(function(entry) {
      entry.agent = agent;
    });
  }
  return proxyConfig;
}

module.exports = setupForCorporateProxy(proxyConfig);
```

參照：

[如何在 Angular CLI 建立的 Angular 2 開發環境呼叫遠端 RESTful APIs](https://blog.miniasp.com/post/2017/02/05/Setup-proxy-to-backend-in-Angular-CLI.aspx)

[Angular 6 Tutorial 13: Configure Proxy for API calls](https://www.youtube.com/watch?v=z1MUmTjYKH8)

[Angular 7 Using corporate proxy](https://angular.io/guide/build#using-corporate-proxy)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Angular

* 回首頁

---

*本文章從點部落遷移至 Writerside*
