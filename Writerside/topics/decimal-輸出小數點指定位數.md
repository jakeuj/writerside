# decimal 輸出小數點指定位數

> **原文發布日期:** 2023-02-02
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/02/02/decimal
> **標籤:** 無

---

筆記一下數字指定輸出格式

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/657848f4-a9d8-4e26-9104-97a29aa0001e/1675329285.png.png)

結論

```
decimal? decimalVar = 0.5m;

decimalVar.GetValueOrDefault().ToString("#.##").Dump();

decimalVar.GetValueOrDefault().ToString("0.##").Dump();

decimalVar.GetValueOrDefault().ToString("0.00").Dump();
```

參照

[c# - How do I display a decimal value to 2 decimal places? - Stack Overflow](https://stackoverflow.com/questions/164926/how-do-i-display-a-decimal-value-to-2-decimal-places)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- 回首頁

---

*本文章從點部落遷移至 Writerside*
