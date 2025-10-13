# Unity 5 使用 Android SDK API 24 問題

> **原文發布日期:** 2016-07-04
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/07/04/Unity
> **標籤:** 無

---

Unity 5 使用 Android SDK API 24 問題 CommandInvokationFailure: Failed to re-package resources.

最近下載了Unity來弄Android的專案

建置的時候需要使用Android SDK

現在的Android SDK API最新版本為24

Unity建置的時候會使用build-tools

如果下載Android Studio時預設會下載最新版本24的build-tools

Unity預設會使用最新版本的build-tools來做建置

但實際上時便最新的測試版UNITY 5.4.0B24目前也只支援到API 23

在建置時會報錯

錯誤內容為 Failed to re-package resources

解決方式是用Android SDK Manager移除build-tools 24

然後安裝build-tools 23

再重新建置一次就可以過了

以下是CONSOLE詳細錯誤訊息

CommandInvokationFailure: Failed to re-package resources.
D:\android-sdk\build-tools\24.0.0\aapt.exe package --auto-add-overlay -v -f -m -J gen -M AndroidManifest.xml -S "res" -I "D:/android-sdk\platforms\android-24\android.jar" -F bin/resources.ap\_

stderr[

]
stdout[

]
UnityEditor.Android.Command.Run (System.Diagnostics.ProcessStartInfo psi, UnityEditor.Android.WaitingForProcessToExit waitingForProcessToExit, System.String errorMsg)
UnityEditor.Android.PostProcessor.Tasks.TasksCommon.Exec (System.String command, System.String args, System.String workingdir, System.String errorMsg)
UnityEditor.Android.PostProcessor.Tasks.BuildResources.CompileResources (UnityEditor.Android.PostProcessor.PostProcessorContext context)
UnityEditor.Android.PostProcessor.Tasks.BuildResources.Execute (UnityEditor.Android.PostProcessor.PostProcessorContext context)
UnityEditor.Android.PostProcessor.PostProcessRunner.RunAllTasks (UnityEditor.Android.PostProcessor.PostProcessorContext context)
UnityEditor.HostView:OnGUI()

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Unity](/jakeuj/Tags?qq=Unity)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
