# ABP.IO WEB應用程式框架 烤肉串命名&#xFF08;Kebab case&#xFF09;

> **原文發布日期:** 2022-04-14
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/04/14/abp-kebab-camel-case
> **標籤:** 無

---

Workaround to **camelCase (去連字號)**

## 結論

```
Configure<AbpAspNetCoreMvcOptions>(options =>
{
    options.ConventionalControllers
        .Create(typeof(YoApplicationModule).Assembly, opts =>
        {
            opts.UseV3UrlStyle = true;
        });
});
```

## 情境

Url 慣例使用 Kebab case（烤肉串命名）

But,人生中最重要的就是這個 But !

種種原因需要去除連字號時可以切回舊版本 `UseV3UrlStyle`

![route-4](https://github.com/abpframework/abp/raw/dev/docs/en/Migration-Guides/images/route-4.png)

Kebab case

![route-before-4](https://github.com/abpframework/abp/raw/dev/docs/en/Migration-Guides/images/route-before-4.png)

**camel Case**

參照

[abp camelCase route parts become kebab-case](https://github.com/abpframework/abp/blob/dev/docs/en/Migration-Guides/Abp-4_0.md#auto-api-controller-route-changes)

[常見重點整理 - 命名慣例 & 開發時注意事項 - HackMD](https://hackmd.io/@Heidi-Liu/note-common)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* ABP

* 回首頁

---

*本文章從點部落遷移至 Writerside*
