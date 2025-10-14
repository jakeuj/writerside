# Azure VPN Windows Server 2012 R2 Error 812

> **原文發布日期:** 2022-06-15
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/06/15/AzureVpnWindowsServer2012R2Error812
> **標籤:** 無

---

因為您 RAS/VPN 伺服器設定的原則，連線被禁止。明確的說，伺服器用於檢查您使用者名稱與密碼的驗證方法不符合您連線設定檔設定的驗證方法。請連絡 RAS 伺服器的系統管理員並通知他們這個錯誤。 (錯誤 812)

結論

使用管理員身分執行以下命令

(開始>右鍵>命令提示字元>以管理者身分執行)

```batch
reg add HKLM\SYSTEM\CurrentControlSet\Services\RasMan\PPP\EAP\13 /v TlsVersion /t REG_DWORD /d 0xfc0
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings\WinHttp" /v DefaultSecureProtocols /t REG_DWORD /d 0xaa0
if %PROCESSOR_ARCHITECTURE% EQU AMD64 reg add "HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Internet Settings\WinHttp" /v DefaultSecureProtocols /t REG_DWORD /d 0xaa0
```
{ignore-vars="true"}

原由

現在很多服務都只能走 TLS 1.2

但舊系統即便更新後有支援 TLS 1.2

但是不特別設定了話還是不會走 1.2

總之首先可以了話請安裝最新版 Windows Server

如果不能之後遇到連線問題請優先把 TLS 1.2 開起來

在不能就把 Windows Update 到最新版

再考慮其他解決方案可能可以比較省時間

參照：[connection problem on VPN due to RAS/VPN policy/ Error 812 (microsoft.com)](https://social.technet.microsoft.com/Forums/ie/en-US/b8489bc2-e64b-4b5d-a8bb-0f63ced99fcc/connection-problem-on-vpn-due-to-rasvpn-policy-error-812?forum=winserveressentials)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Azure
* Windows Server
{ignore-vars="true"}
* Azure VPN
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
