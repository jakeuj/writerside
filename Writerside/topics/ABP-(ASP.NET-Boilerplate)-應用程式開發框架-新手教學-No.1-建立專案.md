# ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.1 建立專案

> **原文發布日期:** 2016-07-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/07/26/abp1
> **標籤:** 無

---

ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.1 建立專案

​[ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.0 索引](https://dotblogs.com.tw/jakeuj/2016/07/28/abp0)

---

1.到ABP官網下載基本框架：[http://aspnetboilerplate.com/​](http://aspnetboilerplate.com/)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9886c5a0-bdd9-440d-aa02-d74325bbb6c0/1469524990_1426.png)

* 這邊使用預設來建立專案，第三步勾選[Include module-zero]，第四步輸入專案名稱[MyCompany.MyProject]，最後CREATE MY PROJECT！

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9886c5a0-bdd9-440d-aa02-d74325bbb6c0/1469525005_6279.png)

2.使用 Visual Studio 2013 以上版本來開啟專案(這邊我使用Visual Studio 15)，並將[MyCompany.MyProject.Web]設為起始專案

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9886c5a0-bdd9-440d-aa02-d74325bbb6c0/1469525074_84791.png)如果沒有本機資料庫，則需到[MyCompany.MyProject.Web]→[Web.config]修改連接字串內的localhost字段，到你的資料庫IP或LocalDB

<add name="Default" connectionString="Server=localhost; Database=MyProject; Trusted\_Connection=True;" providerName="System.Data.SqlClient" />

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9886c5a0-bdd9-440d-aa02-d74325bbb6c0/1469525126_1054.png)這邊我使用LocalDB來建置資料庫

<add name="Default" connectionString="Server=(LocalDB)\MSSQLLocalDB; Database=AbsoluteDuo\_V4; Trusted\_Connection=True;" providerName="System.Data.SqlClient" />

3.開啟 Package Manager Console

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9886c5a0-bdd9-440d-aa02-d74325bbb6c0/1469525144_76684.png)先還原NuGet封裝，之後選擇 'EntityFramework' 專案來預設專案

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9886c5a0-bdd9-440d-aa02-d74325bbb6c0/1469525582_83776.png)

輸入Update-Database 來建立資料庫

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9886c5a0-bdd9-440d-aa02-d74325bbb6c0/1469525159_93863.png)4.沒有問題了話執行這個專案，就會成功開出畫面，使用帳號admin與密碼123qwe即可登入主程式

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9886c5a0-bdd9-440d-aa02-d74325bbb6c0/1469525169_73291.png)5.到這邊我們基本把ABP從無到有建置完成。

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/9886c5a0-bdd9-440d-aa02-d74325bbb6c0/1469525362_70537.png)

接著我們將開始建立實體

---

下一篇

[ABP (ASP.NET Boilerplate) 應用程式開發框架 新手教學 No.2 建立實體](https://dotblogs.com.tw/jakeuj/2016/07/26/abp2)

參照

[一步一步使用ABP框架搭建正式項目系列教程](http://www.cnblogs.com/farb/p/4849791.html)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [C#](/jakeuj/Tags?qq=C%23)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
