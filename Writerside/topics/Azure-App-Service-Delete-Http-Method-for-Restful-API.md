# Azure App Service Delete Http Method for Restful API

> **原文發布日期:** 2021-10-12
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/10/12/Azure-App-Service-Delete
> **標籤:** 無

---

設定 Azure App Service 以啟用 Delete 方法

## 問題

本地開發的 Restful API 發佈到 Azure App Service 就呼叫失敗

## 結論

設定 web.config

```
<configuration>
   <system.webServer>
      <security>
         <requestFiltering>
            <verbs applyToWebDAV="false">
               <add verb="DELETE" allowed="true" />
            </verbs>
         </requestFiltering>
      </security>
   </system.webServer>
</configuration>
```

### 參照

[【Azure 应用服务】如何让App Service 支持 Delete 方法  - 路边两盏灯 - 博客园 (cnblogs.com)](https://www.cnblogs.com/lulight/p/15092019.html)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Azure

* 回首頁

---

*本文章從點部落遷移至 Writerside*
