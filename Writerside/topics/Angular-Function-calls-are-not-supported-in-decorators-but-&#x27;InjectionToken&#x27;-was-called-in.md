# Angular Function calls are not supported in decorators but &#x27;InjectionToken&#x27; was called in {id="Angular-Function-calls-are-not-supported-in-decorators-but-&#x27;InjectionToken&#x27;-was-called-in"}

> **原文發布日期:** 2019-08-26
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/08/26/angulardecoratorerror
> **標籤:** 無

---

Angular ng build --prod 時報錯的解決方法紀錄

Function calls are not supported in decorators but 'InjectionToken' was called in 'OWL\_MOMENT\_DATE\_TIME\_ADAPTER\_OPTIONS'

tsconfig.json

```

"paths": {
    //...

    "@angular/*": ["../node_modules/@angular/*"]
}
```

參照：<https://github.com/angular/angular/issues/16762>

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Angular

* 回首頁

---

*本文章從點部落遷移至 Writerside*
