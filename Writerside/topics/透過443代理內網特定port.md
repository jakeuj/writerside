# 透過443代理內網特定port

[ngrok](https://ngrok.com/docs/guides/device-gateway/linux/)
可以在防火牆未開放443 port外網可以連到指定內網主機 IP 的情況下，透過443 port代理內網特定port。

例如：

```bash
ngrok tcp
443 --remote-addr=0.tcp.ngrok.io:443 --bind-tls=true
--bind-tls=true --region=ap --hostname=0.tcp.ngrok.io:443 --host-header=rewrite
--subdomain=0.tcp.ngrok.io --bind-tls=true --remote-addr=0.tcp.ngrok.io:443
```

這樣就可以透過443 port連到內網特定port。

## 註冊

[ngrok](https://ngrok.com/) 註冊帳號，取得 NGROK_AUTHTOKEN。

## 安裝

```bash
sudo apt install ngrok
```

## 使用

NGROK_AUTHTOKEN: 請替換為你的 ngrok authtoken。

```bash
ngrok authtoken NGROK_AUTHTOKEN
ngrok http --region=ap http://127.0.0.2:8080
```

成功後會拿到一組網址，透過這個網址就可以連到內網特定port。

## 原理

ngrok 會在本地端啟動一個代理伺服器，並將本地或區網的特定 port 綁定到 ngrok 的伺服器上。當外部請求透過 ngrok 的網址訪問時，ngrok 會將請求轉發到本地端的指定位置和port。
這樣就可以在防火牆未開放特定 port 的情況下，透過 ngrok 的網址訪問內網服務。

## 參考

- [ngrok 官方文檔](https://ngrok.com/docs/guides/device-gateway/linux/)
