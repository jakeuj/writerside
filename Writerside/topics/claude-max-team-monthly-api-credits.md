# 領取 Claude Max 與 Team 方案每月免費 API 額度

<web-summary>說明 Claude Max 5x、Max 20x 與 Team 方案每月附贈的 Claude Platform API 額度金額、資格、如何把 claude.ai 帳號連結到 Console 組織完成領取，以及自動儲值與額度不累積等注意事項。</web-summary>

訂閱 Claude Max 或 Team 方案的使用者，每個月都可以領取一筆 Claude Platform API 額度。這份額度**不會自動入帳**，要先到 claude.ai 的「設定 → 帳單 → API 額度」把帳號連結到一個 API 組織（Console 組織）；綁定一次後，之後每期會自動補發。

<tldr>
- **金額**：Max 5x 每月 US$100、Max 20x 每月 US$200、Team 全團隊共用最多 US$500；Pro 方案不包含。
- **領取**：claude.ai → 設定 → 帳單 → API 額度 → 建立組織或連結組織。
- **不要開自動儲值**：額度用完 API 會直接停止，開了就會從信用卡扣款加值。
</tldr>

## 額度與資格

| 方案 | 每月額度 | 誰可以領取 |
|------|----------|------------|
| Max 5x | US$100 | 訂閱者本人 |
| Max 20x | US$200 | 訂閱者本人 |
| Team（含折扣版） | 最多 US$500（全團隊共用） | Primary Owner 或 Owner |

> Pro 方案不包含這份 API 額度。透過 iOS 或 Android App 訂閱的方案同樣符合資格。
{style="note"}

這項福利由 Claude 開發者官方帳號在 2026 年 10 月初公告，額度可用於任何 Claude 模型。

![Claude 開發者官方帳號公告 Max 與 Team 方案每月 API 額度](claude-devs-api-credits-announcement.png){ thumbnail="true" width="400" }

## 領取步驟

1. 打開 [claude.ai](https://claude.ai)，點左下角的頭像，進入 **設定 → 帳單**。
2. 找到 **API 額度** 區塊，確認上面寫著你的方案每月包含的額度。
3. 如果顯示「您尚未成為任何 API 組織的成員」，點右側的 **建立組織**；如果已經有 API 組織，改選 **連結組織**，再選擇要綁定的組織即可。
4. 頁面會跳轉到 Claude Console，詢問你將如何使用 Claude API。只有自己使用、自行管理 API 金鑰與帳單時選 **個人**（一般選這個）；需要邀請團隊成員、共用 API 存取時才選 **組織**。
5. 依照畫面完成設定。

藍框標出一般情況下要點的 **個人**：

![Claude Console 詢問使用方式，藍框標出自用時要選的「個人」](claude-console-usage-type.png){ width="500" }

## 確認是否領取成功

完成後可以從兩個地方確認：

- **claude.ai → 設定 → 帳單 → API 額度**：顯示組織名稱和「已連結」，並列出每月額度與下次點數發放日期。
- **Claude Console 儀表板**：左上角的「組織點數」會顯示對應金額（例如 US$200.00）。

綠框與標籤標出兩個確認點：「已連結」徽章，以及每月額度金額（圖中為 Max 20x 的 US$200）：

![claude.ai 帳單頁的 API 額度區塊，綠框標出「已連結」與每月額度 US$200](claude-billing-api-credits-linked.png){ thumbnail="true" }

Console 儀表板上，綠框是入帳後的組織點數，紅框是不要點的「開啟自動儲值」，藍框是之後建立金鑰的入口：

![Claude Console 儀表板，綠框標出組織點數 US$200.00，紅框標出不要開啟的自動儲值，藍框標出取得 API 金鑰按鈕](claude-console-org-credits.png){ thumbnail="true" }

## 注意事項

> **不要開啟「自動儲值」。** Console 儀表板上的「開啟自動儲值」會在額度用完時自動從信用卡扣款加值。只想使用免費額度的話請保持關閉，額度用完後 API 請求會直接停止，不會額外收費。
{style="warning"}

- 額度每個帳單週期重置，**沒用完的不會累積到下一期**。
- 綁定一次後，之後每期會自動補發，不需要每個月重新領取。
- 每月額度會優先扣用，用完後才會使用自行購買的點數。
- 這份額度只能用在 Claude Platform（API、Managed Agents、Agent SDK、Playground），**不會增加** Claude App 或 Claude Code 的使用上限。

## 開始使用

- 在 Console 右上角點 **取得 API 金鑰**，建立金鑰後即可在程式中呼叫 Claude API。
- 也可以直接到左側選單的 **Playground** 測試各個模型，同樣會從這份額度扣款。

## 參考資料

- [Monthly API credits for Max and Team plans（Claude 說明中心）](https://support.claude.com/en/articles/17154008)
- [API credits for Max and Team plans（Claude Docs）](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers)
