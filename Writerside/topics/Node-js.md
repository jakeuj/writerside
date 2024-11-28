# Node.js

記錄下 Node.js® 安裝

## 官網
[Node.js®](https://nodejs.org/zh-cn/download/package-manager)

## 安裝

```PowerShell
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

```PowerShell
Add-Content $PROFILE 'fnm env | Out-String | Invoke-Expression'
```

## 找不到 node
環境變數 > Path > 新增
`C:\Users\<您的用戶名>\AppData\Roaming\fnm\node-versions\<Node 版本>\installation`

## Yarn 安裝

![yarn.png](yarn.png)

```Shell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
npm install -g yarn
corepack enable
yarn set version stable
```