# [反編譯] Riru-Il2CppDumper 使用筆記

> **原文發布日期:** 2021-10-01
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/10/01/APK-Unity
> **標籤:** 無

---

Riru-Il2CppDumper
APK 找 Unity 版本

Riru-Il2CppDumper

game.h => Riru-Il2CppDumper\module\src\main\cpp\game.h

[Perfare/Riru-Il2CppDumper: Using Riru to dump il2cpp data at runtime (github.com)](https://github.com/Perfare/Riru-Il2CppDumper)

---

APK 找 Unity 版本

apk 改 zip 打開 assets\bin\Data 裡面最小二進位檔案開頭會顯示版本號 2019.4.11f1

參照

[查看apk是用哪个Unity版本打包的\_linxinfa的专栏-CSDN博客s](https://blog.csdn.net/linxinfa/article/details/99817766)

---

Android Studio 打包 => 按兩下 Ctrl 然後輸入以下冒號開頭的命令

:module:assembleRelease

然後會輸出 Riru-Il2CppDumper\out\riru-il2cppdumper-v26.0.0-release.zip

就可以用手機的 Magisk 安裝該 zip

[Android Studio gradle打包实践 - 簡書 (jianshu.com)](https://www.jianshu.com/p/c5f69437100a)

---

Busybox

安裝時系統唯讀

安裝 Android 終端機

```
mount -o rw,remount /system
```

[Read only file system on Android - Stack Overflow](https://stackoverflow.com/questions/6066030/read-only-file-system-on-android)

---

ApkTool

編譯失敗時可能需要在反編譯時加上 -r 參數

**-r, --no-res**

不反編譯資源，保留 resources.arsc 為原來的樣子，如果你只是需要修改代碼，此配置會加快反編譯和重新打包的速度。

apktool d -r my.apk

然後正常編譯

apktool b my

---

Jar Sign (JDK\bin\)

.\keytool.exe -genkey -v -keystore D:\\my-key.keystore -alias mykey01 -keyalg RSA -validity 10000
.\jarsigner.exe -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore D:\\my-key.keystore -storepass 123456 D:\\work\M173C.apk mykey01

[Android 使用jarsigner給apk簽名的方法詳細介紹 | 程式前沿 (codertw.com)](https://codertw.com/android-%E9%96%8B%E7%99%BC/343323/)
{ignore-vars="true"}

---

Androild Killer

Runtime error 217

=> configs.ini => Lang=English

[Androild Killer无法运行，出现Runtime error 217\_Owen\_Suen的博客-CSDN博客](https://blog.csdn.net/Owen_Suen/article/details/104506758)

---

Androild Killer - Signed

Exception in thread "main" java.lang.NoClassDefFoundError: sun/misc/BASE64Encoder

Java 某版本拿掉內建 sun 函示庫，導致找不到該 class

方向可能改寫簽名方法

bin\apktool\signapk.bat

把該文件內改成呼叫 JDK 內建的簽名 jarsigner

[http - java.lang.NoClassDefFoundError: sun/misc/BASE64Encoder - Stack Overflow](https://stackoverflow.com/questions/29692146/java-lang-noclassdeffounderror-sun-misc-base64encoder)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- Riru-Il2CppDumper
- Unity
- 反編譯
{ignore-vars="true"}

- 回首頁

---

*本文章從點部落遷移至 Writerside*
