# 如何在 linux 從 github clone repo

> **原文發布日期:** 2023-10-04
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/10/04/ssh-git-clone
> **標籤:** 無

---

筆記在 GCE ubuntu 使用 ssh 方式從 github 取得專案

結論

```
ssh-keygen
```

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/67d1de2f-d39e-46f7-b2c2-250dfa29334e/1696402201.png.png)

把產出的 `/home/jake/.ssh/id_rsa.pub` 內容貼到 GITHUB [Add new SSH key (github.com)](https://github.com/settings/ssh/new)

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/67d1de2f-d39e-46f7-b2c2-250dfa29334e/1696402458.png.png)

就可以直接 gti clone 了

`git clone git@github.com:jakeuj/demo.git`

![](https://dotblogsfile.blob.core.windows.net/user/小小朱/67d1de2f-d39e-46f7-b2c2-250dfa29334e/1696402559.png.png)

參照

[【Git教學】手把手 Github SSH 連線設定教學 (Windows/Mac) - Max行銷誌 (maxlist.xyz)](https://www.maxlist.xyz/2022/12/22/github-ssh-setting/)

[Git 踩坑紀錄（二）git clone with SSH keys 或 HTTPS 設定步驟 | by TSENG FU CHUN / 豆腐 | Medium](https://tsengbatty.medium.com/git-%E8%B8%A9%E5%9D%91%E7%B4%80%E9%8C%84-%E4%BA%8C-git-clone-with-ssh-keys-%E6%88%96-https-%E8%A8%AD%E5%AE%9A%E6%AD%A5%E9%A9%9F-bdb721bd7cf2)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [GCP](/jakeuj/Tags?qq=GCP)
* [Git](/jakeuj/Tags?qq=Git)
* [Github](/jakeuj/Tags?qq=Github)
* [Linux](/jakeuj/Tags?qq=Linux)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
