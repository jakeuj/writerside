# NVM

記錄 NVM 安裝以考古，新的改用 FNM 來管理

## 安裝

[Node.js](https://nodejs.org/zh-cn/learn/getting-started/how-to-install-nodejs)

Node.js 安裝說明建議使用 NVM 來管理 Node.js 版本。

[NVM](https://github.com/nvm-sh/nvm)

NVM 只支援 Mac 和 Linux，Windows 則需要下載 [nvm-windows](https://github.com/coreybutler/nvm-windows/releases)

## NVM 安裝 Node.js

```Shell
nvm install node
nvm use node
```

## FNM

**fnm**（Fast Node Manager）和 **nvm**（Node Version Manager）是用來管理 Node.js 版本的工具，它們都有助於安裝、切換及管理不同的 Node.js 版本。但它們在性能、功能和使用體驗上有所不同，以下是詳細比較：

---

### 1. **安裝與平台支援**

- **fnm**:
  - 使用 Rust 開發，效能較高。
  - 支援多平台：macOS、Linux、Windows。
  - 可透過各種方式安裝（如 Homebrew、scoop 等）。

- **nvm**:
  - 使用 Shell 腳本開發。
  - 主要支援 Unix 系統（macOS 和 Linux）。
  - 在 Windows 上安裝需要使用第三方版本（如 nvm-windows），但功能有限。

---

### 2. **效能**

- **fnm**:
  - 快速切換版本，因為是用 Rust 開發的，啟動和版本切換速度明顯快。
  - 使用符號連結來實現版本管理，性能最佳。

- **nvm**:
  - 切換版本速度較慢，因為需要修改環境變數。
  - 安裝和使用時，Shell 腳本的效率相對較低。

---

### 3. **功能**

- **fnm**:
  - 支援 `.node-version` 或 `.nvmrc` 文件自動加載版本。
  - 有簡單的指令和更佳的用戶體驗。
  - 整合了許多現代功能（例如更簡單的安裝和卸載）。

- **nvm**:
  - 功能穩定，社群支援廣泛。
  - 支援 `.nvmrc` 文件自動切換 Node.js 版本。
  - 插件和工具整合多，但功能相對傳統。

---

### 4. **使用指令**

大多數指令在兩者中相似，但有些差異：

- 安裝 Node.js：
  - **fnm**: `fnm install <version>` 或 `fnm use <version>`
  - **nvm**: `nvm install <version>` 或 `nvm use <version>`

- 查看可用版本：
  - **fnm**: `fnm list`
  - **nvm**: `nvm ls`

---

### 5. **選擇建議**

- 如果你需要更高的效能、更快速的版本切換，並且偏好現代工具，**fnm** 是更好的選擇。
- 如果你已經熟悉 **nvm**，或需要更多社群支援（例如使用舊版 Node.js 開發），**nvm** 仍然是穩定的選擇。

### 總結

- **fnm**：現代、高效、適合快速工作流程。
- **nvm**：穩定、傳統、社群支援廣泛。

如果你剛開始使用 Node.js 版本管理工具，建議試試 **fnm**，其簡單安裝和高效能會讓你有更好的體驗。
