# Electron Build

基本打包、額外檔案打包與 deb 打包。

## 打包應用程式

打包要把 Author 與 Homepage 加入 package.json

```json
{
  "author": "Your Name",
  "homepage": "https://your-website.com"
}
```

### 使用 `electron-builder`

```bash
# 安裝 electron-builder
yarn add --dev electron-builder
```

```json
{
  "scripts": {
    "build": "electron-builder"
  }
}
```

```bash
# 打包應用程式
yarn build
```

## 打包額外檔案
package.json
```json
{
  "build": {
    "files": [
      "dist/**/*",
      "public/**/*"
    ],
    "extraFiles": [
      {
        "from": "scripts/",
        "to": "resources/scripts/",
        "filter": ["**/*"]
      }
    ]
  }
}
```

## 打包 deb
package.json
```json
{
  "linux": {
    "target": [
      "deb"
    ]
  }
}
```

## REF
[Sample Code](https://github.com/jakeuj/electron/blob/main/package.json)