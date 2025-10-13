# Azure VPN 錯誤 720

> **原文發布日期:** 2023-10-25
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/10/25/Azure-vpn-720
> **標籤:** 無

---

錯誤 720：無法連線到 VPN 連線

## 結論

1. 開**啟 裝置管理員**。
2. 以滑鼠右鍵按一下名稱開頭為 「WAN Miniport」 的所有網路介面卡，然後選取 [ **卸載裝置]**。 以下是您可能會觀察到的一些介面卡：
   * WAN Miniport (IP)
   * WAN Miniport (IPv6)
   * WAN Miniport (GRE)
   * WAN Miniport (L2TP)
   * WAN Miniport (網路監視器)
   * WAN Miniport (PPPOE)
   * WAN Miniport (PPTP)
   * WAN Miniport (SSTP)
3. 在 [裝置管理員] 功能表列上，選取 [**動作**>**掃描] 以取得硬體變更**。 這會自動重新安裝 WAN Miniport 裝置。

## 參照

[當您嘗試建立 VPN 連線時，發生「錯誤 720：無法連線到 VPN 連線」 - Windows Server | Microsoft Learn](https://learn.microsoft.com/zh-tw/troubleshoot/windows-server/networking/troubleshoot-error-720-when-establishing-a-vpn-connection#scenario-3-reinstall-wan-miniport-ip-interface-drivers)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Azure VPN](/jakeuj/Tags?qq=Azure%20VPN)
{ignore-vars="true"}

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
