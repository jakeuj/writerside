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

---

## 憑證自動化管理與最佳實踐

### 問題說明
OpenIddict 若使用 dotnet dev-certs 產生的開發憑證，僅有一年效期，過期會導致服務中斷。手動更新容易遺漏，建議採用自動化與雲端憑證管理。

### 更佳解法

#### 1. 使用 Azure Key Vault 管理憑證
- **自動續期**：將 JWT 加密/簽章憑證託管於 Azure Key Vault，並設定自動續期。
- **App Service 整合**：App Service 可直接存取 Key Vault 憑證，無需手動上傳。
- **程式自動載入**：OpenIddict 支援從 Key Vault 讀取憑證，程式碼可自動根據指紋或名稱載入最新憑證。

**程式碼範例（Startup/Program.cs）**：
```csharp
// ...existing code...
var keyVaultUrl = Environment.GetEnvironmentVariable("KEYVAULT_URL");
var certificateName = Environment.GetEnvironmentVariable("OPENIDDICT_CERT_NAME");
if (!string.IsNullOrEmpty(keyVaultUrl) && !string.IsNullOrEmpty(certificateName))
{
    var client = new SecretClient(new Uri(keyVaultUrl), new DefaultAzureCredential());
    var certificate = new X509Certificate2(Convert.FromBase64String(
        client.GetSecret(certificateName).Value.Value));
    openIddictBuilder.AddEncryptionCertificate(certificate);
}
// ...existing code...
```
- 需安裝 `Azure.Security.KeyVault.Secrets` 與 `Azure.Identity` 套件。

#### 2. 自動化腳本定期更新憑證
- 可用 GitHub Actions、Azure CLI 或 PowerShell 定期產生新憑證並自動上傳至 Key Vault 或 App Service。
- 參考 [Microsoft 官方自動化腳本](https://learn.microsoft.com/en-us/azure/app-service/configure-ssl-certificate#automate-certificate-renewal)。

#### 3. 生產環境建議
- 生產環境請勿使用 dev-certs，建議使用 CA 簽發的正式憑證，並託管於 Key Vault 或 App Service 憑證儲存區。

---

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

- [OpenIddict 官方 Key Vault 整合說明](https://documentation.openiddict.com/configuration/encryption-and-signing-credentials.html#using-azure-key-vault)
- [Azure App Service 憑證自動化](https://learn.microsoft.com/en-us/azure/app-service/configure-ssl-certificate)
- [Key Vault 憑證自動續期](https://learn.microsoft.com/en-us/azure/key-vault/certificates/certificate-scenarios)
