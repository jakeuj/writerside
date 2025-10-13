# C# System.Net.Mail SmtpClient From DisplayName 小括號加中文會消失

> **原文發布日期:** 2023-01-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/01/09/CSharp-System-Net-Mail-SmtpClient-From-DisplayName-Chinese
> **標籤:** 無

---

DisplayName 設定 "Test Mail (測試信件)" 但收信時卻顯示 "Test Mail"

## 問題

`MailMessage.From.DisplayName`

有小括號 => 會被吃字

* Test Mail (測試信件) => Test Mail
* Test Mail (x測x試x信x件x) => Test Mail

沒小括號 => 沒問題

* Test Mail 測試信件 => Test Mail 測試信件

改用全形括號 => 沒問題

* Test Mail（測試信件） => Test Mail（測試信件）

有小括號沒中文 => 沒問題

* Test Mail (xxx) => Test Mail (xxx)

### 測試

```
[Fact]
public async Task Should_Get_Chinese_From_Mail()
{
    // Arrange
    const string displayName = "Test (x測x試x)";

    var mail = new MailMessage
    {
        Subject = "測試小括號中文",
        Body = "有括號時中文會被消失",
        From = new MailAddress(
            "jakeuj@hotmail.com", displayName, Encoding.UTF8)
    };

    mail.To.Add("jakeuj@gmail.com");

    //Act
    using (var smtpClient = new SmtpClient("smtp.gmail.com", 587)
           {
               UseDefaultCredentials = false,
               EnableSsl = true,
               //這裡要填正確的帳號跟密碼
               Credentials = new NetworkCredential("apikey", "apikeyvalue")
           })
    {
        await smtpClient.SendMailAsync(mail);
    }

    //Assert
    _testOutputHelper.WriteLine(displayName);
    displayName.ShouldNotBeNull();
}
```

### 結論

[iis - How to send email locally in .net core without credentials - Stack Overflow](https://stackoverflow.com/questions/58937302/how-to-send-email-locally-in-net-core-without-credentials)

[耕作筆記本: [筆記] .Net SmtpClient 發出的信,特定中文寄件人在特定收信軟體上亂碼問題 (jumping-fun.blogspot.com)](https://jumping-fun.blogspot.com/2019/01/dot-net-smtpclient-mojibake.html)

### 參照

[用C#寄Gmail信(純後端) - iT 邦幫忙::一起幫忙解決難題，拯救 IT 人的一天 (ithome.com.tw)](https://ithelp.ithome.com.tw/articles/10190120)

[原來 System.Net.Mail 也會有 Bug ... — 安德魯的部落格 (chicken-house.net)](https://columns.chicken-house.net/2007/04/06/%E5%8E%9F%E4%BE%86-system-net-mail-%E4%B9%9F%E6%9C%83%E6%9C%89-bug/)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [SMTP](/jakeuj/Tags?qq=SMTP)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
