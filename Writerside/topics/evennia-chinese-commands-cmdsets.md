# Evennia 中文指令解析與 CmdSet 實作

<web-summary>在 Evennia 6.1 實作繁體中文玩家指令，用 arg_regex 決定空格與緊密式輸入，並以 CmdSet 的 priority、Union 與持久化設定處理指令覆寫及暫時互動。</web-summary>

中文指令先用內建 parser 即可。以 `arg_regex` 決定指令名稱後是否需要空格，再用 CmdSet 管理可用指令；只有輸入語法已超出預設 parser 能力時，才另寫 parser。

- 檢視日期：`2026-10-07`
- 範例基準：Evennia `6.1.0`、Python `3.14`，game dir 名稱為 `game`
- 前置作業：[Evennia 開發 MUD 遊戲起手筆記](evennia-mud-development.md)

## 指令名稱與參數的邊界 {#chinese-command-boundary}

預設 parser 不要求指令名稱與參數之間一定有空格；`key = "端詳"` 可以處理 `端詳劍`。原始 `self.args` 可能仍帶有開頭空格，因此由 `parse()` 統一整理，`func()` 再使用整理過的參數。

| 輸入風格 | 範例 | `arg_regex` |
| ------ | ------ | ------ |
| 空格分隔，也允許單獨輸入指令 | `察看 劍`、`察看` | `r"\s.*$\|$"` |
| 名稱後允許直接接參數 | `端詳劍`、`端詳 劍` | `r".*"` |
| 保留 MUX switches | `look/switch target` | 使用 MuxCommand 的解析方式並確認 separator 規則 |

`arg_regex` 是檢查「指令名稱後面的字串」，不是解析整行的正規表示式。允許空參數只表示 parser 可找到這個 command，是否顯示用法或執行預設動作，由 `func()` 決定。

## 建立兩種中文指令 {#chinese-command-implementation}

新增 `game/commands/chinese.py`。這裡使用 game dir 的 Command base class，保留預設英文 `look`，以兩個新中文指令示範邊界規則：

```python
from commands.command import Command
from evennia import CmdSet


class CmdInspect(Command):
    """察看目標。用法：察看 <目標> 或 inspect <目標>。"""

    key = "察看"
    aliases = ["inspect"]
    locks = "cmd:all()"
    help_category = "遊戲"
    arg_regex = r"\s.*$|$"

    def parse(self):
        self.target_name = self.args.strip()

    def func(self):
        if not self.target_name:
            self.caller.msg("用法：察看 <目標>")
            return
        target = self.caller.search(self.target_name)
        if target and target.access(self.caller, "view"):
            self.caller.msg(target.return_appearance(self.caller))
        elif target:
            self.caller.msg("你無法察看這個目標。")


class CmdExamine(CmdInspect):
    """端詳目標。用法：端詳<目標> 或 examine <目標>。"""

    key = "端詳"
    aliases = ["examine"]
    arg_regex = r".*"

    def func(self):
        if not self.target_name:
            self.caller.msg("用法：端詳<目標>")
            return
        super().func()


class CmdFocusedInspect(CmdInspect):
    """專注察看目標。用法：察看 <目標>。"""

    def func(self):
        self.caller.msg("你集中精神。")
        super().func()


class FocusCmdSet(CmdSet):
    key = "FocusCmdSet"
    priority = 10
    mergetype = "Union"

    def at_cmdset_creation(self):
        self.add(CmdFocusedInspect)
```

`search()` 負責尋找目前可搜尋的目標，`view` lock 決定能否查看，`return_appearance()` 則取得外觀。不要只用找到物件與否代替權限判斷。

## 加入 CharacterCmdSet {#chinese-command-registration}

在 `game/commands/default_cmdsets.py` 的既有 `CharacterCmdSet` 加入兩個 command；其他 Account、Session、Unloggedin cmdset 保留原本內容：

```python
from evennia import default_cmds
from .chinese import CmdInspect, CmdExamine


class CharacterCmdSet(default_cmds.CharacterCmdSet):
    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        super().at_cmdset_creation()
        self.add(CmdInspect)
        self.add(CmdExamine)
```

在 game dir 執行 `evennia reload`，登入並操控角色後測試。只有寫好 Python class，沒有註冊 CmdSet，玩家仍無法執行。

若用明確的虛擬環境路徑：

```bash
../.venv/bin/evennia reload
```

## 用輸入矩陣驗證 parser {#chinese-command-input-matrix}

用 Builder 帳號在遊戲內建立測試物件：

```text
create 劍
desc 劍 = 一把用來測試中文指令的木劍。
```

接著確認以下結果。Command 的邊界規則同時作用於 `key` 和 `aliases`：

| 輸入 | 預期結果 |
| ------ | ------ |
| `察看 劍` | 顯示木劍外觀 |
| `察看　劍` | 全形空格也可分隔，顯示木劍外觀 |
| `察看` | 顯示 `用法：察看 <目標>` |
| `察看劍` | 此 command 不匹配；沒有其他匹配指令時顯示找不到指令 |
| `端詳劍` | 顯示木劍外觀 |
| `端詳 劍` | 顯示木劍外觀 |
| `端詳` | 顯示 `用法：端詳<目標>` |
| `inspect 劍` | 顯示木劍外觀 |
| `inspect劍` | 此 command 不匹配 |
| `help 察看`、`help 端詳` | 顯示各自的 docstring |

若同時有 `察看` 與 `察看自己` 等不同長度的指令，要一起測試。`arg_regex` 限制邊界，並不保證所有 CmdSet 合併後都沒有別名衝突。

## 用 Union 暫時覆寫一個指令 {#chinese-command-focus-cmdset}

上述 `FocusCmdSet` 以 priority `10` 合併到預設 priority `0` 的 CharacterCmdSet。同名的 `察看` 被專注版本覆寫，其餘一般角色指令繼續可用。

以開發者帳號在遊戲內執行：

```text
py self.cmdset.add("commands.chinese.FocusCmdSet", persistent=True)
察看 劍
端詳劍
look
```

`察看 劍` 應先顯示「你集中精神。」再顯示外觀；`端詳` 與 `look` 仍可執行。測試完移除：

```text
py self.cmdset.remove("FocusCmdSet")
察看 劍
```

此時 `察看` 應回到一般版本。移除用的是 cmdset 的 key，不是 command 的 key。

`persistent=True` 表示這個動態加入的 CmdSet 會被記錄並於 reload 後恢復；省略時預設不持久化。可先加入、reload、確認專注版本仍存在，再移除並 reload，確認已解除。臨時 UI 是否需要持久化，要依互動能否在 reload 後恢復來決定。

## 合併規則與衝突排查 {#chinese-command-merge-rules}

| 合併方式 | 用途 |
| ------ | ------ |
| `Union` | 保留兩組指令；本例用較高 priority 的同名指令覆寫 |
| `Replace` | 用較高 priority 的集合取代較低 priority 的集合 |
| `Intersect` | 保留兩組共有的指令 |
| `Remove` | 從另一組排除指定指令 |

不要把 `Replace` 當作覆寫單一 command 的預設做法；它可能連其他一般指令一起移除。Exit 與 Channel 等其他來源還有自己的 priority，是否納入也受到 `no_exits`、`no_channels`、`no_objs` 影響；只設定一個 `Replace` 並不等於封鎖所有操作。

排查時先核對 command 的 `key`、全部 aliases、CmdSet 註冊位置與 priority，再看 locks。相同 priority 的物件 command 可能保留重複候選並產生 multimatch，不應假定永遠只剩一個同名指令。

自訂 parser 應保留與 Evennia `6.1.0` 相容的呼叫介面，包括 `session`；這版對缺少 `session` 參數的自訂 parser 加入棄用提醒。單純中文指令通常不需要走到這一步。

## 參考資料 {#chinese-command-references}

- [Evennia Commands](https://www.evennia.com/docs/latest/Components/Commands.html)
- [Evennia Command Sets](https://www.evennia.com/docs/latest/Components/Command-Sets.html)
- [Evennia 6.1.0 parser 原始碼](https://github.com/evennia/evennia/blob/v6.1.0/evennia/commands/cmdparser.py)
- [Evennia Changelog](https://github.com/evennia/evennia/blob/main/CHANGELOG.md)
- [Evennia 時間與狀態更新機制怎麼選](evennia-time-state-updates.md)
