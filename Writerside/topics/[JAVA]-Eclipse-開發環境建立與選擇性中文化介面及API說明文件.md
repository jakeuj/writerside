# [JAVA] Eclipse 開發環境建立與選擇性中文化介面及API說明文件

> **原文發布日期:** 2011-07-12
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2011/07/12/31512
> **標籤:** 無

---

[JAVA] Eclipse 開發環境建立與選擇性中文化介面及API說明文件

1.[![](http://java.sun.com/im/logo_oracle_footer.gif)](http://java.sun.com/javase/downloads/index.jsp)
首先點上圖下載最新版本 JDK(內含JRE) 目前版本是 JDK 6 Update 20
頁面下方可以選擇是否要額外下載 JDK 的 API 說明文件 Java SE 6 Documentation
2.[![](http://www.eclipse.org/eclipse.org-common/themes/Nova/images/eclipse.png)](http://www.eclipse.org/downloads/)
接著點上圖下載最新版本 IDE Eclipse 目前版本是 Eclipse 3.5 SR2
3.[![](http://www.eclipse.org/images/egg-incubation.png)](http://www.eclipse.org/babel/)
在安裝完以上環境可以選擇中文化 IDE 方法如下
[Windows] -> [Preferences] -> Install/Update -> Available Software Sites
我們進行新增(Add)的動作, 並填入下列二筆資料:
Name: Babel
Location: http://archive.eclipse.org/technology/babel/update-site/R0.8.0/galileo
![](http://img64.imageshack.us/img64/1454/15704602.jpg)
選擇Eclipse的繁體中文化後點選下一步進行下載並安裝後，重開Eclipse即可看到中文介面
請展開中文套件選擇For Eclipse，如選擇整個中文化套件未選擇For Eclipse則會中文化失敗
完成後Eclipse介面中文化後應該如下圖:
![](http://img191.imageshack.us/img191/7117/16644672.jpg)
4.[![](http://dev.eclipse.org/large_icons/actions/bookmark-new.png)](http://of.openfoundry.org/download_path/java4zhtw/1.6.20081225/com.sun.java.doc.sdk.1.6_tw_Kuo_chaoyi_v20081225.zip)
接著可以點上圖下載 中文化的JAVA API 說明文件
在操作介面上[Windwos]>[Reference ...]>[Java]>[Installed JRE] 點擊 [Edit ...]>如下列圖操作:
[![](http://2.bp.blogspot.com/_Sx-9Cwd1BEg/SU_FjIyYQbI/AAAAAAAABy0/XR_cbjFJ1ZM/s400/eclipse3.4.tw.chaoyi.kuo.03.png)](http://2.bp.blogspot.com/_Sx-9Cwd1BEg/SU_FjIyYQbI/AAAAAAAABy0/XR_cbjFJ1ZM/s1600-h/eclipse3.4.tw.chaoyi.kuo.03.png)
(二)找 rt.jar
[![](http://4.bp.blogspot.com/_Sx-9Cwd1BEg/SU_GT7rrVgI/AAAAAAAABy8/o-YizabEgqA/s400/eclipse3.4.tw.chaoyi.kuo.04.png)](http://4.bp.blogspot.com/_Sx-9Cwd1BEg/SU_GT7rrVgI/AAAAAAAABy8/o-YizabEgqA/s1600-h/eclipse3.4.tw.chaoyi.kuo.04.png)
(三)再來就看您把老魚的製作且下載的檔案放置於那囉, 在下圖補上位置:
[![](http://3.bp.blogspot.com/_Sx-9Cwd1BEg/SU_HLxxyNTI/AAAAAAAABzE/a6XcXfCwmCY/s400/eclipse3.4.tw.chaoyi.kuo.05.png)](http://3.bp.blogspot.com/_Sx-9Cwd1BEg/SU_HLxxyNTI/AAAAAAAABzE/a6XcXfCwmCY/s1600-h/eclipse3.4.tw.chaoyi.kuo.05.png)
以上圖文參考部分節錄自 [大智若魚::人生處處是道場](http://oss-tw.blogspot.com/)
完成API中文化後應該如下圖
![](http://img190.imageshack.us/img190/1876/69920050.jpg)
5.[![](http://www.eclipse.org/eclipse.org-common/themes/Nova/images/eclipse.png)](http://www.eclipse.org/vep/downloads/)
視窗程式設計GUI設計套件可點上圖下載或用以下方法安裝:
[Windows] -> [Preferences] -> Install/Update -> Available Software Sites
我們進行新增(Add)的動作, 並填入下列二筆資料:
Name:VE
Location:<http://download.eclipse.org/tools/ve/updates/1.4/>
但是說實在的，因為安裝 Eclipse實已經附帶安裝了EMF
而再安裝VE套裝時一直顯示只能安裝唯一版本的EMF套件導致安裝失敗..
直接下載VE蓋到Eclipse後雖然視覺化設計選項有出來
但是裡面好像空空如也，怎麼完整解決目前還不知道..
因為我連怎麼移除套件都不知道，想把原本的EMF拿掉也不行，想把VE先拿掉重裝也不行
而且因此我已經把Eclipse整個刪除再用全新版本來測試VE安裝，未果..
以上待續...

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Eclipse](/jakeuj/Tags?qq=Eclipse)
* [JAVA](/jakeuj/Tags?qq=JAVA)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
