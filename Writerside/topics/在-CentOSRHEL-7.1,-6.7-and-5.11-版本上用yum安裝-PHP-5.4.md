# 在 CentOS/RHEL 7.1, 6.7 and 5.11 版本上用yum安裝  PHP 5.4

> **原文發布日期:** 2016-08-01
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/08/01/php
> **標籤:** 無

---

在 CentOS/RHEL 7.1, 6.7 and 5.11 版本上用yum安裝  PHP 5.4

### 在CentOS 7下(包含安裝EPEL)

```

wget http://dl.fedoraproject.org/pub/epel/7/x86_64/e/epel-release-7-7.noarch.rpm
wget http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
rpm -Uvh remi-release-7*.rpm epel-release-7*.rpm
```

如果您原本就已經裝過EPEL則執行下面指令：

```

wget http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
rpm -Uvh remi-release-7*.rpm
```

### 在CentOS 6下(包含安裝EPEL)

```

wget http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
wget http://rpms.famillecollet.com/enterprise/remi-release-6.rpm
rpm -Uvh remi-release-6*.rpm epel-release-6*.rpm
```

如果您原本就已經裝過EPEL則執行下面指令：

```

wget http://rpms.famillecollet.com/enterprise/remi-release-6.rpm
rpm -Uvh remi-release-6*.rpm
```

## 啟動程式庫(Repo,repository)

vi /etc/yum.repos.d/remi.repo

我們需要確認第一階段`[remi]`是啟用狀態。

```

[remi]
name=Les RPM de remi pour Enterprise Linux 6 - $basearch
#baseurl=http://rpms.famillecollet.com/enterprise/6/remi/$basearch/
mirrorlist=http://rpms.famillecollet.com/enterprise/6/remi/mirror
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-remi
```

這一行`enabled=1`確認要設定！

## Installing PHP

輸入以下指令安裝 php

```

sudo yum install php php-gd php-mysql php-ZendFramework
```

php-gd php-mysql php-ZendFramework　是額外的不需要可以不裝

```

rpm -qa |grep php
```

以上指令可以查安裝了php相關的甚麼套件

參照：[專題文章：如何在CentOS 6和CentOS 7上安裝PHP 5.4、5.5或5.6版本](https://www.cadch.com/modules/news/article.php?storyid=227)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Server](/jakeuj/Tags?qq=Server)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
