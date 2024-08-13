# Node.js

Start typing here...

[Node.js](https://nodejs.org/zh-cn/learn/getting-started/how-to-install-nodejs)

Node.js 安裝說明建議使用 NVM 來管理 Node.js 版本。

[NVM](https://github.com/nvm-sh/nvm)

NVM 只支援 Mac 和 Linux，Windows 則需要下載 [nvm-windows](https://github.com/coreybutler/nvm-windows/releases)

## NVM 安裝 Node.js

```Shell
nvm install node
nvm use node
```

## Yarn 安裝

```Shell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
npm install -g yarn
corepack enable
yarn set version stable
```