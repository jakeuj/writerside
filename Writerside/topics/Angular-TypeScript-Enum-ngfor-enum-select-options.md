# Angular TypeScript Enum ngfor-enum-select-options

> **原文發布日期:** 2019-05-30
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/05/30/145328
> **標籤:** 無

---

ngfor-enum-select-options

```

export enum Symbols {
  equals = '\u003D',
  notEquals = '!='
}

@Component({
  selector: 'my-app',
  template: `
    <p>
      Having the name as label and symbol as value:
      <select>
        <option *ngFor="let symbol of keys(symbols)"
            [ngValue]="symbols[symbol]">{{symbol}}
        </option>
      </select>
    </p>
    <p>
      Having the symbol as label and name as value:
      <select>
        <option *ngFor="let symbol of keys(symbols)"
            [ngValue]="symbol">{{symbols[symbol]}}
        </option>
      </select>
    </p>
  `
})
export class AppComponent  {
  keys = Object.keys;
  symbols = Symbols;
}
```

Ref: <https://stackblitz.com/edit/ngfor-enum-select-options?file=app%2Fapp.component.ts>
{ignore-vars="true"}

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [Angular](/jakeuj/Tags?qq=Angular)
* [TypeScript](/jakeuj/Tags?qq=TypeScript)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
