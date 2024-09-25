# ABP App Settings

紀錄一下上版需要改的 AppSettings 設定檔。

例如：`appsettings.Production.json`

## DbMigrator

```json
{
  "ConnectionStrings": {
    "Default": "Server=tcp:Test-sqlserver.privatelink.database.windows.net,1433;Initial Catalog=XXX;Persist Security Info=False;User ID=XXX;Password=XXX;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
  },
  "Redis": {
    "Configuration": "XXX.redis.cache.windows.net:6380,password=XXX,ssl=True,abortConnect=False"
  },
  "OpenIddict": {
    "Applications": {
      "Test_Web": {
        "ClientSecret": "XXX",
        "RootUrl": "https://Web.azurewebsites.net"
      },
      "Test_Swagger": {
        "RootUrl": "https://Swagger.azurewebsites.net"
      }
    }
  }
}
```

## AuthServer

```json
{
  "App": {
    "SelfUrl": "https://Auth.azurewebsites.net",
    "CorsOrigins": "https://Swagger.azurewebsites.net",
    "RedirectAllowedUrls": "https://Swagger.azurewebsites.net,https://Web.azurewebsites.net"
  },
  "ConnectionStrings": {
    "Default": "Server=tcp:Test-sqlserver.privatelink.database.windows.net,1433;Initial Catalog=Test;Persist Security Info=False;User ID=XXX;Password=XXX;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
  },
  "Redis": {
    "Configuration": "Test.privatelink.redis.cache.windows.net:6380,password=XXX,ssl=True,abortConnect=False"
  }
}
```

## HttpApi.Host

```json
{
  "App": {
    "SelfUrl": "https://Swagger.azurewebsites.net",
    "CorsOrigins": "https://Angular.azurewebsites.net"
  },
  "ConnectionStrings": {
    "Default": "Server=tcp:Test-sqlserver.privatelink.database.windows.net,1433;Initial Catalog=Test;Persist Security Info=False;User ID=XXX;Password=XXX;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
  },
  "Redis": {
    "Configuration": "Test.privatelink.redis.cache.windows.net:6380,password=XXX,ssl=True,abortConnect=False"
  },
  "AuthServer": {
    "Authority": "https://Auth.azurewebsites.net",
    "MetaAddress": "https://Auth.azurewebsites.net"
  }
}
```

## Web

```json
{
  "App": {
    "SelfUrl": "https://Web.azurewebsites.net"
  },
  "RemoteServices": {
    "Default": {
      "BaseUrl": "https://Swagger.azurewebsites.net/"
    },
    "AbpAccountPublic": {
      "BaseUrl": "https://Auth.azurewebsites.net/"
    }
  },
  "Redis": {
    "Configuration": "Test.privatelink.redis.cache.windows.net:6380,password=XXX,ssl=True,abortConnect=False"
  },
  "AuthServer": {
    "Authority": "https://Auth.azurewebsites.net"
  }
}
```

## 備註
目前測試 Redis 不開公開連線時，需要設定私人端點，並且修改連線字串，加上 `privatelink`

- 公開外網
  - DB=xxx.database.windows.net
  - Redis=xxx.redis.cache.windows.net
- 私人端點
  - DB=xxx.privatelink.database.windows.net
  - Redis=xxx.privatelink.redis.cache.windows.net