# [Git] .gitignore 和.git/info/exclude 的區別

> **原文發布日期:** 2023-12-25
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/12/25/git-exclude
> **標籤:** 無

---

gitignore vs exclude

## 結論

* .gitignore
  + **說明**：顯式地阻止提交檔。
  + **優勢**：.gitignore 檔本身提交至遠端倉庫，全組共用忽略檔配置。
  + **局限**：如果專案已經存在遠程倉庫，即使被加入 .gitignore，仍然可以進行修改並提交。 本地的修改會顯示在 結果中。`git status`
* .git/info/exclude
  + **說明**：顯式地阻止提交檔。
  + **優勢**：exclude 檔本身不會提交至遠端倉庫，因此適合放一些個人定製的 「gitignore」 專案。
  + **局限**：和 .gitignore 存在同樣地局限。 檔若已存在遠端倉庫，則本地修改仍可以提交至遠端倉庫。 本地的修改會顯示在 結果中。`git status`
* assume-unchanged
  + **說明**：聲明本地遠端都**不會修改**這個檔。
  + **優勢**：git 直接跳過這些文件的處理以提升性能。 檔案不會出現在 。`git status`
  + **局限**：不適合本地或遠端需要修改的檔。 本地會忽略掉之後遠端檔的修改。
* skip-worktree
  + **說明**：聲明忽略檔的本地修改。
  + **優勢**：本地可以對檔做一些個人定製。 檔案不會出現在 。`git status`
  + **局限**：拉取遠端檔更新，或切換分支時有可能出現衝突，需要撤銷忽略後手動解決衝突。

參照

[[Git] .gitignore 和.git/info/exclude 的区别 - 簡書 (jianshu.com)](https://www.jianshu.com/p/f42254bc3ffb)

[Git 移除新增忽略之已推送檔案的追蹤 | 御用小本本 - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2021/11/24/Git-RM-Cached)

[Git 小技巧 - 忽略不想要提交的本地修改 | Mengqi's blog (mengqi92.github.io)](https://mengqi92.github.io/2020/07/17/hide-files-from-git/)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Git](/jakeuj/Tags?qq=Git)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
