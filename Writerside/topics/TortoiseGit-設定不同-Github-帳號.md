# TortoiseGit 設定不同 Github 帳號

> **原文發布日期:** 2023-11-03
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/11/03/tortoisegit-multiple-github-repositories
> **標籤:** 無

---

筆記下如何跨帳號存取 repo

## 結論

.\.get\config

```
[core]
 repositoryformatversion = 0
 filemode = false
 bare = false
 logallrefupdates = true
 symlinks = false
 ignorecase = true
[submodule]
 active = .
[remote "origin"]
 url = https://jakeuj@github.com/Org/ChatDemoByVertexAI.git
 fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
 remote = origin
 merge = refs/heads/main
```

將 `origin` 裡面的 `url` 加上 帳號@ 來切換不同 github 帳號

### 參照

[git - TortoiseGit - Multiple GitHub repositories with different key pairs each - Stack Overflow](https://stackoverflow.com/questions/41291043/tortoisegit-multiple-github-repositories-with-different-key-pairs-each/41292048#41292048)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Github

- 回首頁

---

*本文章從點部落遷移至 Writerside*
