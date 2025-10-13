# Wcf Error (Message part XXXXXResult in namespace http://tempuri.org/ appears more than once in Message.)

> **原文發布日期:** 2012-11-20
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2012/11/20/84757
> **標籤:** 無

---

Wcf Error (Message part XXXXXResult in namespace http://tempuri.org/ appears more than once in Message.)

前言：
我寫了一個Wcf之後在呼叫時發生執行階段錯誤
錯誤碼如下
Message part EventSnReceiveResult in namespace http://tempuri.org/ appears more than once in Message.
查Google又找不太到相關文章於是就開始今天的Debug之旅...
旅途我就不多說，直接跳心得部分吧！

說明：

---

Wcf介面interface中定義一個作業合約EventSnReceive

```

[OperationContract]
        int EventSnReceive(string EventCode, out int EventSnReceiveMessage);
```

---

Wcf中繼資料wsdl自動生成xml

```

<xs:element name="EventSnReceive">
<xs:complexType>
<xs:sequence>
<xs:element minOccurs="0" name="EventCode" nillable="true" type="xs:string"/>
</xs:sequence>
</xs:complexType>
</xs:element>
<xs:element name="EventSnReceiveResponse">
<xs:complexType>
<xs:sequence>
<xs:element minOccurs="0" name="EventSnReceiveResult" type="xs:int"/>
<xs:element minOccurs="0" name="EventSnReceiveMessage" type="xs:int"/>
</xs:sequence>
</xs:complexType>
</xs:element>
```

---

由此可知Wcf架構下的方法回傳值(return)是以方法名稱其後附加"Result"來表示

並且在回傳值在wcf回呼時是與out參數一同序列化
這意味著如果我們將out參數名稱定義為方法名稱其後附加"Result"時
將會與Return值的Wcf定義名稱發生衝突

請注意看下列wsdl->xml->EventSnReceiveResponse->EventSnReceiveResult
由於重複所以最後產生的wsdl將會只有一個EventSnReceiveResult但是wcf內其實是包含return與out
因此程式無法將其對應並產生執行階段錯誤

---

Wcf介面interface中定義一個作業合約EventSnReceive

```

[OperationContract]
        int EventSnReceive(string EventCode, out int EventSnReceiveResult);
```

---

Wcf中繼資料wsdl自動生成xml

```

<xs:element name="EventSnReceive">
<xs:complexType>
<xs:sequence>
<xs:element minOccurs="0" name="EventCode" nillable="true" type="xs:string"/>>
</xs:sequence>
</xs:complexType>
</xs:element>
<xs:element name="EventSnReceiveResponse">
<xs:complexType>
<xs:sequence>
<xs:element minOccurs="0" name="EventSnReceiveResult" type="xs:int"/>
<xs:element minOccurs="0" name="EventSnReceiveResult" type="xs:int"/>
</xs:sequence>
</xs:complexType>
</xs:element>
```

---

結論：
所以避免用 {[方法名稱]+"Result"} 的方式來命名 out 參數即可避免此Bug
(Message part EventSnReceiveResult in namespace http://tempuri.org/ appears more than once in Message.)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* C#
{ignore-vars="true"}

* 回首頁

---

*本文章從點部落遷移至 Writerside*
