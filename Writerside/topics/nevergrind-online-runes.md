# Nevergrind Online 符文 Runes 指南

`Runes` 是 Nevergrind Online 後期裝備客製化的核心：有 sockets 的裝備可以透過 Blacksmith 的 enchanting / crafting 相關功能加入 rune bonus，把「好裝」推成更明確服務於 build 的核心裝。鑲嵌前先想清楚這件裝備會穿多久，因為符文通常不是拿來補一件很快會被換掉的過渡裝。

- 檢視日期：`2026-05-03`
- 前置閱讀：[Nevergrind Online 物品與戰利品總覽](nevergrind-online-items-loot.md)
- 資料來源：NotebookLM 摘要、SteamDB patch notes、Nevergrind Online 日文 wiki rune list
- 版本提醒：符文效果、可鑲嵌部位、是否可取下、是否可升級，可能會隨 crafting 系統更新；點確認前請以目前遊戲內 UI 和 tooltip 為準

<tldr>
<p>物理職通常先看武器基礎傷害、攻速、命中與 <code>Cros</code> / <code>Rath</code> 類傷害收益。</p>
<p>魔法職通常先看 enemy resistance reduction、casting haste、crit、元素傷害與資源續航，不要只堆智慧或智力。</p>
<p>防具符文多半是補短板：抗性、生存、magic find 或缺少的資源循環。</p>
</tldr>

## 基本規則

SteamDB 的 2024 Season 2 patch note 提到 Blacksmith 的 enchanting counter 已啟用，可以用 runes 強化 socketed items；2025 patch note 又提到 crafting counter 加入 rune upgrade。這代表 rune 系統已經從單純鑲嵌，逐漸變成 crafting 後期的一部分。

操作前先確認：

- 這件裝備是否有 sockets。
- 該 rune 是否能放進這個部位，例如 1h、2h、armor 或 charm。
- 鑲嵌是否不可逆，或目前版本是否有取下 / 覆蓋 / 升級機制。
- 裝備是否值得長期穿到你投入高階 rune。
- 這個 rune 是補 build 核心，還是只是看起來數字漂亮。

<warning>
<p>NotebookLM 摘要把 rune 鑲嵌視為永久且不可逆；但 2025 patch note 已提到 rune upgrade via crafting。實務上請先把高階 rune 當成不可輕易反悔的資源，並在遊戲內確認目前 crafting counter 的實際規則。</p>
</warning>

## 符文名稱與資料來源

日文 wiki 目前列出一批 rune 名稱與等級，例如 `Gra`、`Gart`、`Ruck`、`Nag`、`Rok`、`Skar`、`Targ`、`Tae`、`Rath`、`Marr`、`Cros`、`Mael` 等。NotebookLM 摘要則進一步整理了這些符文在不同職業與部位上的使用方向。

本文把它們當成 build 策略筆記，不把每個 rune 的數值寫死。真正要鑲嵌前，仍要看當前 tooltip。

## 物理職武器

物理職的 rune 選擇，先看武器基礎與角色問題在哪裡。

| 情境 | 優先方向 | 判斷 |
| ------ | ------ | ------ |
| 單手武器 | `Cros` 武器傷害、`Targ` 全被動、`Gart` strength | 單手基礎傷害較低，直接補 weapon damage 往往很有感 |
| 兩手武器 | `Rath` 攻擊能力 / 攻擊相關百分比 | 兩手基礎傷害高，放大命中與爆發通常更划算 |
| 弓 | `Cros` 武器傷害或 `Rok` weapon speed | 依武器速度、socket 數與職業技能判斷 |
| 命中不足 | `Rath` / `Shir` 類攻擊能力 | 打不中時，帳面傷害再高也沒有意義 |
| 資源斷循環 | `Gra` hit 時 mana 回復 | 適合高攻速、頻繁命中的 build |

NotebookLM 摘要提到 `Demetrium's Ballista` 因為 sockets 多，即使是較低等級套裝弓，也可能因 rune space 而保有後期價值。這個觀念比單一裝名更重要：有時候 sockets 數量會改寫裝備上限。

## 魔法職與支援職武器

魔法職不要只看 `Wisdom` / `Intelligence` 這類 stat rune。NotebookLM 摘要認為 `Ruck`、`Nag` 這類純屬性 rune 對 caster 火力提升偏弱，因為真正的瓶頸常常在 resistance reduction、cast speed、crit、技能加成與資源。

| 需求 | 優先方向 | 適用情境 |
| ------ | ------ | ------ |
| 打高抗性怪 | `Mael` enemy resistance reduction | 高難度與 boss farm 很重要 |
| 提高爆發 | `Tae` crit 或屬性傷害 rune | 已有足夠命中 / sustain 時再追 |
| 缺 casting haste | `Skar` casting speed | 沒有 Templar / Enchanter / Bard 支援時更有感 |
| 想刷寶 | `Marr` rare drop / magic find 類 | 防具或低風險 farm 裝可考慮 |
| 魔力不足 | `Gra` 或資源回復詞綴 | 對高頻率施法或混合攻擊 build 有價值 |

對 Cleric、Druid、Shaman 這類 healer / hybrid 來說，rune 不只是輸出。你可能需要在 healing uptime、resist、casting speed、spirit / mana sustain 與 magic find 之間取捨。

## 防具符文

防具 rune 的角色比較像補洞。你可以把它分成三種用途：

1. 補生存
   - 抗性、armor、生命、全屬性、防禦。
2. 補效率
   - magic find、gold find、移動速度或資源回復。
3. 補 build breakpoint
   - all talents、all passive、技能加成、casting haste。

NotebookLM 摘要提到，物理防具用 `Rath` 類全 stat / strength 方向可能很奢侈；如果角色抗性很破，先補抗性比追輸出更合理。魔法防具在沒有明確缺口時，`Marr` 類刷寶符文是常見選擇。

## 依隊伍配置調整

符文不是單機計算器，它會受到隊伍影響。

- 有 `Bard` 回魔、haste、資源歌曲時，可以少補一些 sustain。
- 有 `Enchanter` 或法系支援時，casting haste 壓力可能降低。
- 沒有穩定支援時，`Gra`、`Skar`、資源與抗性 rune 的價值上升。
- 物理隊伍缺命中時，攻擊能力 rune 可能比更多傷害更有用。
- 高難度 boss farm 中，抗性與資源斷點通常比多一點 magic find 更重要。

## 鑲嵌前檢查表

鑲嵌高價 rune 前，先問自己：

1. 這件裝備會穿多久？
2. 這件裝備的 sockets 數是否值得投入？
3. 這個 rune 是補核心問題，還是只增加漂亮數字？
4. 我的 build 是單刷、組隊、刷寶，還是 boss farm？
5. 有沒有隊友 buff 會讓某個 rune 的收益下降？
6. 目前版本是否允許 rune upgrade、覆蓋或取回？
7. 如果明天拿到更好的 unique / set，這顆 rune 會不會心痛？

好的 rune 策略不是把最貴的東西塞上去，而是把裝備最後一段缺口補到剛好。物理職追基礎與命中質變，魔法職追 resistance reduction 與施法節奏，防具則負責讓角色不被難度反咬。

## 參考資料

- [SteamDB: Enchanting With Runes Enabled](https://steamdb.info/patchnotes/16172899/)
- [SteamDB: Added ability to upgrade runes via crafting](https://steamdb.info/patchnotes/18527675/)
- [Nevergrind Online 日本語 Wiki: ルーン](https://wikiwiki.jp/ngowiki/%E3%83%AB%E3%83%BC%E3%83%B3)
- [Nevergrind Wiki: Magic Find Mechanics](https://nevergrind.com/wiki/index.php?title=Magic_Find_Mechanics)
- [Nevergrind Online Wiki: Loot](https://nevergrind-online.fandom.com/wiki/Loot)
