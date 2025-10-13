# Git Credential Manager for Windows

> **原文發布日期:** 2024-03-06
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/03/06/Git-Credential-Manager
> **標籤:** 無

---

筆記下 Git 認證的事情

## 結論

安裝

[Releases · git-ecosystem/git-credential-manager (github.com)](https://github.com/git-ecosystem/git-credential-manager/releases)

上面是最新的有 MFA，下面是舊的誤裝會各種登不了

[~~Releases · microsoft/Git-Credential-Manager-for-Windows (github.com)~~](https://github.com/microsoft/Git-Credential-Manager-for-Windows/releases)

如有卡到舊的陰可能要清除舊的 `credential` 區段

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/f9e1de8c-04e1-437f-aa74-8b2b9d8de6b4/1709714123.png.png)

以下是清除後應該長成(乾淨)的樣子

### .gitconfig

* 本地
  + 清空
* 全域

```
[user]
name = jake.chu
email = jakeuj@hotmail.com
```

* 系統

```
[diff "astextplain"]
textconv = astextplain
[filter "lfs"]
clean = git-lfs clean -- %f
smudge = git-lfs smudge -- %f
process = git-lfs filter-process
required = true
[http]
sslBackend = openssl
sslCAInfo = C:/Program Files/Git/mingw64/etc/ssl/certs/ca-bundle.crt
[core]
autocrlf = true
fscache = true
symlinks = false
[pull]
rebase = false
[credential]
helper = manager
[credential "https://dev.azure.com"]
useHttpPath = true
[init]
defaultBranch = master
```

## 參照

[介紹好用工具：Git Credential Manager for Windows (記憶 Git 常用密碼) | The Will Will Web (miniasp.com)](https://blog.miniasp.com/post/2016/02/01/Useful-tool-Git-Credential-Manager-for-Windows)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* 回首頁

---

*本文章從點部落遷移至 Writerside*
