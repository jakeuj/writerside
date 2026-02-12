# Identity-Server-4-ClientSecret

記錄下如何新增 ClientSecret 到 Identity Server 4

## 新增 ClientSecret

1. 進入 ABP 的資料庫
2. 找到 `IdentityServerClientSecrets` Table
3. 新增一筆資料
4. `ClientId` 輸入 Client 名稱
5. `ClientSecrets` 輸入 **SHA256 並 Base64** 後的 ClientSecret
6. `Type` 輸入 `SharedSecret`
7. `Expiration` 期限 (可以不填)
8. `Description` 輸入描述 (可以不填)
9. 儲存後即可使用

## 參考

[identityserver4-storing-client-secrets](https://stackoverflow.com/questions/44001798/identityserver4-storing-client-secrets)
