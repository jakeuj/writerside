# 圖形驗證服務 hcaptcha dotnet core 實作筆記

> **原文發布日期:** 2021-01-28
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/01/28/hCaptcha
> **標籤:** 無

---

hcaptcha 是一套免費圖形驗證服務

Cloudflare 就宣布換掉 Google reCAPTCHA

改成可在中國等地使用的 hCaptcha

這邊主要紀錄一下 dotnet core 實作流程

##

## 簡介

> „CDN及安全服務業者Cloudflare就宣布換掉Google reCAPTCHA，改用hCaptcha
>
> „不出售個人資料，僅蒐集必要的個人資訊，且明白揭露
>
> „速度和解析率都優於競爭對手
>
> „提供視障等其他不便人士的輔助功能
>
> „可在中國等地使用
>
> „產生新CAPTCHA也相當快速

## 新增 .NetCore (5.0) WebApplication 專案

### 註冊帳號申請服務

官方網站 https://www.hcaptcha.com/

申請完之後要將網站的網域加入設定

https://dashboard.hcaptcha.com/sites?page=1

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/ff27ddb8-8aab-4e5f-bd89-a95de4a4565a/1611801003.png)這邊必須要是可以成功從外部dns解析的網站，也不能是localhost​

開發階段要將測試網址解析到本地以利開發測試

C:\Windows\System32\drivers\etc\hosts

```

# For hcaptcha test
127.0.0.1 google.com
```

沒自己網址可能可以先用比如 **google.com** 來做設定

參照：https://blog.gtwang.org/windows/windows-linux-hosts-file-configuration/

### 共用樣板 Pages\Shared\\_Layout.cshtml

head 附加 api.js

```html
<script src="https://hcaptcha.com/1/api.js" async defer></script>
```

```html
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>@ViewData["Title"] - WebApplicationHcaptcha</title>
    <link rel="stylesheet" href="~/lib/bootstrap/dist/css/bootstrap.min.css" />
    <link rel="stylesheet" href="~/css/site.css" />
    <script src="https://hcaptcha.com/1/api.js" async defer></script>
</head>
```

### 前端頁面 Pages\Index.cshtml

新增 form 加入 h-captcha div

```

<div class="text-center">
    <h1 class="display-4">Jake's Hcaptcha Lab</h1>>
    <form method="post">
        <div class="h-captcha" data-sitekey="daf22222-f90e-43cb-8533-6774a363506c"></div>
        <input type="submit" />
    </form>
</div>
```

其中 `data-sitekey="daf22222-f90e-43cb-8533-6774a363506c"`

需換成你自己申請的 sitekey

由此取得 https://dashboard.hcaptcha.com/sites?page=1

### 後端程式 Pages\Index.cshtml.cs

注入 IHttpClientFactory

```

private readonly IHttpClientFactory _clientFactory;
private readonly ILogger<IndexModel> _logger;

public IndexModel(ILogger<IndexModel> logger, IHttpClientFactory clientFactory)
{
	_logger = logger;
	_clientFactory = clientFactory;
}
```

新增 回傳 DTO

```

class Hcaptcha
{
	public bool success { get; set; }
	public DateTime challenge_ts { get; set; }
	public string hostname { get; set; }
}
```

處理 POST 要求

```

public async Task<IActionResult> OnPostAsync()
{
	var token = Request.Form["h-captcha-response"];
	var secret = "0xc55C202E9c857A09758fB6e3C13437b70Ee33333";
	var url = $"https://hcaptcha.com/siteverify?response={token}&secret={secret}";

	var client = _clientFactory.CreateClient();
	using var response = await client.PostAsync(url, null);
	using var contentStream = await response.Content.ReadAsStreamAsync();
	var result = await JsonSerializer.DeserializeAsync<Hcaptcha>(contentStream);

	if (result.success)
	{
		// do somthing...
		return RedirectToPage("./Privacy");
	}
	else
	{
		// reject
		return RedirectToPage("./Error");
	}
}
```

 其中 secret 要換成你自己申請的 serect

由此取得 https://dashboard.hcaptcha.com/settings

### 修改開發階段執行網址

Properties\launchSettings.json

將 applicationUrl 中的 localhost 改成你的網址 (example: google.com)

```

"WebApplicationHcaptcha": {
  "commandName": "Project",
  "dotnetRunMessages": "true",
  "launchBrowser": true,
  "applicationUrl": "https://google.com:5001;http://google.com:5000",
  "environmentVariables": {
	"ASPNETCORE_ENVIRONMENT": "Development"
  }
}
```

最後執行 WebApplicationHcaptcha 就可以測試圖形驗證是否成功

參照：官方API技術說明文件 https://docs.hcaptcha.com/

參考：https://www.ithome.com.tw/news/136936​

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* C#
{ignore-vars="true"}
* .Net Core
{ignore-vars="true"}
* HttpClinet
* hcaptcha

* 回首頁

---

*本文章從點部落遷移至 Writerside*
