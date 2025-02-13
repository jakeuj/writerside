# Flutter

紀錄開發 Flutter 所需的環境設定。

![Andriod SDK API.png](Andriod SDK API.png)

其中 `Android SDK Command-line Tools` 是必要的，可以透過 `Android Studio` 安裝。

![Command-line.png](Command-line.png)

## 需求
- [ ] [PowerShell](https://apps.microsoft.com/detail/9mz1snwt0n5d)
- [ ] [Git](https://git-scm.com/)
- [ ] [Android Studio](https://developer.android.com/studio)
  - [ ] [Flutter plugin for IntelliJ](https://plugins.jetbrains.com/plugin/9212-flutter)
  - [ ] Android SDK Build-Tools
  - [ ] Android SDK Platform-Tools
  - [ ] Android Emulator
  - [ ] Android SDK Platform, API 35.0.1
  - [ ] Android SDK Command-line Tools
    - [ ] Run `flutter doctor --android-licenses` to accept the SDK licenses.
    - [ ] [設定環境變數](https://developer.android.com/tools?hl=zh-tw#environment-variables)
- [ ] [Visual Studio Code](https://code.visualstudio.com/docs/?dv=win64)
  - [ ] [Flutter extension for VS Code](https://marketplace.visualstudio.com/items?itemName=Dart-Code.flutter)
- [ ] [Flutter SDK](https://docs.flutter.dev/get-started/install/windows/mobile#install-the-flutter-sdk)
  - [ ] [Add Flutter to your PATH](https://docs.flutter.dev/get-started/install/windows/mobile?tab=download#update-your-windows-path-variable)
  - [ ] Run "flutter doctor" to check if your system is ready to run Flutter apps.
  - [ ] Run `flutter doctor --android-licenses` to accept the SDK licenses.

## 建立專案
1. 打開 `Android Studio` > Create Project > Flutter > 設定 Flutter SDK Path > Next
![Flutter.png](Flutter.png){ style="inline" }

2. 設定「專案名稱」、「專案存檔路徑」、「專案說明」、「專案類型」、「組織名稱」、「雙平台開發語言」-> Finish
![flutter-project.png](flutter-project.png){ style="inline" }
   - P.S. 這邊專案名稱好像不能有大寫，自己在調整一下大小寫，截圖我就不更新了

3. 建立完成 > 右上角選擇裝置 > refresh > 找到之前建立的模擬手機型號
![flutter-demo.png](flutter-demo.png){ style="inline" }

## 參照
- [Get started with Flutter](https://docs.flutter.dev/get-started/install/windows/mobile#install-the-flutter-sdk)
- [iOS](iOS.md)