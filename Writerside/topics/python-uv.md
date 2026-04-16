# Python uv 筆記：固定 Python 3.14、建立虛擬環境、在 PyCharm 與 Evennia 使用

如果你是從 `venv + pip` 轉到 `uv`，最重要的觀念只有三個：`uv python pin` 是固定專案預設 Python 版本、`uv venv` 是建立虛擬環境、`uv pip install` 或 `uv add` 才是安裝依賴。對大多數新專案，先用 Python 3.14 建好 `.venv`，再決定要走快速環境模式還是完整專案模式，就已經足夠穩定。

- 快速建環境：`uv python pin 3.14` -> `uv venv .venv` -> `uv pip install --python .venv/bin/python <package>`
- 完整專案：`uv init` -> `uv add <package>` -> `uv run <command>`
- PyCharm 的 `Set up uv env` 只會建立或選擇 interpreter，不會自動幫框架完成初始化

## 先分清楚 uv 在做哪一層的事

`venv` 沒有過時，它只是職責比較單純，主要負責建立虛擬環境。`uv` 則把 Python 版本、虛擬環境、套件安裝、依賴解析、lock file 與執行流程整合在一起，所以在新專案裡通常更順手。

| 工具 | 主要工作 | 適合什麼情境 |
| ------ | ---------- | -------------- |
| `venv` | 建立虛擬環境 | 只想先隔離環境，不需要 lock file 或完整專案工作流 |
| `pip` | 安裝套件 | 已經有環境，只想安裝或升級套件 |
| `uv` | 管理 Python、虛擬環境、依賴、lock file 與執行 | 新專案、想重現依賴、想減少工具切換 |

實務上可以這樣記：

- `uv venv` 比較像是「用現代工具建立 `.venv`」
- `uv pip install` 比較像是「在指定環境裡裝套件」
- `uv add` 則是「把依賴寫進 `pyproject.toml`，並同步更新環境與 lock file」

## 路徑一：只想快速建一個乾淨的 `.venv`

如果你只是想在目前資料夾快速建立一個專案環境，不急著先建 `pyproject.toml`，可以走這條路。

```bash
uv python pin 3.14
uv venv .venv
.venv/bin/python --version
uv pip install --python .venv/bin/python <package-name>
```

例如安裝 `requests`：

```bash
uv python pin 3.14
uv venv .venv
uv pip install --python .venv/bin/python requests
.venv/bin/python -c "import requests; print(requests.__version__)"
```

這條路的重點有三個：

- `uv python pin 3.14` 會在專案根目錄建立 `.python-version`，讓這個專案預設優先用 Python 3.14
- `uv venv` 預設會建立 `.venv`
- 不想 `source .venv/bin/activate` 也沒關係，直接用 `.venv/bin/python`、`.venv/bin/pip` 或 `uv run` 就能工作

## 路徑二：要 lock file 與可重現依賴

如果你要的是完整專案工作流，而不是單純一個環境，先建立 `pyproject.toml` 會比較合理。

```bash
uv init --app .
uv python pin 3.14
uv add requests
uv run python --version
```

這條路和前一條的差別在於：

- `uv init` 會把目前目錄初始化成 `uv` 專案
- `uv add` 需要在有 `pyproject.toml` 的專案中執行
- `uv add` 會更新專案依賴，並同步處理環境與 lock file

如果你看到 `uv add` 報「找不到 project」，通常就是因為你還沒先跑 `uv init`。

## `uv python pin`、`uv venv --python` 差在哪裡

兩者都能讓你用 Python 3.14 建環境，但用途不同。

- `uv python pin 3.14`
  - 設定目前專案的預設 Python 版本
  - 適合長期維護的專案
- `uv venv --python 3.14 .venv`
  - 只對這次建立環境生效
  - 適合單次建立或臨時測試

如果你每次都希望 `uv venv` 預設用 3.14，優先在專案根目錄固定：

```bash
uv python pin 3.14
```

如果你只想這次明確指定：

```bash
uv venv --python 3.14 .venv
```

## `uv` 不一定要 activate

`uv` 一個很好用的地方是，它會優先尋找目前目錄或上層目錄的 `.venv`，所以很多情況下不必先 activate。

例如：

```bash
uv run python --version
uv run python -m pip list
```

但在下面這些情境，還是很常需要明確選 interpreter 或 activate：

- IDE 要綁定專案 interpreter
- 你想直接執行 `.venv/bin/python`
- 某些教學文件或框架工具預設仍假設你已經進入虛擬環境

## PyCharm 的 `Set up uv env` 是什麼

在 PyCharm 裡，`Set up uv env` 的意思通常是：

- 幫這個專案建立或掛上 `uv` 管理的虛擬環境
- 把它設成目前專案的 Python interpreter

它不會幫你自動完成 Django、FastAPI、Evennia 這類框架初始化。換句話說：

- `Set up uv env` 是在準備 Python 環境
- `django-admin startproject`、`evennia --init game` 這類命令，才是在建立框架專案

如果 PyCharm 畫面先顯示 Python 3.12，不一定代表 3.14 不支援，通常只是它先抓到目前已存在的可用版本。想固定用 3.14 時，先在 terminal 跑：

```bash
uv python install 3.14
uv python pin 3.14
```

然後回 PyCharm 選 `.venv/bin/python` 或重新建立一次 `uv` interpreter。

## 用 `uv` 初始化 Evennia 的最短路徑

如果你是要建立一個 Evennia MUD 專案，`uv` 負責的是 Python 環境與套件；真正建立 Evennia game dir 的命令，仍然是 `evennia --init`。

```bash
mkdir my-evennia
cd my-evennia

uv python pin 3.14
uv venv .venv
uv pip install --python .venv/bin/python evennia

.venv/bin/evennia --init game
cd game
../.venv/bin/evennia migrate
../.venv/bin/evennia start
```

如果你想再多走一步，把專案也納入 `uv` 的依賴管理，可以改成：

```bash
mkdir my-evennia
cd my-evennia

uv init --app .
uv python pin 3.14
uv add evennia

uv run evennia --init game
cd game
../.venv/bin/evennia migrate
../.venv/bin/evennia start
```

第一條比較直覺，第二條比較適合你已經決定要把 `pyproject.toml`、`uv.lock` 一起納入版本控制。

## 常見問題

### 為什麼 `python3 -m pip install --upgrade pip` 會出現 `externally-managed-environment`

如果你的 Python 是 Homebrew、系統套件管理器或其他外部工具安裝的，全域 `pip` 可能會被 PEP 668 保護，避免你直接改壞系統環境。

這時候正確作法通常不是強行加 `--break-system-packages`，而是改成在專案裡使用 `uv venv` 或 `python -m venv` 建自己的虛擬環境，再在裡面安裝套件。

### 為什麼 `python` 和 `python3` 版本不一樣

一台機器上同時有 Homebrew Python、pyenv Python、系統 Python 很常見，所以：

- `python` 可能是某個舊版本
- `python3` 可能是另一個版本
- PyCharm 與 `uv` 也可能各自找到不同的 interpreter

最簡單的驗證方式是直接看你要用的那一個：

```bash
python3 --version
uv run python --version
.venv/bin/python --version
```

### 什麼時候用 `uv pip install`，什麼時候用 `uv add`

可以用這個原則分：

- 只想把套件裝進某個現有環境，選 `uv pip install`
- 想把依賴寫進專案設定並追蹤 lock file，選 `uv add`

如果你還在快速試驗階段，`uv pip install` 比較直接。確定專案會長期維護後，再切到 `uv init` + `uv add` 通常比較自然。

### 重建 `.venv` 前先注意什麼

如果你打算刪掉舊環境重建，先確認目前專案裡沒有重要的手動安裝內容只存在於 `.venv`。比較保險的做法是把依賴寫回 `pyproject.toml` 或其他可版本控制的檔案，讓環境可以真正重建。

## 參考資料

- [uv 官方文件](https://docs.astral.sh/uv/)
- [uv Python versions](https://docs.astral.sh/uv/concepts/python-versions/)
- [PyCharm: Configure a uv environment](https://www.jetbrains.com/help/pycharm/uv.html)
- [Evennia Installation and Running](https://www.evennia.com/docs/latest/Setup/Setup-Overview.html#installation-and-running)
