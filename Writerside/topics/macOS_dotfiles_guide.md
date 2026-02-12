# macOS Dotfiles 管理完整指南

## 什麼是 Dotfiles？ {id="what-is-dotfiles"}

Dotfiles 是指在 macOS / Linux 系統中，以「.」開頭的設定檔。這些檔案通常位於使用者家目錄（~）下，用來控制各種 CLI 與開發工具的行為。

常見範例：

- ~/.zshrc
- ~/.gitconfig
- ~/.vimrc
- ~/.ssh/config
- ~/.config/alacritty/alacritty.yml

因為這些檔名都以「dot」開頭，所以統稱為 dotfiles。

---

## 為什麼要管理 Dotfiles？ {id="why-manage-dotfiles"}

當你遇到以下情境時：

- 重灌電腦
- 換新 Mac
- 同時使用多台機器
- 建立新的開發環境

如果沒有版本控制：

- 所有 shell 設定要重建
- alias 要重打
- plugin 要重裝
- terminal 設定要重新調整

管理 dotfiles 的目的是：

✔ 環境可重現  
✔ 版本可追蹤  
✔ 一鍵快速還原  
✔ 團隊可共享

---

## 建議的 Dotfiles 專案結構 {id="dotfiles-structure"}

``` bash
.dotfiles/
├── zsh/
│   ├── .zshrc
│   └── .p10k.zsh
├── git/
│   └── .gitconfig
├── alacritty/
│   └── alacritty.yml
├── brew/
│   └── Brewfile
├── install.sh
└── README.md
```

---

## 使用 Symbolic Link 連結設定檔

範例：

``` bash
ln -s ~/.dotfiles/zsh/.zshrc ~/.zshrc
```

原理：

- 真正編輯的是 .dotfiles 裡的檔案
- 系統實際使用的是 ~ 底下的設定檔
- Git 只需管理 .dotfiles 目錄

---

## Oh My Zsh 建議整合方式

建議不要把整個 oh-my-zsh 專案納入版本控制，而是管理以下內容：

- .zshrc
- plugin 列表
- Powerlevel10k 設定檔
- alias
- 環境變數

範例 plugins 設定：

``` bash
plugins=(
  git
  docker
  kubectl
  zsh-autosuggestions
  zsh-syntax-highlighting
)
```

---

## Homebrew 整合管理

匯出已安裝套件：

``` bash
brew bundle dump --file=~/.dotfiles/brew/Brewfile --force
```

安裝套件：

``` bash
brew bundle --file=~/.dotfiles/brew/Brewfile
```

---

## 建議的 install.sh 範例

``` bash
#!/bin/bash

echo "建立 symbolic links..."

ln -sf ~/.dotfiles/zsh/.zshrc ~/.zshrc
ln -sf ~/.dotfiles/git/.gitconfig ~/.gitconfig

echo "安裝 Homebrew 套件..."
brew bundle --file=~/.dotfiles/brew/Brewfile

echo "完成設定"
```

---

## 新電腦快速還原流程

``` bash
git clone https://github.com/yourname/.dotfiles.git ~/.dotfiles
cd ~/.dotfiles
chmod +x install.sh
./install.sh
```

幾分鐘內即可完成完整開發環境建置。

---

## 進階建議

- 使用 GitHub Private Repo 保存個人設定
- 不要把敏感資訊（如 SSH 私鑰）直接放入 repo
- 可使用 .env 或分離 private config
- 可搭配 chezmoi / stow 進行更進階管理

---

## 結語

Dotfiles 本質上是：

> Developer Environment as Code

透過版本控制，你可以讓自己的開發環境變成可複製、可追蹤、可還原的工程資產。
