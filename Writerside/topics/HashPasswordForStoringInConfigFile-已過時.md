# HashPasswordForStoringInConfigFile 已過時

> **原文發布日期:** 2021-03-19
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/03/19/HashPasswordForStoringInConfigFile
> **標籤:** 無

---

System.Web.Security.FormsAuthentication.HashPasswordForStoringInConfigFile

已過時的更新方案筆記 (MD5 & SHA1)

- 引用

```
using System.Security.Cryptography;
```

- SHA1

```
BitConverter.ToString(SHA1.Create().ComputeHash(Encoding.UTF8.GetBytes(str)))
 .Replace("-", null);
```

- MD5

```
BitConverter.ToString(MD5.Create().ComputeHash(Encoding.UTF8.GetBytes(str)))
 .Replace("-", null);
```

- 參照
  [SHA1 類別](https://docs.microsoft.com/zh-tw/dotnet/api/system.security.cryptography.sha1?view=net-5.0)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- .NET Framework
{ignore-vars="true"}
- C#
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
