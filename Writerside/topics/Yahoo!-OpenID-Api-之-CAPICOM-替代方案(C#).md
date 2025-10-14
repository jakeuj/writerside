# Yahoo OpenID CAPICOM 替代

> **原文發布日期:** 2012-10-08
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2012/10/08/76334
> **標籤:** 無

---

Yahoo! OpenID Api 之 CAPICOM 替代方案

有鑑於CAPICOM只有32位元版本，用起來不是很方便，乾脆自己繞過CAPICOM處理，就結果而言其實也沒幾行程式碼@@

如果還是對CAPICOM有需求可以參考我之前寫得這篇

http://www.dotblogs.com.tw/jakeuj/archive/2012/03/03/70494.aspx

---

原本範例程式碼

---

```

Set Hash = Server.CreateObject("CAPICOM.HashedData.1")
Const SHA1 = 0
Const MD5 = 3
Hash.Algorithm = SHA1
Hash.Hash(Convert2Bytes(buf))
buf = Hash.Value
Set Util = Server.CreateObject("CAPICOM.Utilities.1")
buf = Util.HexToBinary(buf)
b64 = Util.Base64Encode(buf)
```

---

替代程式碼

---

```

protected string b64(string buf)
{
    return Convert.ToBase64String(HexStringToBytes(SHA1_Encrypt(buf)));
}
protected static byte[] HexStringToBytes(string hex)
{
    byte[] data = new byte[hex.Length / 2];
    int j = 0;
    for (int i = 0; i < hex.Length; i += 2)
    {
        data[j] = Convert.ToByte(hex.Substring(i, 2), 16);
        ++j;
     }
     return data;
}
protected string SHA1_Encrypt(string Source_String)
{
    byte[] StrRes = Encoding.Default.GetBytes(Source_String);
    HashAlgorithm iSHA = new SHA1CryptoServiceProvider();
    StrRes = iSHA.ComputeHash(StrRes);
    StringBuilder EnText = new StringBuilder();
    foreach (byte iByte in StrRes)
       EnText.AppendFormat("{0:x2}", iByte);
    return EnText.ToString();
}
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* C#
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
