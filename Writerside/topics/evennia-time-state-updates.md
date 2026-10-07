# Evennia 時間與狀態更新機制怎麼選

<web-summary>在 Evennia 6.1 依玩法選擇時間戳、delay、Script、TickerHandler 或 OnDemandHandler，用冷卻、延後通知、天氣與植物生長範例說明持久化、停止訂閱和伺服器停機時間的差異。</web-summary>

先判斷「時間到了是否一定要主動執行」。只在玩家操作時需要答案的冷卻或生長狀態，可以查詢時計算；必須主動通知的事件才安排 callback。需要保存整個系統狀態時用 Script，多個訂閱者共用固定間隔時用 TickerHandler。

- 檢視日期：`2026-10-07`
- 範例基準：Evennia `6.1.0`、Python `3.14`
- 前置作業：[Evennia 開發 MUD 遊戲起手筆記](evennia-mud-development.md)

## 依需求選工具 {#time-tool-selection}

| 需求 | 建議工具 | 例子 |
| ------ | ------ | ------ |
| 操作時檢查是否到期 | 持久化時間戳 | 技能冷卻、商店刷新期限 |
| 延後主動執行一次 | `utils.delay` | 幾秒後回報休息完成 |
| 保存系統資料，可選擇加 timer | Script | 世界時鐘、經濟系統、戰鬥回合 |
| 多個訂閱者共用固定更新間隔 | TickerHandler | 對訂閱房間發送天氣訊息 |
| 查詢時推算分段狀態 | OnDemandHandler | 藥草從幼苗到成熟 |
| 某個事件發生後立即反應 | 既有 hook 或直接通知 | 拾取物品後更新任務進度 |

不要每秒掃描所有角色去猜測任務或背包有沒有改變。能在變更發生時通知的事情，直接放在對應行為或 hook；定時器無法降低這種輪詢的成本。

## 冷卻用時間戳，不必建立 timer {#time-cooldown-timestamp}

新增 `game/world/timing.py`，先放兩個小函數：

```python
import math
import time


def begin_cooldown(character, seconds=30):
    character.db.skill_ready_at = time.time() + seconds


def cooldown_remaining(character):
    ready_at = character.db.skill_ready_at or 0
    return max(0, math.ceil(ready_at - time.time()))
```

使用技能時先檢查 `cooldown_remaining()`；回傳 `0` 才執行效果並呼叫 `begin_cooldown()`。到期前不用安排背景工作，也不會有重複訂閱。

在開發遊戲內測試：

```text
py from world.timing import begin_cooldown; begin_cooldown(self, 30)
py from world.timing import cooldown_remaining; self.msg(cooldown_remaining(self))
```

這裡用的是現實 UTC epoch 時間戳，因此停機時間也算進冷卻；reload 後 `.db` 的期限仍存在。它依賴系統時鐘，若玩法需要暫停時計時或不受時鐘校正影響，應另選符合需求的時間來源。

## 延後通知用 delay {#time-delay-notification}

在同一個 `world/timing.py` 加入：

```python
from evennia.utils import delay


def notify_rest_finished(character):
    if character and character.pk:
        character.msg("休息完成。")


def schedule_rest_notification(character, seconds=5):
    return delay(
        seconds,
        notify_rest_finished,
        character,
        persistent=True,
    )
```

callback 放在可 import 的模組頂層，持久化時才能在重啟後重新找到。不要用 lambda、區域函數或暫時 Command instance 當持久化 callback。執行時仍應重查角色是否存在，以及事件是否已被取消或失效。

```text
py from world.timing import schedule_rest_notification; task = schedule_rest_notification(self)
```

等待期間可繼續輸入其他指令。`delay` 預設不持久化，本例明確設 `persistent=True`；期限在停機期間已過的持久化工作，會在啟動後執行。玩家當時沒有連線時，`character.msg()` 不是離線信箱，不能假定玩家一定看得到。

需要取消時，用 `task.get_id()` 取得 `TaskHandlerTask` 的 ID，再透過 `TASK_HANDLER.remove(task_id)` 移除工作。若期限必須在 reload 後仍能取消，將 ID 存入 Attribute；不要只保留在 command 的區域變數。本文通知範例只排程一次；重複呼叫會建立多個工作。

不要在 command 使用 `time.sleep()` 等待，它會阻塞伺服器處理其他玩家輸入。

## 有系統資料與週期工作時用 Script {#time-script-clock}

新增 `game/typeclasses/timed_systems.py`：

```python
from typeclasses.scripts import Script


class WorldClock(Script):
    def at_script_creation(self):
        self.key = "world-clock"
        self.interval = 60
        self.start_delay = True
        self.repeats = 0
        self.persistent = True
        self.db.ticks = 0

    def at_repeat(self):
        self.db.ticks += 1
```

以開發者帳號建立一次：

```text
py from evennia import create_script; create_script("typeclasses.timed_systems.WorldClock")
```

此示例每次 callback 累加一次 tick，保存的是執行次數，不能直接拿來當準確的現實分鐘數；停機或 callback 延遲時不會自動補齊所有漏掉的分鐘。若要以經過時間計算結果，另記錄時間基準。

重複 `create_script()` 會建立多個 Script；長期系統可透過 `GLOBAL_SCRIPTS` 設定與管理，或在建立前明確檢查既有實例。Script 的 `.stop()` 停止 timer，不會刪除 Script 資料；要移除系統實例需另呼叫 `.delete()`。

Script 可以只作為持久化系統容器，不一定需要 timer。只為延後呼叫一次而建立 Script，通常比 `delay` 多了不必要的管理工作。

## 多個房間共用 ticker {#time-weather-ticker}

在 `world/timing.py` 加入天氣訂閱函數：

```python
from evennia import TICKER_HANDLER


def start_weather(room):
    return TICKER_HANDLER.add(
        60,
        room.msg_contents,
        idstring="weather",
        persistent=True,
        text="一陣涼風吹過。",
    )


def stop_weather(room):
    TICKER_HANDLER.remove(
        60,
        room.msg_contents,
        idstring="weather",
        persistent=True,
    )
```

在遊戲內訂閱與取消目前所在房間：

```text
py from world.timing import start_weather; start_weather(self.location)
py from world.timing import stop_weather; stop_weather(self.location)
```

這是廣播訊息的最小示例；真正的天氣系統通常還要保存區域天氣狀態。同間隔的訂閱共用 ticker，但每個房間的 callback 仍會被呼叫，不代表所有遊戲邏輯只執行一次。

訂閱身分包含 callback、interval、`idstring` 與 `persistent`；移除時必須一致。重複呼叫本例的 `start_weather(room)` 會更新同一訂閱，換成不同 idstring 才會另外建立訂閱。

`persistent=False` 的 ticker 仍可跨正常 reload，完整 shutdown 後不恢復。callback 與傳入參數即使不跨 shutdown，也仍受序列化限制。

不要混用位置參數與關鍵字參數順序。若 callback 需要位置參數，必須先依序提供 `idstring` 與 `persistent`；通常改用具名參數比較容易核對。不要在正常停止某一個系統時用 `TICKER_HANDLER.clear()`，它會影響其他訂閱。

## 藥草生長用 OnDemandHandler {#time-herb-on-demand}

新增 `game/typeclasses/timed_objects.py`：

```python
from evennia import ON_DEMAND_HANDLER
from typeclasses.objects import Object


class GrowingHerb(Object):
    def at_object_creation(self):
        super().at_object_creation()
        ON_DEMAND_HANDLER.add(
            self.dbref,
            category="herb-growth",
            stages={0: "seedling", 10: "sprout", 30: "mature"},
        )

    def get_display_desc(self, looker, **kwargs):
        stage = ON_DEMAND_HANDLER.get_stage(
            self.dbref, category="herb-growth"
        )
        descriptions = {
            "seedling": "一株剛種下的藥草幼苗。",
            "sprout": "藥草已長出嫩芽。",
            "mature": "藥草已經成熟，可以採收。",
        }
        return descriptions.get(stage, "這株藥草尚未登錄生長狀態。")

    def at_object_delete(self):
        allowed = super().at_object_delete()
        if allowed:
            ON_DEMAND_HANDLER.remove(self.dbref, category="herb-growth")
        return allowed
```

以穩定的 `dbref` 作 key，改名不會讓生長狀態失去對應。`get_display_desc()` 是預設 `look` 經由 `return_appearance()` 取得描述時呼叫的 hook；只新增任意命名的 `at_desc()` 不會讓它自動參與外觀顯示。

```text
create 藥草:typeclasses.timed_objects.GrowingHerb
look 藥草
```

建立時預設 `autostart=True`，開始計時。查看時才推算現在在哪個階段，不會每秒更新藥草。Evennia `6.1.0` 的查詢 API 是 **`get_stage()`**；不要照舊範例誤用 `get_state()`。

此版本的 `OnDemandTask.runtime()` 使用 `gametime.runtime()`，以伺服器累積運作秒數計算，停機時間不算入；也不是乘上 `TIME_FACTOR` 的遊戲日曆時間。若需要停機期間繼續生長，應改以現實時間戳計算，而非直接假定 handler 會補上停機時數。

關閉或 reload 時 handler 會保存狀態，再於啟動時讀回。這不等於每次 `.add()` 都立即提交資料庫，也不能保證程序異常終止前尚未保存的內容仍存在。不要在每次 `at_init()` 或查看時重新 `.add()`，否則會重設起點。

查詢可能直接跨到成熟階段，不會補執行每個中間階段。必須發獎勵、扣款或主動通知的事件，應另外安排且防止重複執行。

## 驗證與清理 {#time-validation}

先 reload 新增的模組，再用測試資料驗證以下行為：

| 系統 | 驗證重點 |
| ------ | ------ |
| 冷卻 | 開始後剩餘秒數為正；到期後為 0；reload 不會清掉期限 |
| delay | 等待時仍能操作；持久化 callback 可重新載入；取消後不再通知 |
| Script | `.db.ticks` 隨 callback 累加；stop 後不再累加但資料仍存在 |
| ticker | 相同訂閱不重複增加；stop_weather 可移除；另測正常 reload 與完整 stop/start |
| 藥草 | 初始顯示幼苗；經過 10／30 秒運作時間後顯示嫩芽／成熟；刪除物件會移除 task |

測藥草不必每次真的等待。以開發者帳號對測試物件設定已經過的時間，然後透過正常 `look` 檢查外觀：

```text
py from evennia import ON_DEMAND_HANDLER; herb = self.search("藥草"); ON_DEMAND_HANDLER.set_dt(herb.dbref, "herb-growth", 31)
look 藥草
```

`set_dt()` 是測試或玩法控制手段，設定本身不會立即觸發階段 callback，下一次查詢才重新判定。這些操作應在開發資料上執行。

## 參考資料 {#time-references}

- [Evennia Async Process](https://www.evennia.com/docs/latest/Concepts/Async-Process.html)
- [Evennia Scripts](https://www.evennia.com/docs/latest/Components/Scripts.html)
- [Evennia TickerHandler](https://www.evennia.com/docs/latest/Components/TickerHandler.html)
- [Evennia OnDemandHandler](https://www.evennia.com/docs/latest/Components/OnDemandHandler.html)
- [Evennia 6.1.0 OnDemandHandler 原始碼](https://github.com/evennia/evennia/blob/v6.1.0/evennia/scripts/ondemandhandler.py)
- [Evennia 6.1.0 gametime 原始碼](https://github.com/evennia/evennia/blob/v6.1.0/evennia/utils/gametime.py)
- [Evennia 中文指令解析與 CmdSet 實作](evennia-chinese-commands-cmdsets.md)
