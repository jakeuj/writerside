# Azure SendGrid Invalid from email address

> **原文發布日期:** 2021-09-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/09/09/Azure-SendGrid-Invalid-from-email-address
> **標籤:** 無

---

筆記一下 SendGrid 驗證寄件者的543

## 情境

有新使用者要共用 SendGrid 帳號額度，需要提供 API Key

### 子帳號

[SendGrid](https://app.sendgrid.com/settings/subusers) 有提供子帳號功能

從 設定 > Subuser 管理 > Create New Subuser

這樣就可以切到子帳號再新增 API Key

信件紀錄與報表分析之類的也會跟主帳號切分開來

Sender 識別與驗證也是獨立的

也就是子帳號要用的 domain 要自己再透過 cname 驗證一遍

如果有多個IP也可以指定某個IP給子帳號來跟主帳號分開

當然如果只有一組IP就只能共用了

### API Key

首先可以針對新的單位創建新的 API Key

從 Azure SendGrid 一路點到管理畫面左邊 Settings > API Key

[發送格柵 (sendgrid.com)](https://app.sendgrid.com/settings/api_keys) > 新增 API Key

新增時需要設定該 API 的權限範圍

沒甚麼事情了話應該只要開寄信權限就好了

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/6e3eb724-eff4-49d7-a070-25d7f96da48c/1631168718.png)

### 寄件者驗證

實際使用該API寄信時可能會遇到以下錯誤 (40x)

Invalid from email address

因為寄件人的 domain 需要先進行所有權驗證

不然就會被擋並觸發以上錯誤

所以需要到設定>寄件人驗證>驗證 Domain > I am not sure.

這邊會需要設定你信箱 domain 的 CName 到 Sendgrid.net

大概長這樣，三條都要設定，設定後按完成，之後就可以發信了。

### Add all of these records to I'm+Not+Sure's DNS section.

| TYPE | HOST |  | VALUE |  |
| --- | --- | --- | --- | --- |
| CNAME | eeeee.jakeuj.com | Copy | uuuuu.wwww.sendgrid.net | Copy |
| CNAME | s1.\_domainkey.jakeuj.com | Copy | s1.domainkey.uuuuu.wwww.sendgrid.net | Copy |
| CNAME | s2.\_domainkey.jakeuj.com | Copy | s2.domainkey.uuuuu.wwww.sendgrid.net | Copy |

### 技術文件

[GitHub - sendgrid/sendgrid-csharp: The Official Twilio SendGrid Led, Community Driven C#, .NetStandard, .NetCore API Library](https://github.com/sendgrid/sendgrid-csharp)

### 範例程式碼

PM> Install-Package SendGrid

|  |  |
| --- | --- |
|  | // using SendGrid's C# Library |
|  | // <https://github.com/sendgrid/sendgrid-csharp> |
|  | using SendGrid; |
|  | using SendGrid.Helpers.Mail; |
|  | using System; |
|  | using System.Threading.Tasks; |
|  |  |
|  | namespace Example |
|  | { |
|  | internal class Example |
|  | { |
|  | private static void Main() |
|  | { |
|  | Execute().Wait(); |
|  | } |
|  |  |
|  | static async Task Execute() |
|  | { |
|  | var apiKey = Environment.GetEnvironmentVariable("NAME\_OF\_THE\_ENVIRONMENT\_VARIABLE\_FOR\_YOUR\_SENDGRID\_KEY"); |
|  | var client = new SendGridClient(apiKey); |
|  | var from = new EmailAddress("[test@example.com](mailto:test@example.com)", "Example User"); |
|  | var subject = "Sending with SendGrid is Fun"; |
|  | var to = new EmailAddress("[test@example.com](mailto:test@example.com)", "Example User"); |
|  | var plainTextContent = "and easy to do anywhere, even with C#"; |
|  | var htmlContent = "<strong>and easy to do anywhere, even with C#</strong>"; |
|  | var msg = MailHelper.CreateSingleEmail(from, to, subject, plainTextContent, htmlContent); |
|  | var response = await client.SendEmailAsync(msg); |
|  | } |
|  | } |
|  | } |

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* SendGrid

* 回首頁

---

*本文章從點部落遷移至 Writerside*
