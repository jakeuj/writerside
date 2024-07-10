# Vue

筆記一下初次使用 VUE 3 的過程。

## Prerequisites

Vue3 是 Vue.js 的下一代版本，它的目標是提供更快的渲染速度、更小的 bundle 大小、更好的 TypeScript 支持。

[官方文件](https://zh-hk.vuejs.org/guide/quick-start)

根據文件需要先準備 Node.js

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

## 建立 Vue3 專案

```Shell
yarn create vue@latest
```

## 執行

```Shell
cd vue-project
yarn
yarn dev
```