# OpenSSL 憑證格式轉換

> **原文發布日期:** 2024-03-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/03/26/ssl--pfx-openssl
> **標籤:** 無

---

筆記一下更新 SSL

## CMD

加入路徑環境變數

`set PATH=%PATH%;C:\Program Files\Git\usr\bin`

轉出 伺服器憑證檔 cer

`openssl pkcs12 -in server.pfx -nokeys -password "pass:vEryComPleXPw" -out - 2>nul | openssl x509 -out server.crt`

轉出 私密金鑰檔 key

`openssl pkcs12 -in server.pfx -nocerts -password "pass:vEryComPleXPw" -nodes -out server.key`

打開並複製 `server.crt` & `server.key`

`explorer .`

替換 apache 原本指定的網站憑證檔案

## 參照

[常見的PowerShell 輸出訊息的 2 種方法 | 御用小本本 - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2024/03/26/powershell-output-to-file)

[如何在收到 PFX 或 CER 憑證檔之後使用 OpenSSL 進行常見的格式轉換 | The Will Will Web (miniasp.com)](https://blog.miniasp.com/post/2019/04/17/Convert-PFX-and-CER-format-using-OpenSSL)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Apache
- SSL

- 回首頁

---

*本文章從點部落遷移至 Writerside*
