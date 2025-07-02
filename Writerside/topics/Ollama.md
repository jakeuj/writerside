# Ollama

安裝 Ollama 執行 DeepSeek R1 (預設是 8B 模型)

## 安裝

MacOS
```bash
brew install ollama
```

Ubuntu

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## 使用

```bash
ollama run deepseek-r1:
```

## API

```bash
curl http://localhost:11434/api/generate -X POST -H "Content-Type: application/json" -d '{"model":"deepseek-r1:","prompt":"Hello, world!"}'
```

## 臨時開放外部呼叫

```bash
sudo systemctl stop ollama.service
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

## 自動開放外部呼叫

```bash
sudo systemctl stop ollama.service
sudo systemctl edit ollama.service
```

```
### Editing /etc/systemd/system/ollama.service.d/override.conf
### Anything between here and the comment below will become the new contents of the file

# 加入下面這兩行
[Service] 
Environment="OLLAMA_HOST=0.0.0.0:11434"
#下面的不要碰

### Lines below this comment will be discarded

### /etc/systemd/system/ollama.service
# [Unit]
# Description=Ollama Service
# After=network-online.target
#
# [Service]
# ExecStart=/usr/local/bin/ollama serve
# User=ollama
# Group=ollama
# Restart=always
# RestartSec=3
# Environment="PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games"
#
# [Install]
# WantedBy=default.target
```

```bash
sudo systemctl start ollama.service
```

用另一台電腦測試是否可以打 API

```bash
curl http://{your_ip_address}:11434/api/generate -X POST -H "Content-Type: application/json" -d '{"model":"deepseek-r1:","prompt":"Hello, world!"}'
```

## python

```python
from ollama import Client
client = Client(
  host='http://localhost:11434',
  headers={'x-some-header': 'some-value'}
)
response = client.chat(model='deepseek-r1:', messages=[
  {
    'role': 'user',
    'content': '为什么天空是蓝色的？',
  },
])
print(response)
```

## 參考

- [ollama](https://ollama.com/download/linux)
- [open-web-ui-with-ollama/](https://imuslab.com/wordpress/2024/07/13/open-web-ui-with-ollama/)
- [Python Ollama API](https://github.com/datawhalechina/handy-ollama/blob/main/docs/C4/2.%20%E5%9C%A8%20Python%20%E4%B8%AD%E4%BD%BF%E7%94%A8%20Ollama%20API.md){ignore-vars="true"}