# [Git] 跳過工作樹以忽略本地變更

> **原文發布日期:** 2023-12-25
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/12/25/git-update-index--skip-worktree
> **標籤:** 無

---

git update-index --skip-worktree /path/to/file

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/446535fc-9ec2-42a3-b435-211905200e00/1703495445.png.png)

## 結論

* commit 時選擇 跳過工作樹
* `git update-index --skip-worktree .\path\to\file`
* 遇到衝突 `git update-index --no-skip-worktree .\path\to\file`

## 說明

有些檔案我們不想將變更同步到 Git

比如：appsettings.secrets.json

因為這個檔案內容就是為了將敏感資料分離出來

但每次用這檔案又會問你要不要 commit

這時就可以用 skip-worktree 來避開這類檔案

## 參照

[[Git] .gitignore 和.git/info/exclude 的區別 | 御用小本本 - 點部落 (dotblogs.com.tw)](https://www.dotblogs.com.tw/jakeuj/2023/12/25/git-exclude)

[Git 小技巧 - 忽略不想要提交的本地修改 | Mengqi's blog (mengqi92.github.io)](https://mengqi92.github.io/2020/07/17/hide-files-from-git/)

[idea中好用的git shelve changes和stash changes-CSDN博客](https://blog.csdn.net/eclipse1024/article/details/116352777)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Git

* 回首頁

---

*本文章從點部落遷移至 Writerside*
