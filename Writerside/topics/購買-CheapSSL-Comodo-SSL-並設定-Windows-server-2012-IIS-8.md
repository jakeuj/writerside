# 購買 CheapSSL Comodo SSL 並設定 Windows server 2012 IIS 8

> **原文發布日期:** 2020-12-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2020/12/26/SSLIIS
> **標籤:** 無

---

買便宜的憑證

產生憑證申請

完成後綁回站台

之類的筆記下

## **SSL 驗證級別：**

1. 域名型 DV (Domain validated)：只需要驗證網址所有權
2. 企業型 OV (Organization validated)：驗證網址所有權 及 公司登記資料
3. 增強型 EV (Extended validation)：驗證網址所有權 及 公司登記資料，網址列會呈現綠色，並且包含公司名稱

## **SSL 憑證種類：**

1. 單一憑證 (SSL Certificate)：參考價格 = $7.99/年
   domain.com 和 www.domain.com 可以使用，域名必須完全符合

   範例: domain.com, a.domain.com, b.domain.com => 需要買三個單一憑證

   參考：[商店頁面](https://cheapsslsecurity.com/comodo/positivessl.html) 價格 = 參考價格 = $7.99/年
2. 萬用憑證、通配符憑證 (Wildcard SSL Certificate)：參考價格 = $67/年
   \*.domain.com 表示只要網址後面為 domain.com 前面皆可，但注意有分 多層 或 單層。

   範例(同主網域、不同子網域): domain.com, a.domain.com, b.domain.com => 只需要一個萬用憑證
   範例(同主網域、多層不同子網域): a.s1.domain.com, a.s2.domain.com => 如果買單層就要買兩份，多層可以用同一份萬用憑證
   範例(不同主網域): domain1.com, domain2.com => 要買兩份萬用憑證

   參考：[商店頁面](https://cheapsslsecurity.com/comodo/positivessl-wildcard.html) 價格 = 參考價格 = $67/年
3. SAN憑證、多網域憑證 (Multi-Domain SSL Certificate)：
   domain.tw、domain.cn 、domain.jp ... 這種就要使用 SAN 憑證。
   買的時候會內含至少2個SAN，可以添購更多SAN，看實際要使用多少個不同domain而定。

   範例(兩個不同主網域): domain1.com, domain2.com => 可以買一份多網域憑證，內含2個SAN
   範例(三個不同主網域): domain1.com, domain2.com, domain3.com => 可以買一份多網域憑證，但要添購1份SAN，共三個SAN
   範例(同主網域、不同子網域): domain.com, a.domain.com, b.domain.com => 同上，需要三個SAN

   參考：[商店頁面](https://cheapsslsecurity.com/comodo/positive-multi-domainssl.html) 價格 = 基本2SAN $22.99/年，額外加購每SAN $8.9/年
4. SAN萬用憑證 (Multi-Domain Wildcard SSL Certificate)：參考價格 = 基本2SAN $189/年，額外加購每SAN $88/年
   以上兩個 (2.萬用憑證 & 3.多網域憑證) 綜合體。

   範例(同主網域、不同子網域): domain.com, a.domain.com, b.domain.com => 占用一個SAN
   範例(不同主網域、不同子網域): a.domain1.com, b.domain1.com, a.domain2.com, b.domain2.com => 占用兩個SAN

   參考：[商店頁面](https://cheapsslsecurity.com/comodo/positivemultidomain-wildcardssl.html) 價格 = 基本2SAN $189/年，額外加購每SAN $88/年

## SSL 範例**：**

* 環境：Windows server 2012 IIS 8
* 憑證：單一憑證
* 網域：不同主網域

### SSL 流程

1. 建立憑證要求
   Windows Server 2012 => IIS 8 => 服務器證書 => 創建證書申請
   ![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608988876.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608988886.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608991145.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608988902.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608988909.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608988916.png)做到這步要先到網頁購買並建立憑證，建立過程會需要將以上文字檔內容貼到InputCsr欄位。​
2. 購買憑證
   購買網址：<https://cheapsslsecurity.com/comodo/positivessl.html>
   依需求數量購買並完成線上刷卡結帳
3. 建立憑證
   於訂單頁面點擊 Generate Cert 開始建立憑證
   訂單網址：[https://cheapsslsecurity.com/client/ordersummary.html
   ![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608986491.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608986497.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608986507.png)](https://cheapsslsecurity.com/client/ordersummary.html)做到這步需要把IIS產生的文字檔內容複製貼上到中間InputCsr欄位
   ![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608989085.png)接續上一步驟，點完繼續之後會看到以下畫面，請點擊 Download Auth File 按鈕下載驗證檔案到目標站台目錄  /.well-known/pki-validation/
   ![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608990910.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608991529.png)如果剛剛還沒下載驗證檔案，可以在這裡點擊 Download Auth File 按鈕下載到目標站台目錄  /.well-known/pki-validation/
4. 驗證網址
   這邊需要到dns將domain指到目標網站Server的IP並於IIS繫結domain到目標站台​，
   並於該站台根目錄建立 /.well-known/pki-validation/ 資料夾目錄結構
   放入上面下載的驗證檔案 BBFAA6385EB410B8DC58D4D31E871BCC.txt

   ※ 但是Windows目錄不能包含小點點 .
   所以這邊用 添加虛擬目錄 的方式建立對應目錄結構
   ![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608990221.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608989944.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608990206.png)
   確保輸入網址 **http://example.com/.well-known/pki-validation/BBFAA6385EB410B8DC58D4D31E871BCC.txt**
   可以看到該檔案的內容
   ![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608990303.png)到這邊即驗證完URL所有權
5. 完成證書申請
   訂單網址：[https://cheapsslsecurity.com/client/ordersummary.html
   ![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608991862.png)](https://cheapsslsecurity.com/client/ordersummary.html)進去之後下載憑證檔案
   ![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608992232.png)下載並解壓縮之後到 Windows Server 2012 => IIS 8 => 服務器證書 => 完成證書申請
   ![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608992688.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608992765.png)到這就完成了SSL
6. 繫結到網站 https

   ※ 需要服務器名稱指示 千萬記得勾選！
   ![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9f823204-e6ce-4ff8-b15e-bd886efc4f59/1608993181.png)

   ## ※ 需要服務器名稱指示 千萬記得勾選！

* 如果忘記勾，其他網站的憑證可能都會被改成這個，請到其他有綁ssl的網站確認憑證是否正確，有誤請換回正確的憑證並將「需要服務器名稱指示」打勾！

## **到此完成一個網站的一個domain https ssl 憑證申請與綁定！**

**P.S. Windows Server 2008 一個IP只能綁一個domain的https !!!**

參照：[6個步驟完成 CheapSSL 購買 Comodo SSL 憑證及安裝設定](https://cootag.com/Topic/51621-Buy-Cheap-SSL.html)
參照：[How to Install a Certificate](https://knowledge.cheapsslsecurity.com/support/solutions/articles/22000202334-microsoft-iis-8)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* IIS
* SSL

* 回首頁

---

*本文章從點部落遷移至 Writerside*
