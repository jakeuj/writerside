# Evennia 開發 MUD 遊戲起手筆記

Evennia 是用 Python 開發 MUD、MUSH、MUX、MU* 等文字多人遊戲的框架。新專案最短路徑是先建立 Python 虛擬環境，安裝 Evennia，執行 `evennia --init` 產生 game dir，再用 `evennia migrate` 建資料庫、`evennia start` 啟動伺服器；真正的遊戲邏輯主要會落在 `commands/`、`typeclasses/`、`world/` 與 `server/conf/settings.py`。

- 檢視日期：`2026-04-20`
- 主要來源：[evennia/evennia](https://github.com/evennia/evennia)
- 建議閱讀順序：Installation -> Beginner Tutorial -> Game Dir Overview -> Components

## 適用情境

這篇筆記適合想用 Evennia 從零開始做 MUD 或文字 RPG 的開發者，尤其是下面這種情境：

- 想先把本機開發環境與空白 game dir 跑起來
- 想知道 Evennia 產生的資料夾各自負責什麼
- 想理解 Commands、CmdSets、Typeclasses、Attributes、Prototypes 這幾個初期核心概念
- 想用繁體中文玩家指令與文案，但 Python module、class、function 名稱維持英文

如果只是想快速建立一個能登入的空白遊戲，先完成「初始化指令」那一節就夠；如果要開始做玩法，再往後看開發節奏與第一個 command 範例。

## Evennia 是什麼

Evennia 不會替你決定遊戲類型、數值規則或世界觀。它比較像一套多人文字遊戲伺服器框架，先幫你處理：

- 帳號、角色、物件、房間、出口等基礎模型
- Telnet、webclient、website 等連線與網頁入口
- 指令系統、權限、鎖、help、channel、prototype、script 等常用 MUD 基礎設施
- Django database 與 Twisted server runtime

所以開發時心態可以抓成：

- Evennia core 負責伺服器與框架能力
- game dir 負責你的遊戲規則、世界內容、指令、角色與網頁覆寫
- 初期不要改 Evennia core，先在 game dir 內擴充

## 初始化指令

下面用 `uv` 示範，因為它可以同時管理 Python 版本、虛擬環境與依賴。若你想完全照官方文件，也可以把安裝段落改成傳統 `venv + pip install evennia`。

```bash
mkdir my-evennia
cd my-evennia

uv python install 3.14
uv python pin 3.14
uv venv .venv
uv pip install --python .venv/bin/python evennia

.venv/bin/evennia --init game
cd game
../.venv/bin/evennia migrate
../.venv/bin/evennia start
```

啟動後可以用兩種方式連線：

- Web client: `http://localhost:4001`
- MUD client: `localhost:4000`

第一次 `evennia start` 會建立 superuser。官方安裝文件通常用 `mygame` 當 game dir 名稱；實務上目錄名稱不一定要等於正式遊戲名稱，遊戲名稱可以之後在 `server/conf/settings.py` 調整。

## Python 版本怎麼選

Evennia 的版本需求要以你實際安裝的版本為準。以官方 GitHub `main` branch 在 `2026-04-20` 檢視時為例，`pyproject.toml` 寫的是 `requires-python = ">=3.12"`，classifiers 也列出 Python `3.12`、`3.13`、`3.14`。

如果你是使用 PyPI release 或團隊固定版本，建議先看該版本的 `pyproject.toml` 或安裝文件，再決定要 pin 到哪個 Python 版本。

常用判斷：

- 想跟官方文件保守走：選官方安裝文件建議的版本
- 想跟 GitHub main branch 開發：看 repo 內 `pyproject.toml`
- 想固定團隊環境：提交 `.python-version`、`pyproject.toml`、`uv.lock`

## 建議專案結構

一個乾淨的本機專案可以長這樣：

```text
my-evennia/
  .python-version
  .venv/
  pyproject.toml
  uv.lock
  game/
    commands/
    server/
    typeclasses/
    web/
    world/
```

如果你先走 `uv venv` + `uv pip install` 的快速模式，不一定會有 `pyproject.toml` 與 `uv.lock`。若專案會長期維護，建議之後改成 `uv init` + `uv add evennia`，讓依賴可以被版本控制。

## Game dir 重要資料夾

`evennia --init game` 產生的 `game/` 才是主要開發位置。

| 路徑 | 用途 |
| ------ | ------ |
| `commands/` | 放自訂玩家指令、管理指令與 CmdSet 註冊 |
| `commands/command.py` | 自訂 Command base class 或共用 command 行為 |
| `commands/default_cmdsets.py` | 把 command 掛進 Character、Account、Session 等預設 cmdset |
| `typeclasses/` | 放會存進資料庫的遊戲實體，例如 Character、Room、Object、Exit、Script |
| `server/conf/settings.py` | 放遊戲設定覆寫，例如遊戲名稱、typeclass path、port、installed apps |
| `server/conf/secret_settings.py` | 放不適合進版本控制的本機或部署秘密設定 |
| `server/logs/` | `server.log`、`portal.log` 等 runtime log |
| `world/` | 放世界資料、prototype、規則模組、build scripts 或不適合放 typeclass 的內容 |
| `web/` | 覆寫 website、webclient、static、template 或 Django app 相關內容 |

最重要的原則是：`server/` 的結構不要亂改，Evennia 會依賴它；其他資料夾可以依專案習慣重組，但改路徑後要同步調整設定。

## 第一週開發節奏

剛開始不要急著做完整世界，先做一個小 vertical slice，證明你知道「玩家輸入 -> command -> typeclass / attribute -> reload -> 測試」這條鏈怎麼走。

建議順序：

1. 先跑起空白 game dir，能用 web client 或 MUD client 登入。
2. 看懂 `commands/`、`typeclasses/`、`world/`、`server/conf/`。
3. 新增一個 command，掛到 `CharacterCmdSet`。
4. 在 Character 或 Object typeclass 上放一個持久化 Attribute。
5. 用 in-game command 或 `evennia shell` 檢查資料是否真的存在。
6. 用 `evennia reload` 載入程式碼變更。
7. 用 `evennia -l` 看 log，遇到 traceback 先從底部往上讀。
8. 再開始做房間、物件、NPC、原型資料或戰鬥規則。

## 第一個繁體中文 command 範例

先在 `game/commands/mycommands.py` 新增一個簡單 command：

```python
from commands.command import Command


class CmdLookSelf(Command):
    """
    查看自己的狀態。

    Usage:
      看自己
      look self
    """

    key = "看自己"
    aliases = ["look self"]
    locks = "cmd:all()"
    help_category = "遊戲"

    def func(self):
        caller = self.caller
        location = caller.location.key if caller.location else "未知之地"
        caller.msg(f"你是 {caller.key}，目前位於 {location}。")
```

再到 `game/commands/default_cmdsets.py`，把 command 加進 `CharacterCmdSet`：

```python
from evennia import default_cmds
from . import mycommands


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(mycommands.CmdLookSelf)
```

然後在 game dir 裡 reload：

```bash
../.venv/bin/evennia reload
```

登入角色後測試：

```text
看自己
help 看自己
```

這個例子可以驗證三件事：

- 新 command module 可以被 import
- command 已掛到 `CharacterCmdSet`
- docstring 會出現在 Evennia help system

## Commands 與 CmdSets 怎麼想

Evennia 的玩家輸入主要靠 Command system 處理。

| 概念 | 說明 |
| ------ | ------ |
| Command | 一個 Python class，負責 parse input 並執行邏輯 |
| CmdSet | 一組 command 的集合，可以掛在 Character、Account、Object 或 Session 上 |
| CharacterCmdSet | 玩家操控角色時最常改的預設 command set |
| AccountCmdSet | 帳號層級 command，適合放和帳號或 OOC 狀態相關的功能 |
| Object command | 可以掛在物件上，例如鐘、門、機關、商人 NPC |

早期開發時，最常見的作法是：

1. 在 `commands/mycommands.py` 寫 command class。
2. 在 `commands/default_cmdsets.py` import 並 `self.add(...)`。
3. `evennia reload`。
4. 登入遊戲測試 command。

如果是中文 MUD，要早點決定 command 風格：

- 空格式：`看 劍`、`說 你好`
- 緊密式：`看劍`、`拜師張三`

兩種都能做，但不要混亂。若某個中文 command 必須要求分隔符，記得搭配 `arg_regex`，避免短 command 吃掉較長詞。

## Typeclasses 怎麼想

Typeclass 是 Evennia 最核心的資料持久化模型。簡單說，它是「會存進資料庫的 Python class」。

常見 typeclass：

| Typeclass | 對應概念 |
| ------ | ------ |
| `Account` | 玩家帳號 |
| `Character` | 玩家角色或 avatar |
| `Object` | 一般物件 |
| `Room` | 地點、房間、區域節點 |
| `Exit` | 連接 room 的出口 |
| `Script` | 沒有位置但需要持久化或定時執行的系統，例如天氣、經濟、戰鬥 tick |
| `Channel` | 聊天頻道 |

實務判斷：

- 這個東西需要永久存在於世界中：用 Typeclass
- 這個資料只是暫時互動狀態，reload 後消失可接受：可以用 `ndb`
- 這個數值要存在角色或物件上：用 Attribute 或 AttributeProperty
- 這個系統需要定時執行、跨 reload 保留狀態：考慮 Script

不要覆寫 typeclass 的 `__init__` 當作初始化遊戲資料的主要方式；Evennia 文件通常建議使用像 `at_object_creation` 這類 hook。

## Attributes、Tags、Locks、Prototypes 的分工

這幾個概念一開始很容易混在一起，可以先用用途分：

| 概念 | 用途 | 範例 |
| ------ | ------ | ------ |
| Attribute | 存在物件上的持久化資料 | 角色力量、物件重量、NPC 狀態 |
| NAttribute | 暫存資料，不進資料庫 | 暫時選單狀態、當前施法進度 |
| Tag | 搜尋與分類用標籤 | `npc`、`quest-giver`、`region:luoyang` |
| Lock | 權限判斷語法 | 只有 Builder 能編輯，只有持有鑰匙能開門 |
| Prototype | 資料驅動的物件模板 | 不同種類的 goblin、武器、藥草、房間 |

如果你要做很多相似物件，不要每個都寫一個 class。先做共同 typeclass，再用 Prototype 描述不同外觀、數值、裝備與 tags，會比較適合 builder workflow。

## 建議的 MUD 開發切片

不要一開始就做完整戰鬥、完整經濟、完整世界。Evennia 專案比較適合這樣切：

1. Administration
   - superuser、Builder 權限、基本 build 指令、reload 流程
2. Building pipeline
   - room / exit 建立方式、prototype、batch command、區域資料
3. Core systems
   - 角色屬性、技能檢定、戰鬥、物品、貨幣
4. Rooms
   - 描述、details、時間或天氣狀態、出口規則
5. Objects
   - 裝備、消耗品、容器、任務物件
6. Characters
   - 玩家角色、NPC、怪物、商人、對話
7. Content tooling
   - importer、prototype library、地圖或區域資料驗證

每一層都先做一個最小可玩的 demo，再擴大內容量。

## 常用開發命令

下面命令都在 game dir 內執行。

| 命令 | 用途 |
| ------ | ------ |
| `evennia start` | 啟動 Portal 與 Server |
| `evennia start -l` | 啟動並直接看 log |
| `evennia reload` | 熱重載 Server，玩家連線通常不斷線 |
| `evennia stop` | 完整停止 Portal 與 Server |
| `evennia reboot` | stop 後再 start |
| `evennia status` | 看 Portal / Server 狀態 |
| `evennia info` | 看目前服務與 port 設定 |
| `evennia -l` | tail `server/logs` 內的 log |
| `evennia shell` | 開 Django-aware Python shell |
| `evennia migrate` | 套用 database migration |

開發中最常用的是：

```bash
evennia reload
evennia -l
evennia shell
```

## 常見坑

### 改了 Python 檔但遊戲沒反應

先確認有沒有 reload：

```bash
evennia reload
```

如果 reload 卡住，通常是語法錯誤或 import error。用：

```bash
evennia -l
```

看 `server.log` 或 `portal.log`，從 traceback 底部往上讀。

### `evennia` command 找不到

通常是虛擬環境沒有啟用，或 IDE / terminal 用到不同 Python。

如果使用 `.venv`，可以明確執行：

```bash
.venv/bin/evennia --help
```

或在 game dir 裡用上一層環境：

```bash
../.venv/bin/evennia status
```

### 不知道程式碼路徑怎麼寫

Evennia 常用 Python path 指向 game dir 內的 class。假設檔案是：

```text
game/typeclasses/mobs.py
```

class 是：

```python
class Goblin(Object):
    pass
```

常見 typeclass path 會寫成：

```text
typeclasses.mobs.Goblin
```

也就是把 `/` 換成 `.`，省略 `.py`，最後加上 class 名稱。

### 一開始就想重做所有預設 command

先不要。預設 command 是很好的起點；初期優先新增自己的 command，或只覆寫你真的需要改的那一個。等你理解 CmdSet merge 與 lock 行為後，再考慮大規模替換。

## 延伸閱讀

- [Evennia GitHub repo](https://github.com/evennia/evennia)
- [Evennia Installation](https://www.evennia.com/docs/latest/Setup/Installation.html)
- [Evennia Beginner Tutorial](https://www.evennia.com/docs/latest/Howtos/Beginner-Tutorial/Beginner-Tutorial-Overview.html)
- [Game Dir Overview](https://www.evennia.com/docs/latest/Howtos/Beginner-Tutorial/Part1/Beginner-Tutorial-Gamedir-Overview.html)
- [Core Components](https://www.evennia.com/docs/latest/Components/Components-Overview.html)
- [Commands](https://www.evennia.com/docs/latest/Components/Commands.html)
- [Command Sets](https://www.evennia.com/docs/latest/Components/Command-Sets.html)
- [Typeclasses](https://www.evennia.com/docs/latest/Components/Typeclasses.html)
- [Prototypes](https://www.evennia.com/docs/latest/Components/Prototypes.html)
