# Convert Web site (WSP) to Web Application (WAP) with Visual Studio 2019

> **原文發布日期:** 2021-03-02
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/03/02/Convert-Web-site-to-WebApplication-Visual-Studio-2019
> **標籤:** 無

---

轉換 網站型專案 到 網頁應用程式專案 (VS 2019) 流程筆記

WSP 缺點：

1. 原始碼被部署到正式主機違反一般資安原則（靠編譯後發佈或WDP可以克服）
2. 每個網頁自成DLL，載入程序繁瑣影響效能（可在WDP設定每個資料夾編成一顆DLL改善）
3. 依賴將DLL放入BIN目錄形成參照，參照關聯不明確，除錯不易。BIN目錄需簽入版控，編譯後DLL檔案日期改變形成異動待簽入假象有點困擾
4. 網頁採動態編譯，單元測試實施不易
5. 跨網頁共用的程式碼只能集中在App\_Code，不像WAP可以自由調置
6. 不支援ASP.NET MVC

WAP 步驟

1. 新建一個新版空白WebApplication專案
2. 將原有網站頁面程式碼包含App\_Code複製貼上到新專案
3. App\_Code進去裡面全選之後，去 屬性>進階>建置動作>內容> 改成 編譯

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/4d2ba2fb-e07a-4c9c-b9c3-141fa3e8ae2f/1614670712.png)

1. 將缺少的Nuget套件先裝一裝
2. 有其他Bug先解一解
   (比如甚麼複製A到B頁面的時候
   class 名稱忘記改
   導致同名 class new 了相同類別)
3. 重頭戲，點一下 Convert to web application

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/4d2ba2fb-e07a-4c9c-b9c3-141fa3e8ae2f/1614670402.png)

1. 這邊我卡N久，因為舊版是在右邊專案總管點右鍵會有這選項，
   新版拿掉了，要從上方專案Tab點進去才會看到...
2. Bulid & Test

## 備註

1. 如果專案本身有問題不能 build，偵錯 > 偵錯屬性 > 建置 > 不建置
2. c#新版語法不支援：將編譯器改成 Roslyn ，並將 C# 版本從 5.0 升到 7.3

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* VisualStudio
* WebApplication
* WebSite

* 回首頁

---

*本文章從點部落遷移至 Writerside*
