# GitHub Projects 草稿不顯示：用 gh 查證與原地轉成 Issue

<web-summary>GitHub Projects 清單為空但草稿仍能依 ID 讀取時，先排除篩選與封存，再用 gh 原地轉換單張 Draft issue，分別驗證資料、清單與畫面，避免重複新增。</web-summary>

Project 顯示 0 項，不代表草稿沒有建立。先用既有 Project item ID 查證；確認任務適合成為正式 Issue 後，可原地轉換一張作為測試，保留卡片關聯與狀態，再確認清單是否恢復。不要因為畫面空白就重複新增或刪除重建。

這是 2026-10-23 的排查紀錄。轉換後的 Issue 稍後能被清單列出，但其餘草稿仍未列出；期間也修改過 Default repository，無法確定哪個動作促成更新，亦未獲 GitHub 確認後端根因。以下名稱與 ID 均為示意值。

## 先分清項目類型 {#item-types}

| 類型 | 所在位置與用途 |
| --- | --- |
| Issue | repository 的正式議題，可加入 Project |
| Pull request | repository 的合併請求，可加入 Project；圖示容易被誤認為一般分支 |
| Draft issue | 只存在 Project 的草稿，可稍後轉成 repository Issue |

右側「Add items to project」是搜尋 repository Issue／PR 並加入的面板，不是既有草稿清單。草稿正常應直接出現在 Project 的表格或看板。

## 本次觀察與證據界線 {#observed-behavior}

本次 35 張既有草稿可依 ID 逐張讀回，都屬於同一 Project、未封存，也都有 Status；檢視沒有篩選條件，但 Project 的 items connection 與 `gh project item-list` 都回傳 0 項。

轉換其中一張後，觀察順序如下：

1. 轉換成功，Project item ID 不變，content 從 `DraftIssue` 改成 `Issue`。
2. Issue 可讀取，反向查詢確認連結原 Project，Status 保持「待辦」。
3. 立即重查清單仍為 0。
4. 使用者調整 Default repository 後，再查變成 1 項，列出剛轉換的 Issue。

這只能證明該 Issue 後來已可由清單查出，不能證明所有草稿已恢復，也不能把轉換或設定預設 repo 說成必定有效的修復。當次尚未取得重新整理後的畫面證據。

## 先查既有資料，不重新建立 {#inspect-existing}

以下範例使用 PowerShell 與 GitHub CLI。帳號需有 Project 與目標 repository 的讀寫權限；遇到權限錯誤先處理授權，不要判定為清單異常。

```powershell
$projectOwner = 'example-owner'
$projectNumber = 7
$repoName = 'example-owner/example-repo'
$projectItemId = 'PVTI_REPLACE_WITH_EXISTING_ITEM_ID'

gh project view $projectNumber --owner $projectOwner --format json
gh project item-list $projectNumber --owner $projectOwner --limit 100 --format json
gh issue list --repo $repoName --state all --limit 100 --json number,title,body,url
```

核對帳號、Project、檢視 filter、封存與分頁。超過查詢上限時繼續分頁；查重包含已關閉 Issue，按任務來源與範圍比對，不能只比標題。

若清單仍空白，使用建立回應保存的 ID 查詢。Project item ID 與 DraftIssue content ID 不同；下列查詢和轉換使用前者。

```powershell
$itemQuery = @'
query($id: ID!) {
  node(id: $id) {
    ... on ProjectV2Item {
      id
      isArchived
      project { id number url }
      content {
        __typename
        ... on DraftIssue { id title body }
        ... on Issue { id number title body url state }
      }
      fieldValueByName(name: "Status") {
        ... on ProjectV2ItemFieldSingleSelectValue { name }
      }
    }
  }
}
'@
gh api graphql -f query=$itemQuery -f id=$projectItemId
```

若 `node` 為空，先核對 ID、帳號與權限。沒有既有 ID 時先找建立紀錄；無法確認就保留診斷缺口，不以重新建立試探。

## 原地轉換一張草稿 {#convert-one}

確認沒有同範圍正式 Issue，且草稿適合公開到目標 repository 後，再轉換。私人 Project 的草稿轉入公開 repository 會成為公開 Issue，內文必須先檢查。

```powershell
$repositoryId = gh repo view $repoName --json id --jq '.id'
if ($LASTEXITCODE -ne 0) { throw '無法取得 repository ID' }

$convertMutation = @'
mutation($item: ID!, $repo: ID!) {
  convertProjectV2DraftIssueItemToIssue(
    input: {itemId: $item, repositoryId: $repo}
  ) {
    item {
      id
      content {
        __typename
        ... on Issue { id number title body url state }
      }
      fieldValueByName(name: "Status") {
        ... on ProjectV2ItemFieldSingleSelectValue { name }
      }
    }
  }
}
'@
gh api graphql -f query=$convertMutation -f item=$projectItemId -f repo=$repositoryId
```

這個 mutation 將既有卡片轉成正式 Issue，不需再執行 `gh issue create` 或 `gh project item-add`。保存回應中的 Issue URL、content ID 與原 Project item ID。

若逾時、502 或回應不明，先用上一節查詢讀回原卡片；已轉成 Issue 就沿用它，不直接重送或另建一張。

## 驗證後才擴大處理 {#verify-result}

```powershell
gh api graphql -f query=$itemQuery -f id=$projectItemId
gh project item-list $projectNumber --owner $projectOwner --limit 100 --format json
```

逐一確認：

- **資料**：原 item ID 不變，content 是 Issue，標題、內文、Project 與 Status 相符，且未封存。
- **清單**：items 包含同一個 item ID 與 Issue URL，不能只看 totalCount 增加。
- **畫面**：回到沒有排除條件的表格／看板，重新整理後確認能看到該項。

寫入成功與清單可見可能不同步。立即查詢仍空白時，稍後做一次有限重查並保留時間與結果；不要無限輪詢或重複建立。單張成功後才評估其餘草稿是否適合轉成正式 Issue；候選研究不會因轉換就成為已核准開發任務。

## Default repository 的作用 {#default-repository}

Project Settings 的 Default repository 決定從 Project 建立新 Issue 時預設使用哪個 repository，變更後需按 Save changes。它不是檢視篩選器，也不等於把所有既有草稿轉成 Issue。

本次 API 轉換明確傳入 `repositoryId`，不依賴 UI 的預設值。設定變更與清單恢復前後相鄰，只是觀察到的時間順序，不能據此確認因果。

## 參考資料 {#references}

- [GitHub Docs：加入 Issue、PR 與草稿](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-items-in-your-project/adding-items-to-your-project)
- [GitHub Docs：Project 的預設 repository](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/adding-your-project-to-a-repository)
- [GraphQL mutation：convertProjectV2DraftIssueItemToIssue](https://docs.github.com/en/graphql/reference/mutations#convertprojectv2draftissueitemtoissue)
- [社群回報：新增成功，但 API 與 UI 清單未顯示](https://github.com/orgs/community/discussions/188487)
- [社群回報：Issue 加入後延遲出現在清單](https://github.com/orgs/community/discussions/208697)

社群回報提供相似症狀的參考，不代表 GitHub 已確認本案例的根因或通用修復方式。
