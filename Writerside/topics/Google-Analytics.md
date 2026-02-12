# Google Analytics

記錄下 WriterSide 如何加入 Google Analytics 進行網站流量分析。

## 參照

[analytics-head-script-file](https://www.jetbrains.com/help/writerside/buildprofiles-xml.html#analytics-head-script-file)

## 步驟

1. cfg 資料夾建立 google-analytics.js。
2. 把 Google Analytics 的追蹤碼放入 google-analytics.js。
3. 在 buildprofiles.xml 中加入 analytics-head-script-file 區段並設定為 google-analytics.js。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<buildprofiles>
    <variables>
        <analytics-head-script-file>
            google-analytics.js
        </analytics-head-script-file>
    </variables>
</buildprofiles>
```

{ignore-vars="true"}

## 結果

![ga.png](ga.png){style="block"}
