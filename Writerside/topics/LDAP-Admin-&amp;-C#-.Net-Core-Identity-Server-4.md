# LDAP Admin &amp; C# .Net Core Identity Server 4

> **原文發布日期:** 2021-07-30
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/07/30/LdapAdmin
> **標籤:** 無

---

LDAP 與 C# .Net Core Identity Server 4 的一些筆記

本身只簡單設定過 Windows Server AD

至於拿來當類資料庫的操作是第一次

首先科普一下

AD：Active Directory（中國大陸譯名為「活動目錄」，台灣為維持英文不譯）

LDAP：輕型目錄存取協定(Lightweight Directory Access Protocol)

由此可知我們一般用AD就來建建員工電腦登入帳號

至於要從其他應用來對AD進行操作需要透過某種協定

也就是 LDAP 輕型目錄存取協定

至於 AD 本身就像是電腦資料夾

C:\Users\jake.chu\Music

類似這種目錄結構的感覺

Com:\Microsoft\Sales\Jake

套用domain的概念他就會反過來

jake.sales.microsoft.com

大概這種感覺

在AD中表達的方式會加上各區段的屬性

CN=Jake,OU=Sales,DC=Microsoft,DC=COM

其中屬性代表意義如下：

LDAP目錄結構組成：

* DN(Distinguished Name)：識別名稱，絕對位置
* RDN(Relative Distinguished Name)：相對識別名稱，相對位置
* CN(Common Name) ：名稱
* OU(Organizational Unit Name)：組織名稱
* O (Organizational Unit )：組織
* DC(Domain Componet)：網域元件

參照：https://blog.xuite.net/tolarku/blog/151029105-LDAP+%E5%9F%BA%E7%A4%8E%E8%AA%AA%E6%98%8E

 LADP 可以先透過 Client 叫做 Ldap Admin 來進行登入取得資料看一下長怎樣

Ldap Admin 下載：http://www.ldapadmin.org/

打開可以設定 AD 的 IP 跟帳號密碼

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/ad5dae73-a042-4b43-8724-0952e0bdc08b/1627623432.png)

其中其實有蠻多選項的，可能需要跟IT詢問一下

像是我這邊是用 GSS-API 才能連得到

如果你本機已經是用 AD 帳號登入

那也可以直接選 使用目前使用者認證

然後左下角色測試連線看能不能連成功

失敗了話可能要多嘗試幾種選項組合

成功就可以連過去看到內容

![](https://dotblogsfile.blob.core.windows.net/user/御星幻/ad5dae73-a042-4b43-8724-0952e0bdc08b/1627623650.png)

參照：https://karatejb.blogspot.com/2019/07/aspnet-core-identity-server-4-ldap.html

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* AD
* LDAP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
