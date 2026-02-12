# 如何利用&#x300C;磁碟清理&#x300D;工具 安全的騰出系統硬碟的多餘空間 {id="How-To-Use-Disk-Cleanup-Tool-Safely"}

> **原文發布日期:** 2015-08-13
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2015/08/13/153129
> **標籤:** 無

---

磁碟清理 Server 磁碟空間不足 DISM

Server 磁碟空間不足時可用指令

CMD

Windows Server 2008 以下

dism /online /cleanup-image /spsuperseded /hidesp

Windows 2012 以上

DISM.exe /online /Cleanup-Image /StartComponentCleanup

參照：http://blog.miniasp.com/post/2014/01/22/Using-Disk-Cleanup-Wizard-delete-outdated-Windows-Update-files.aspx

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- DISM
- Server

- 回首頁

---

*本文章從點部落遷移至 Writerside*
