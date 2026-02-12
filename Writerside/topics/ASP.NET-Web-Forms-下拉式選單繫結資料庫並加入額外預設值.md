# ASP.NET Web Forms 下拉式選單

> **原文發布日期:** 2024-01-03
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2024/01/03/asp-net-web-form-dropdownlist
> **標籤:** 無

---

本文說明如何在 ASP.NET Web Forms 中，讓下拉式選單繫結資料庫資料的同時，加入額外的預設值選項。

## 結論

加上 `AppendDataBoundItems="true"`

### 範例

```
<asp:SqlDataSource ID="ds1" runat="server" ConnectionString="<%$ ConnectionStrings:MyDb %>"
    SelectCommand="SELECT [id], [name] FROM [Test] WHERE ([IsDeleted] = @isDeleted) ORDER BY [seq]">
    <SelectParameters>
        <asp:Parameter DefaultValue="0" Name="isDeleted" Type="Int32" />
    </SelectParameters>
</asp:SqlDataSource>

<asp:DropDownList ID="cbo1" runat="server" DataSourceID="ds1" DataTextField="name" DataValueField="id" AppendDataBoundItems="true">
    <asp:ListItem Text="預設" Value="" Selected="True"></asp:ListItem>
</asp:DropDownList>
```

#### 參考

[[程式筆記]下拉選單DropDownList範例(asp.net) @ 貓羽的文字日誌 :: 痞客邦 :: (pixnet.net)](https://whitecat2.pixnet.net/blog/post/63515803-%5B%E7%A8%8B%E5%BC%8F%E7%AD%86%E8%A8%98%5D%E4%B8%8B%E6%8B%89%E9%81%B8%E5%96%AEdropdownli)
{ignore-vars="true"}

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

- ASPX

- 回首頁

---

*本文章從點部落遷移至 Writerside*
