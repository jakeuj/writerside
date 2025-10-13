# 控制反轉(IoC) 與 相依性注入(DI) 簡單說明

> **原文發布日期:** 2016-07-15
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/07/15/IoC_DI
> **標籤:** 無

---

控制反轉(IoC) 與 相依性注入(DI) 簡單說明

角色：

* A.老師
* B.班長(我)
* C.國文小老師
* D.數學小老師

情境：

1.國文考試後老師要我叫國文小老師幫他改考卷

```

public class 班長
{
    國文小老師 LittleTeacher = new 國文小老師();
    public void 找小老師改考卷()
    {
        LittleTeacher.改考卷();
    }
}
```

2.數學考試後老師要我叫數學小老師幫他改考卷

```

public class 班長
{
    數學小老師 LittleTeacher = new 數學小老師();
    public void 找小老師改考卷()
    {
        LittleTeacher.改考卷();
    }
}
```

控制反轉IoC：宣告一個小老師的介面，讓班長宣告時不用直接宣告 [國文或數學小老師] 類別，改為宣告 I小老師 介面。

```

public interface I小老師
{
    改考卷();
}

public class 班長
{
    I小老師 D = new 數學小老師();
    public void 找小老師改考卷()
    {
        D.改考卷();
    }
}
```

DI：宣告介面時不直接實體化 [國文或數學小老師]，而改由建構式來接收的 [國文或數學小老師] 實體

```

public class 老師
{
    數學小老師 LittleTeacher = new 數學小老師();
    改考卷(LittleTeacher);
}

public class 班長
{
    I小老師 LittleTeacher;
    班長(I小老師 littleTeacher)
    {
        this.LittleTeacher = littleTeacher;
    }
    public void 找小老師改考卷()
    {
        D.改考卷();
    }
}
```

如此一來班長這個角色就不用知道小老師到底是誰，而改由呼叫班長的老師直接指派

對於班長來說就只需要知道自己需要有改考卷的這件事，但不用自己改而是交給小老師改

並且事先也不用知道到底是要交給哪個小老師，而是由大老師呼叫班長時會直接告知是哪位小老師

最後只要大家按照訂好的小老師介面來作業，無論今天老師多了物理小老師還是化學小老師需要改的考卷，對於班長來說都沒有影響

* 結果：對於我們班長這個角色，就達到了降低耦合的目標，自身不受類別的影響。

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [C#](/jakeuj/Tags?qq=C%23)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
