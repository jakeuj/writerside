# Git 移除新增忽略之已推送檔案的追蹤

> **原文發布日期:** 2021-11-24
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/11/24/Git-RM-Cached
> **標籤:** 無

---

誤 Push 之檔案的處理方式

結論

到 PowerShell 下 Git 指令移除已 Push 的東西

* 移除某資料夾

```
git rm -r --cached .\ServiceDependencies\
```

* 移除某檔案

```
git rm --cached profile.arm.json
```

然後把要排除的東西加到忽略檔 .gitgnore

* 忽略資料夾

```
src/MyProject.HttpApi.Host/Properties/ServiceDependencies/*
src/MyProject.IdentityServer/Properties/ServiceDependencies/*
```

* 忽略檔案

```
profile.arm.json
```

或是反過來先加忽略，再全部移除，然後重新追蹤，最後重新 Commit

1. `echo "profile.arm.json" > .gitgnore`
2. `git rm -r --cached .`
3. `git add .`
4. `git commit -m 'update .gitignore'`

參照

[更新成符合 .gitignore 設定的追蹤狀態 (poychang.net)](https://blog.poychang.net/gitignore-and-delete-untracked-files/)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Git](/jakeuj/Tags?qq=Git)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
