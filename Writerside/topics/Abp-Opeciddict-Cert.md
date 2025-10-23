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

## 生產環境 CA 憑證申請與配置

### OpenIddict 憑證需求說明

OpenIddict 需要兩種憑證:
1. **Signing Certificate (簽章憑證)**: 用於簽署 JWT token,確保 token 的真實性
2. **Encryption Certificate (加密憑證)**: 用於加密敏感資料,保護 token 內容

**重要**: 可以使用同一張憑證同時作為簽章和加密用途,不需要分別申請兩張憑證。

### 方案一: 使用 Let's Encrypt 免費 CA 憑證

Let's Encrypt 提供免費的 SSL/TLS 憑證,適合中小型專案。

#### 使用 Certbot 申請 (適用於有獨立伺服器的情況)

```bash
# 安裝 Certbot (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install certbot

# 申請憑證 (需要有網域名稱)
sudo certbot certonly --standalone -d yourdomain.com

# 憑證會儲存在
# /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem

# 轉換為 PFX 格式 (OpenIddict 需要)
sudo openssl pkcs12 -export \
  -out openiddict.pfx \
  -inkey /etc/letsencrypt/live/yourdomain.com/privkey.pem \
  -in /etc/letsencrypt/live/yourdomain.com/fullchain.pem \
  -password pass:YourStrongPassword
```

#### 使用 Azure App Service 託管憑證 (推薦)

Azure App Service 可以自動管理 Let's Encrypt 憑證:

1. **前往 Azure Portal** → 您的 App Service → **憑證** → **託管憑證**
2. 點選 **新增憑證**
3. 選擇您的自訂網域
4. Azure 會自動申請並續期 Let's Encrypt 憑證
5. 憑證會自動載入到 App Service,可透過 `WEBSITE_LOAD_CERTIFICATES` 環境變數存取

**注意**: 託管憑證主要用於 HTTPS,若要用於 OpenIddict,需要額外匯出為 PFX 格式。

### 方案二: 使用商業 CA 憑證

適合企業級應用,提供更長效期和更高信任度。

#### 推薦的 CA 供應商

- **DigiCert**: 業界標準,提供 EV 憑證
- **GlobalSign**: 適合國際企業
- **Sectigo (原 Comodo)**: 性價比高
- **GoDaddy**: 適合中小企業

#### 申請流程

1. **生成 CSR (Certificate Signing Request)**

```powershell
# Windows PowerShell
$cert = New-SelfSignedCertificate `
  -Subject "CN=yourdomain.com" `
  -KeyAlgorithm RSA `
  -KeyLength 2048 `
  -NotAfter (Get-Date).AddYears(2) `
  -CertStoreLocation "Cert:\CurrentUser\My" `
  -KeyExportPolicy Exportable `
  -KeyUsage DigitalSignature, KeyEncipherment

# 匯出 CSR
$csr = [System.Convert]::ToBase64String($cert.GetRawCertData())
$csr | Out-File -FilePath "request.csr"
```

或使用 OpenSSL:

```bash
# 生成私鑰
openssl genrsa -out private.key 2048

# 生成 CSR
openssl req -new -key private.key -out request.csr \
  -subj "/C=TW/ST=Taiwan/L=Taipei/O=YourCompany/CN=yourdomain.com"
```

2. **提交 CSR 到 CA 供應商**
   - 登入 CA 供應商網站
   - 選擇憑證類型 (建議選擇 Code Signing 或 Standard SSL)
   - 上傳 CSR 檔案
   - 完成網域驗證 (DNS、Email 或 HTTP 驗證)

3. **下載簽發的憑證**
   - CA 會提供 `.crt` 或 `.cer` 檔案
   - 可能還會提供中繼憑證 (intermediate certificate)

4. **轉換為 PFX 格式**

```bash
# 合併憑證和私鑰為 PFX
openssl pkcs12 -export \
  -out openiddict.pfx \
  -inkey private.key \
  -in certificate.crt \
  -certfile intermediate.crt \
  -password pass:YourStrongPassword
```

### 方案三: 使用 Azure Key Vault 憑證 (最佳實踐)

Azure Key Vault 可以自動管理憑證生命週期,包括自動續期。

#### 在 Key Vault 中建立憑證

```bash
# 使用 Azure CLI
az keyvault certificate create \
  --vault-name YourKeyVaultName \
  --name openiddict-cert \
  --policy @policy.json
```

**policy.json 範例**:
```json
{
  "issuerParameters": {
    "name": "Self",
    "certificateTransparency": null
  },
  "keyProperties": {
    "exportable": true,
    "keyType": "RSA",
    "keySize": 2048,
    "reuseKey": false
  },
  "secretProperties": {
    "contentType": "application/x-pkcs12"
  },
  "x509CertificateProperties": {
    "subject": "CN=yourdomain.com",
    "validityInMonths": 12,
    "keyUsage": [
      "digitalSignature",
      "keyEncipherment"
    ]
  },
  "lifetimeActions": [
    {
      "trigger": {
        "daysBeforeExpiry": 30
      },
      "action": {
        "actionType": "AutoRenew"
      }
    }
  ]
}
```

#### 在程式中使用 Key Vault 憑證

```csharp
// 安裝套件
// dotnet add package Azure.Security.KeyVault.Certificates
// dotnet add package Azure.Identity

using Azure.Identity;
using Azure.Security.KeyVault.Certificates;
using System.Security.Cryptography.X509Certificates;

public override void PreConfigureServices(ServiceConfigurationContext context)
{
    var configuration = context.Services.GetConfiguration();
    var hostingEnvironment = context.Services.GetHostingEnvironment();

    if (!hostingEnvironment.IsDevelopment())
    {
        PreConfigure<AbpOpenIddictAspNetCoreOptions>(options =>
        {
            options.AddDevelopmentEncryptionAndSigningCertificate = false;
        });

        PreConfigure<OpenIddictServerBuilder>(serverBuilder =>
        {
            var keyVaultUrl = configuration["KeyVault:Url"];
            var certificateName = configuration["KeyVault:CertificateName"];

            if (!string.IsNullOrEmpty(keyVaultUrl) && !string.IsNullOrEmpty(certificateName))
            {
                var client = new CertificateClient(
                    new Uri(keyVaultUrl),
                    new DefaultAzureCredential()
                );

                // 下載憑證
                var certificateResponse = client.DownloadCertificate(certificateName);
                var certificate = certificateResponse.Value;

                // 同時用於簽章和加密
                serverBuilder.AddSigningCertificate(certificate);
                serverBuilder.AddEncryptionCertificate(certificate);
            }
        });
    }
}
```

**appsettings.json 設定**:
```json
{
  "KeyVault": {
    "Url": "https://your-keyvault.vault.azure.net/",
    "CertificateName": "openiddict-cert"
  }
}
```

### 憑證要求規格

OpenIddict 對憑證的要求:

- **金鑰類型**: RSA
- **金鑰長度**: 至少 2048 位元 (建議 4096 位元)
- **金鑰用途**: Digital Signature, Key Encipherment
- **格式**: PFX/PKCS#12 (需包含私鑰)
- **效期**: 建議 1-2 年 (配合自動續期機制)

### 憑證安全最佳實踐

1. **絕不將憑證檔案提交到版控系統** (加入 `.gitignore`)
2. **使用強密碼保護 PFX 檔案** (至少 16 字元,包含大小寫、數字、符號)
3. **定期輪換憑證** (建議每年更新)
4. **使用 Key Vault 或 Azure App Service 憑證儲存** (避免將憑證放在專案目錄)
5. **啟用憑證到期監控** (Azure Monitor 或第三方服務)
6. **實作 Key Rollover 機制** (同時註冊新舊憑證,平滑過渡)

### Key Rollover 實作範例

```csharp
PreConfigure<OpenIddictServerBuilder>(serverBuilder =>
{
    // 載入新憑證 (主要)
    var newCert = LoadCertificateFromKeyVault("openiddict-cert-2025");
    serverBuilder.AddSigningCertificate(newCert);
    serverBuilder.AddEncryptionCertificate(newCert);

    // 保留舊憑證 (用於驗證舊 token)
    var oldCert = LoadCertificateFromKeyVault("openiddict-cert-2024");
    serverBuilder.AddSigningCertificate(oldCert);
    serverBuilder.AddEncryptionCertificate(oldCert);
});
```

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

- [OpenIddict 官方說明 在生產環境中，建議使用兩個 RSA 憑證，與用於 HTTPS 的憑證不同：一個用於加密，一個用於簽署。您可以使用 .NET Core API 在本機產生憑證和自我簽署](https://documentation.openiddict.com/configuration/encryption-and-signing-credentials.html#registering-a-certificate-recommended-for-production-ready-scenarios)
- [Azure App Service 憑證自動化](https://learn.microsoft.com/en-us/azure/app-service/configure-ssl-certificate)
- [Key Vault 憑證自動續期](https://learn.microsoft.com/en-us/azure/key-vault/certificates/certificate-scenarios)
