# OpenIddict

紀錄一下登入登出的事情

## 登出

1. 首先找到設定檔，通常位於 AuthServer 的 /.well-known/openid-configuration
例如：https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration
2. 裡面會有 OAuth2 的設定，找到 `end_session_endpoint` 就是登出的網址
例如：`"end_session_endpoint": "https://login.microsoftonline.com/common/oauth2/v2.0/logout"`
3. 然後我們就可以在需要登出的時候導向這個網址，例如：
`https://auth.domain.com/connect/logout?post_logout_redirect_uri=https%3A%2F%2Fwww.domain.com`
4. 其中 `post_logout_redirect_uri` 需到 Application (OpenIddict) 裡面設定

- Allow logout endpoint：勾選
- Post logout redirect uris：裡面加入登出後要導向的網址
  
這樣登出後才會導向正確的網址

  ![logout.png](logout.png){style="block"}
