# 委派 delegate C# 基本概念具現化

> **原文發布日期:** 2012-10-30
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2012/10/30/CSharp-delegate
> **標籤:** 無

---

委派 delegate C# 基本概念具現化

怎麼宣告跟使用我想MSDN和GOOGLE就夠了

這邊只是筆記一下委派的小觀念(總覺得有點抽象)

我想用傳遞參數來解釋委派會比較具體好懂點兒

原本我們常用的傳遞參數是來傳遞String,int等等型別

舉例來說就是

`int XaddY(int x,int y){return x+y;}`

這是原本我們常用的傳遞參數(x,y)的方式

而這跟委派又有甚麼關係呢?

今天(何年何月)我們可能會想在A函式內使用B函式

直覺上會使用

```
void A()
{
  //dosomething
  B(1);
}

void B(string c)
{
  //dosomething
}
```

但是如果今天B函式並非固定的呢？

我想用傳遞參數的方式把我想用的函式丟進A裡頭，讓A用我給他的函式來處理(這樣就不用寫死B並且可以根據工作需要來執行不同的B程序)

所以我想的表達方式是

```
void A(B)
{
  //dosomething
  B(1);
}
```

C#用來實現以上需求的東西就叫做委派(delegate)！

實作上需要先宣告一個委派(就是我們想傳遞的函式B)

因為A還不知道你會傳甚麼進來(因為B函式沒有定義在該組件中，而是由我們(外部)傳遞給A的)

所以我們需要先宣告一個空殼(這叫委派！)

```
public delegate bool MethodB(string s);
```

 麻雀雖小，五臟也不全，但是頭跟尾需要先定義好讓A知道可以傳甚麼進去，而你又會排放甚麼排泄物出來，他才不管你內部是怎麼去消化的呢！

這行的意思是我定義一個我等等要傳進來的函式(這叫委派)，這個函式會接收一個String參數，並且Return一個布林值，內部做甚麼事就不得而知了，你只管使用就對了

所以程序可以這樣寫

```
public delegate bool MethodB(string a);

void A(MethodB B)
{
  //dosomething
  B(1);
}
```

意思就是A會照你給的B函式來處理工作

結論是你可以將委派理解為傳遞一個參數，該參數不是字串也不是整數而是一個函式(Function)

或者你也可以將委派理解為一個函式(Function)的指標(point)，如果你學過C/OOP了話這樣可能可以幫助你理解這東西

以上就是今天遇到的問題跟自己現在的理解

參照

<http://huan-lin.blogspot.tw/2009/01/delegate-revisited-csharp-1-to-2-to-3.html>

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* C#
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
