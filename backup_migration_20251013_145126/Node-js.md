# Node.js

記錄下 Node.js® 安裝

## 官網
[Node.js®](https://nodejs.org/zh-cn/download/package-manager)

## 安裝

```Shell
# 安装 fnm (快速 Node 管理器)
winget install Schniz.fnm
# 配置 fnm 环境
fnm env --use-on-cd | Out-String | Invoke-Expression
# 下载并安装 Node.js
fnm use --install-if-missing 18
# 验证环境中是否存在正确的 Node.js 版本
node -v # 应该打印 `v18.20.5`
# 验证环境中是否存在正确的 npm 版本
npm -v # 应该打印 `10.8.2`
```

## 找不到 FNM

```Shell
Add-Content $PROFILE 'fnm env | Out-String | Invoke-Expression'
```

## 找不到 node
先考慮全局固定在某版本還是隨FNM變動對開發環境比較方便，然後到系統 > 環境變數 > Path > 新增下方其中一個路徑

- FNM 目前指向的版本
  - `C:\Users\<您的用戶名>\AppData\Roaming\fnm\aliases\default`
- 固定版本 (V18 是在 `\installation`，其他版本可能在 `\installation\bin`)
  - `C:\Users\<您的用戶名>\AppData\Roaming\fnm\node-versions\<Node 版本>\installation`

比如 ABP Studio 要求 V18，並且無法使用 fnm 切版本，另外我有 Electron 需要隨不同專案變動 node 版本，所以我選擇固定 V18，然後在專案中使用 FNM

## Yarn 安裝

![yarn.png](yarn.png)

```Shell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
npm install -g yarn
corepack enable
yarn set version stable
```