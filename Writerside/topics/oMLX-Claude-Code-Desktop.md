# oMLX Claude Code Desktop

記錄最短 oMLX 本地模型直接給 Claude Code Desktop 使用的方式。

## 結論
- 需要在 oMLX 設定模型別名，格式為 `claude-*`。

## 設定模型別名
1. 選擇模型

![model_settings.png](model_settings.png)

2. 設定別名

![model_alias.png](model_alias.png)

- 名稱必須符合格式 `claude-*`, 比如：`claude-opus-4`

## 設定 Claude Code Desktop 使用本地模型

1. 打開 Claude Code Desktop，上方 Help -> troubleshooting -> Enable Developer Mode。

![claude_troub.png](claude_troub.png)

2. 上方會多出 Developer 選單，點擊 Developer -> Configure Third-Party Inference...。

![claude_dev.png](claude_dev.png)

3. Connection -> 
  - 設定 base URL 為 `http://127.0.0.1:8000`
  - 設定 API Key 為你在 oMLX 設定的密碼。
  - 設定 model ID 為你在 oMLX 設定的模型別名。比如：`claude-opus-4`
  - 選擇性 設定 Display Name 為原始模型名稱，以利後續辨識。

![claude_setting.png](claude_setting.png)

## Claude Cli
oMLX 也可以直接給 Claude Cli 使用，oMLX 內建整合模式，設定後 `omlx launch claude`。

![claude_cli.png](claude_cli.png)

也可以直接於命令列使用

```bash
ANTHROPIC_BASE_URL='http://127.0.0.1:8000' 
ANTHROPIC_AUTH_TOKEN='你的密碼' 
ANTHROPIC_DEFAULT_OPUS_MODEL='Ornith-1.0-35B-8bit' 
ANTHROPIC_DEFAULT_SONNET_MODEL='Ornith-1.0-35B-8bit' 
ANTHROPIC_DEFAULT_HAIKU_MODEL='Ornith-1.0-35B-8bit' 
API_TIMEOUT_MS=3000000 
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 
claude
``` 

來直接啟動 claude cli。


## 備註
也可以額外安裝 [cc-switch](https://github.com/farion1231/cc-switch) 來切換模型，裡面可以修改模型名稱對應。


