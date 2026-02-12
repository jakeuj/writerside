# SQL UPDATE 大量更新

> **原文發布日期:** 2019-06-28
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/06/28/SQLUPDATE
> **標籤:** 無

---

SQL UPDATE 大量更新

MySql, MariaDB

```

UPDATE A,B SET A.C2=B.C3 WHERE A.C1=B.C1;
```

MSSQL

```

UPDATE A SET A.C2=B.C3 FROM A,B WHERE A.C1=B.C1;
```

參照：<http://cuixiaodong214.blog.163.com/blog/static/951639820104100443302/>

```

UPDATE A SET A.C2=B.C3 FROM A JOIN B ON A.C1=B.C1;
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- SQL

- 回首頁

---

*本文章從點部落遷移至 Writerside*
