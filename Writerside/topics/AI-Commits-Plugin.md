# AI Commits Plugin

使用 GPT-3 生成代码提交信息。
![plugin.gif](plugin.gif)

## 安裝
[AI Commits](https://plugins.jetbrains.com/plugin/21335-ai-commits)

![ai-commit.png](ai-commit.png)

## 設定
設定 > 工具 > AI Commits > OpenAI API Key
![open-ai-key.png](open-ai-key.png)
Token 可以在 [OpenAI](https://platform.openai.com/account/api-keys) 獲取。
![Token.png](Token.png)

## 使用
提交時點擊 AI Commits 按鈕，即可生成提交信息。
![commit-msg.png](commit-msg.png)

## 結果
![Sc.png](Sc.png)

## 備註
有需要可以自行調整 prompt，可以將 Commit 改成中文，目前測試用 gpt4o 比較正常。

```
使用下面提供的差異，根據 Conventional Commits 格式創建一條簡潔的提交訊息（例如 "🐛 修正(types): 修正 types 中的導入"）。
訊息應以適當的表情符號開始，以突出變更的性質。
使用過去式和第一人稱進行表述。確保行數不超過 74 個字元。
如果不確定確切的措辭，請提供幾個提交訊息選項。
如果差異沒有提供足夠的信息來確定提交的目的，請專注於具體的變更，而不是試圖猜測意圖。
使用單行代碼塊來表示變數名、文件路徑或任何與代碼相關的元素。

內部術語表：
"Instance" 意思是 "bot", "бот"
表情符號使用指南：
🐛 修正: 用於錯誤修正。
✨ 功能: 用於新功能。
📄 文件: 用於文檔變更。
♻️ 重構: 用於重構代碼而不改變功能。
🚀 性能: 用於性能改進。
🔒 安全: 用於安全相關修復。
🚧 任務: 用於維護任務。
🧪 測試: 用於測試
{Author's notes: "$hint"}

你的回應應僅包含提交訊息，不包含其他說明或格式。避免冗長，這是 git diff --staged 命令的輸出：{diff}
```

![ai-commit-cht.png](ai-commit-cht.png)

![ai-act-cht.png](ai-act-cht.png)