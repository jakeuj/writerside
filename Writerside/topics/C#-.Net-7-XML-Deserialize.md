# C# .Net 7 XML Deserialize

> **原文發布日期:** 2023-05-30
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/05/30/xml-serialization-xmlserializer-deserialize
> **標籤:** 無

---

筆記一下 XML 反序列化

## CLASS

Visual Studio 可以從 功能表 編輯 貼上 選擇將 XML 轉成 CLASS

![Screenshot of the Paste Special option from the Edit menu in Visual Studio.](https://learn.microsoft.com/en-us/visualstudio/ide/reference/media/paste-json-xml-class-sml.png?view=vs-2022)

## XML

```
<?xml version="1.0"?>
 <OrderedItem xmlns:inventory="http://www.cpandl.com" xmlns:money="http://www.cohowinery.com">
   <inventory:ItemName>Widget</inventory:ItemName>
   <inventory:Description>Regular Widget</inventory:Description>
   <money:UnitPrice>2.3</money:UnitPrice>
   <inventory:Quantity>10</inventory:Quantity>
   <money:LineTotal>23</money:LineTotal>
 </OrderedItem>
```

## Program

```
using System;
using System.IO;
using System.Text;
using System.Xml;
using System.Xml.Serialization;

// This is the class that will be deserialized.
public class OrderedItem
{
    public string ItemName;
    public string Description;
    public decimal UnitPrice;
    public int Quantity;
    public decimal LineTotal;

    // A custom method used to calculate price per item.
    public void Calculate()
    {
        LineTotal = UnitPrice * Quantity;
    }
}
public class Test
{
    public static void Main(string[] args)
    {
        Test t = new Test();
        // Read a purchase order.
        t.DeserializeObject("simple.xml");
    }

    private void DeserializeObject(string filename)
    {
        Console.WriteLine("Reading with XmlReader");

        // Create an instance of the XmlSerializer specifying type and namespace.
        XmlSerializer serializer = new
        XmlSerializer(typeof(OrderedItem));

        // A FileStream is needed to read the XML document.
        FileStream fs = new FileStream(filename, FileMode.Open);
        XmlReader reader = XmlReader.Create(fs);

        // Declare an object variable of the type to be deserialized.
        OrderedItem i;

        // Use the Deserialize method to restore the object's state.
        i = (OrderedItem)serializer.Deserialize(reader);
        fs.Close();

        // Write out the properties of the object.
        Console.Write(
        i.ItemName + "\t" +
        i.Description + "\t" +
        i.UnitPrice + "\t" +
        i.Quantity + "\t" +
        i.LineTotal);
    }
}
```

## 參照

[Paste JSON or XML as classes - Visual Studio (Windows) | Microsoft Learn](https://learn.microsoft.com/en-us/visualstudio/ide/reference/paste-json-xml?view=vs-2022#xml)

[XmlSerializer.Deserialize 方法 (System.Xml.Serialization) | Microsoft Learn](https://learn.microsoft.com/zh-tw/dotnet/api/system.xml.serialization.xmlserializer.deserialize?view=net-8.0#system-xml-serialization-xmlserializer-deserialize(system-xml-xmlreader))

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [XML](/jakeuj/Tags?qq=XML)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
