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
有需要可以自行調整 prompt。

```
撰寫一條見解深刻但簡潔的 Git 提交訊息，使用完整的現在時態句子，不需要任何前言，回應必須以 {locale} 語言撰寫，且不超過 74 個字符。
傳送的文本將是文件之間的差異，其中刪除的行前綴一個減號，新增的行前綴一個加號。{使用這個提示來改進此提交訊息：$hint }{diff}
```

![ai-ch.png](ai-ch.png)

可以將 Commit 改成中文，目前測試用 gpt4 比較正常。

![ai-result.png](ai-result.png)