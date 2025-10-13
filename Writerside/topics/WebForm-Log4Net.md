# WebForm Log4Net

> **原文發布日期:** 2021-01-13
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2021/01/13/Log4Net
> **標籤:** 無

---

幾年沒碰WebForm

習慣了Nuget套件

紀錄一下丟dll進去

要怎麼寫Log來著

下載：[log4net-binaries](https://logging.apache.org/log4net/download_log4net.html)

丟到專案 bin\

web.config

```

<configuration>
  <configSections>
    <!-- 附加這行 -->
    <section name="log4net" type="log4net.Config.Log4NetConfigurationSectionHandler, log4net"/>
  </configSections>
  <!-- 附加下面區塊 -->
  <log4net>
    <appender name="RollingFile" type="log4net.Appender.RollingFileAppender">
      <file value="logs\log.log" />
      <appendToFile value="true" />
      <maximumFileSize value="100KB" />
      <maxSizeRollBackups value="2" />
      <lockingmodel type="log4net.Appender.FileAppender+MinimalLock" />
      <datepattern value="'.'yyyy-MM-dd" />
      <layout type="log4net.Layout.PatternLayout">
        <conversionPattern value="%date | %-5level | %logger{1}.%method:%line | %message%newline" />
      </layout>
      <filter type="log4net.Filter.LevelRangeFilter">
        <levelmin value="DEBUG" />
        <levelmax value="ERROR" />
      </filter>
    </appender>
    <root>
      <level value="DEBUG" />
      <appender-ref ref="RollingFile" />
    </root>
  </log4net>
  <!-- 主要就上面兩部分 -->
  <connectionStrings/>
  <appSettings/>
</configuration>
```

要用Log的class

```

// Import log4net classes.
using log4net;
using log4net.Config;

public class MyApp
{
    // Define a static logger variable so that it references the
    // Logger instance named "MyApp".
    private static readonly ILog log = LogManager.GetLogger(typeof(MyApp));

    static void Main(string[] args)
    {
        // Set up a xml configuration that logs.
        XmlConfigurator.Configure();

        log.Info("Entering application.");

        // do somethings...

        log.Info("Exiting application.");
    }
}
```

參照：[Apache log4net™ Manual - Configuration](https://logging.apache.org/log4net/release/manual/configuration.html)

參照：[[料理佳餚] 使用 log4net](https://dotblogs.com.tw/supershowwei/2015/08/25/153214)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Apache](/jakeuj/Tags?qq=Apache)
* [C#](/jakeuj/Tags?qq=C%23)
* [Log](/jakeuj/Tags?qq=Log)
* [Log](/jakeuj/Tags?qq=Log)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
