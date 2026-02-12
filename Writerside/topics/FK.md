# FK

絕對不需要設定關聯性兩次，一旦從主體開始，然後再從相依項目開始。
此外，嘗試個別設定關聯性的主體和相依部分通常無法運作。
選擇從一端或另一端設定每個關聯性，然後只撰寫組態程式代碼一次。

## 從子集合實體設定一對一關聯性

```C#
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<Blog>()
        .HasOne(e => e.Header)
        .WithOne(e => e.Blog)
        .HasForeignKey<BlogHeader>(e => e.BlogId)
        .IsRequired();
}
```

## 從主要實體設定一對多關聯性

```C#
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.Entity<BlogHeader>()
        .HasOne(e => e.Blog)
        .WithOne(e => e.Header)
        .HasForeignKey<BlogHeader>(e => e.BlogId)
        .IsRequired();
}
```

### 再次提醒

以上設定只要選其中一個來設定即可，不需要兩邊都設定。

好像會在 Migration 時出現錯誤，類似 FK 重複建立甚麼的，所以只要選其中一個來設定即可。
