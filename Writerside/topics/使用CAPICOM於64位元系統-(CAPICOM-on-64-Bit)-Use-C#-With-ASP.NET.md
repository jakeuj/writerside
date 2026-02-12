# CAPICOM 64位元系統

> **原文發布日期:** 2012-03-03
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2012/03/03/70494
> **標籤:** 無

---

使用CAPICOM於64位元系統 (CAPICOM on 64 Bit)

#### 因緣際會需要使用CAPICOM進行加解密處理

現在64位元為主流的時代中，CAPICOM卻跟不上時代潮流只支援32位元

可是我不想為此建立一個32位元的Server只是為了跑CAPICOM阿…

廢話不多說，以下是在X64系統使用CAPICOM的步驟：

1. 複製 capicom.dll 到 `%windir%\syswow64`{ignore-vars="true"}
2. 執行 CMD 命令 `%windir%\syswow64\regsvr32.exe %windir%\syswow64\capicom.dll`{ignore-vars="true"}
3. 到 IIS → 應用程式集區 → 應用程式→ 進階設定→ 啟用32位元應用程式→ TRUE
   適用 IIS： *(Could not load file or assembly 'Interop.CAPICOM' or one of its dependencies. 試圖載入格式錯誤的程式。)*
4. Visual Studios → 參考 → CAPICOM → 內嵌Interop型別 → false
   適用 Visual Studios：(無法內嵌 Interop 型別 'CAPICOM.UtilitiesClass'。請改用適當的介面。)

如此終於解決CAPICOM ON 64BIT 所遇到的問題囉~~

附上 CAPICOM 下載位置

#### Platform SDK 可轉散佈程式碼

下載連結：[CAPICOM](http://www.microsoft.com/downloads/zh-tw/details.aspx?FamilyID=860ee43a-a843-462f-abb5-ff88ea5896f6&DisplayLang=zh-tw)

參考：

- [msdn](http://social.msdn.microsoft.com/Forums/en/netfx64bit/thread/8b0ed9bb-1c05-4607-8130-46fb58d64d3e){ignore-vars="true"}
- [google](http://www.google.com.tw/search?ix=ieb&sourceid=chrome&ie=UTF-8&q=%E5%9C%A864%E4%BD%8D%E7%B3%BB%E7%BB%9F%E4%B8%AD%E4%BD%BF%E7%94%A8CAPICOM){ignore-vars="true"}

聲明：

歡迎轉載，請註明來源 [http://www.dotblogs.com.tw/jakeuj/](http://www.dotblogs.com.tw/jakeuj/)，感謝您的支持與配合！

By [jakeuj@hotmail.com](mailto:jakeuj@hotmail.com) 分享於 [點部落(DotBolog)](http://www.dotblogs.com.tw/)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- C#
- 回首頁

---

*本文章從點部落遷移至 Writerside*
