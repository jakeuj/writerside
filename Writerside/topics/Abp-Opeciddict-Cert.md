# Azure-Abp-Opeciddict-Cert

Azure App Service 的 Abp 網站忽然無法正常啟動，Log 顯示錯誤關於 `X.509 encryption credentials`

## 結論
1. 於本機輸入輸入以下指令來產生新的開發憑證

    ```powershell
    dotnet dev-certs https --clean
    dotnet dev-certs https -v -ep .\openiddict.pfx -p YourCertificatePassword
    Get-PfxCertificate -FilePath .\openiddict.pfx | Select Subject, NotAfter
    dotnet dev-certs https --trust
    ```

2. 並將憑證上傳到 Azure App Service 的憑證設定中
3. 將 openiddict 讀取憑證邏輯改成讀取指定指紋 
[Azure-App-Service-CICD-deployment](ABP.IO-WEB應用程式框架-Azure-App-Service-CICD-deployment.md)
4. 將環境變數中的指紋改成第二步驟所上傳的憑證指紋

## 徵狀
abp 網站重啟時無法正常啟動，會出現以下錯誤訊息

    ```
    An unhandled exception was thrown by the application.
    System.InvalidOperationException: 
    When using X.509 encryption credentials, 
    at least one of the registered certificates must be valid.
    To use key rollover, 
    register both the new certificate 
    and the old one in the credentials collection.
    ```
## 問題

Azure App Service 上部署 Abp 專案，
因其內使用 OpenIddict 來實作 OAuth2 會用到 dotnet 開發憑證來加密 JWT，
而憑證每一年會過期，屆時沒有提前更新就會遇到憑證問題。

## 解法
目前採用修改讀取憑證邏輯：
[Azure-App-Service-CICD-deployment](ABP.IO-WEB應用程式框架-Azure-App-Service-CICD-deployment.md)
並定期重新產生新憑證上傳並且更新指紋的方式來使 openiddict 可以正常運作。

## 產生憑證指令

```powershell
# 清除現有開發憑證
dotnet dev-certs https --clean

# 重新建立並匯出 PFX
dotnet dev-certs https -v -ep openiddict.pfx -p YourCertificatePassword

# Windows（以管理員執行）
dotnet dev-certs https --trust

# macOS（會打開 keychain 同意）
dotnet dev-certs https --trust

# 檢查 PFX 的到期日
Get-PfxCertificate -FilePath .\openiddict.pfx | Select-Object Subject, NotBefore, NotAfter
```

## 上傳憑證
Azure App Service > 憑證 > 攜帶您自己的憑證(.pfx) > 新增憑證 > 指紋 > 複製

## 更新指紋
Azure App Service > 環境變數 > OpenIddict:EncryptionCertificateThumbprint > 貼上指紋

    P.S. WEBSITE_LOAD_CERTIFICATES 不知道能不能

## 參考
Abp 官方針對此問題的疑難排解文章
[dotnet dev-certs](https://abp.io/community/articles/fixing-openiddict-certificate-issues-in-iis-or-azure-0znavo8r#gsc.tab=0:~:text=and%20Azure%20environments.-,Troubleshooting,-Guide)