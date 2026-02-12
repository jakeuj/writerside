# ✅ OpenIddict 憑證最佳實踐：Azure Key Vault 自動輪替方案

## 🎯 目標

讓 **OpenIddict 的 JWT 簽章／加密憑證** 自動輪替、不影響舊 Token 驗證、並維持高安全性。

---

## 🧩 架構概要

1. 憑證存放於 **Azure Key Vault** 並啟用 **Auto-Renew**。
2. App Service 透過 **Managed Identity** 存取 Key Vault。
3. OpenIddict 啟動時自動載入所有有效憑證，挑最新版本簽 Token。

---

## ⚙️ 程式碼範例

```c#
PreConfigure<OpenIddictServerBuilder>(builder =>
{
    var configuration = context.Services.GetConfiguration();
    var keyVaultUrl = configuration["KeyVault:Url"];
    var secretName = configuration["KeyVault:SigningCertificate"];

    var secretClient = new SecretClient(new Uri(keyVaultUrl), new DefaultAzureCredential());
    var secretProperties = secretClient.GetPropertiesOfSecretVersions(secretName);
    var certs = new List<X509Certificate2>();

    foreach (var prop in secretProperties)
    {
        var secret = secretClient.GetSecret(prop.Name, prop.Version);
        var certBytes = Convert.FromBase64String(secret.Value.Value);
        var cert = new X509Certificate2(certBytes, (string?)null, X509KeyStorageFlags.MachineKeySet);
        if (DateTime.UtcNow >= cert.NotBefore && DateTime.UtcNow <= cert.NotAfter)
            certs.Add(cert);
    }

    foreach (var cert in certs.OrderByDescending(c => c.NotAfter))
    {
        builder.AddSigningCertificate(cert);
        builder.AddEncryptionCertificate(cert);
    }
});
```

---

## 🔧 policy.json 自動輪替設定

```json
{
  "issuerParameters": { "name": "Self" },
  "keyProperties": {
    "exportable": true,
    "keyType": "RSA",
    "keySize": 2048,
    "reuseKey": false
  },
  "secretProperties": { "contentType": "application/x-pkcs12" },
  "x509CertificateProperties": {
    "subject": "CN=yourdomain.com",
    "validityInMonths": 12,
    "keyUsage": [ "digitalSignature", "keyEncipherment" ]
  },
  "lifetimeActions": [
    {
      "trigger": { "daysBeforeExpiry": 30 },
      "action": { "actionType": "AutoRenew" }
    }
  ]
}
```

---

## 🧰 Azure CLI 建立指令

```bash
az keyvault create -n your-keyvault -g your-rg -l eastasia

az keyvault certificate create   --vault-name your-keyvault   --name AuthServerCertificate   --policy @policy.json
```

---

## 💰 成本

Key Vault 憑證自動輪替幾乎免費，每月僅需幾毛錢（< NT$3/月）。

---

## ✅ 結論

此方案完全自動化，無需手動上傳 `.pfx` 或更新指紋，並可確保舊 Token 繼續有效，  
是 **OpenIddict 在 Azure 上的最佳實踐**。
