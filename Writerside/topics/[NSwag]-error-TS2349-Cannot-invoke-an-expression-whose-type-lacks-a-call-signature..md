# [NSwag] error TS2349: Cannot invoke an expression whose type lacks a call signature.

> **原文發布日期:** 2019-07-31
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/07/31/NSwagTemplate
> **標籤:** 無

---

tsconfig.json 更新 es6 Ts3 之後可能遇到 MomentJS import 報錯

這邊筆記修改樣板 (NSwag Template) 來解決此問題的步驟

先下結論

1.修改NSwag樣板檔案來符合ES6

NSwag GitHub > [File.liquid](https://github.com/RicoSuter/NSwag/blob/master/src/NSwag.CodeGeneration.TypeScript/Templates/File.liquid#L55)

下載後把L60

mport \* as moment from 'moment';

改成

mport moment from 'moment';

參照：[Change momentjs import (TS)](https://github.com/RicoSuter/NSwag/pull/1901/commits/a01fe4c196b06f24f81fbd304dff6081df927c4d)

2.修改 service.config.nswag

找到 "templateDirectory": null,

改成你放修改後的樣板的目錄

EX: "templateDirectory": "TemplateDirectory",

參照：[Templates](https://github.com/RicoSuter/NSwag/wiki/Templates)

總之為了使用新版Json檔案讀取，更新了TS3啟用ES6規範之類的，然後編譯發現會報錯

接著大概知道要改import但每次NSwag refresh自動生成Code都要手動改一次 覺得麻煩

最後找到改樣板可以解決這問題，目前NSwag還沒決定最終解決方案，目前就先這樣改吧

error TS2349: Cannot invoke an expression whose type lacks a call signature.

Type 'typeof import("node\_modules/moment/moment.d.ts")' has no compatible call signatures.

參照：[Typescript compilation error when using momentjs and TypeScript 3](https://github.com/RicoSuter/NSwag/issues/1859)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Angular
* TypeScript
* NSwag
* ES6

* 回首頁

---

*本文章從點部落遷移至 Writerside*
