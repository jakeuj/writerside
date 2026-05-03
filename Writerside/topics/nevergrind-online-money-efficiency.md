# Nevergrind Online 金錢效率與賣裝策略

Nevergrind Online 的 gold 不是單純的商店貨幣，而是技能升級、背包擴張、補給鑑定、item upgrades、gambling 與 crafting 的共同燃料。金錢效率的核心不是「把每件裝備都撿回來」，而是在有限背包裡優先帶回高價值部位，透過鑑定提高售價，再把 gold 投入最能提升下一趟地城效率的地方。

- 檢視日期：`2026-05-03`
- 分類：[Nevergrind Online 物品與戰利品總覽](nevergrind-online-items-loot.md)
- 延伸閱讀：[裝備收集路線](nevergrind-online-equipment-collection.md)、[Identification 鑑定指南](nevergrind-online-identification.md)、[Merchant 商店指南](nevergrind-online-merchant.md)、[Gambling 賭博指南](nevergrind-online-gambling.md)
- 資料來源：NotebookLM 摘要、既有 Nevergrind 筆記、Fandom General Game Mechanics / Races、Nevergrind Wiki Item Upgrades 與相關來源整理
- 版本提醒：物品售價、背包上限、gold bonus、`/players` 類指令、商店刷新與 gambling 池可能隨版本調整；實際操作請以目前遊戲內 UI、tooltip、`/help` 與 vendor price 為準

<tldr>
<p>背包有限時，優先帶回 focus / stave、plate、chest、shield、head、high-level weapon base 這類高價候選。</p>
<p>鑑定不只是看能不能穿，也會讓 talents、高 resistance 或高價 mods 轉成更好的 vendor value。</p>
<p>Gold 先投技能、背包、補給與穩定地城；有餘裕後再進 gambling、runes、crafting 與終局投資。</p>
</tldr>

## Gold 花在哪裡 {#gold-spending-priorities}

金錢效率要從支出端倒推。你賺 gold 的目的不是把數字堆高，而是讓下一場更穩、更快，或讓裝備追求更有方向。

| 支出 | 優先度 | 判斷 |
| ------ | ------ | ------ |
| 技能學習 / 升級 | 很高 | 核心 rotation 還沒成形前，通常比 gambling 更重要 |
| 補給與鑑定 | 很高 | 沒藥水、沒卷軸、不能整理掉落，地城效率會下降 |
| 背包擴張 | 很高 | 背包太小會直接損失掉落與補給空間 |
| Item upgrades | 中高 | 對會穿一段時間的裝備才值得投入 |
| 商店巡視 | 中 | 可補過渡裝、socketed base 或高價底材 |
| Runes / crafting | 中後期 | 高成本且常不可逆，先確認裝備或 base 夠好 |
| Gambling | 後期 | gold overflow 後，把多餘金幣換成定向抽裝機會 |

## 背包滿時先撿什麼

來源摘要把高價值帶回順序整理得很實用：優先看法系鈍器、胴體、重裝與高價部位。實際售價仍以 vendor UI 為準，但地城中背包快滿時可以先照這個方向篩。

| 優先級 | 類型 | 為什麼值得帶回 |
| ------ | ------ | ------ |
| 1 | `Focus` / `Stave` / magic blunt | 容易帶 talents、caster mods 或資源詞綴；鑑定後可能自用或高價出售 |
| 2 | Chest / 胴體 | 部位價值高，也常影響 armor、resistance 與 survivability |
| 3 | Plate / mail 重裝 | 原始售價通常較高，plate 類尤其值得多看一眼 |
| 4 | Shield、head、gloves、legs、boots | 高價部位、抗性、talents 或防禦 roll 可能讓售價提高 |
| 5 | High-level 2H weapon / weapon base | 高 DPS 或高等底材可能有穩定售價或 crafting 價值 |
| 6 | 低等 cloth / leather、小部位、詞綴不合的低價件 | 背包滿時通常先丟，除非有好 roll、set / unique 或特殊用途 |

<note>
<p>來源摘要提到稀有兩手物理武器若 DPS 超過某個門檻，售價會變得穩定且高昂。這類數字很吃版本與 item level，筆記中保留「高 DPS 兩手武器值得看」這個原則，不把特定門檻寫成永久規則。</p>
</note>

## 鑑定如何提高收益

鑑定是 gold farming 的放大器。未鑑定裝備只是一個可能性；鑑定後若出現 talents、高 resistance、核心技能、資源或其他高價 mods，vendor value 與自用 / 交易價值都可能提高。

| 做法 | 適合時機 | 收益 |
| ------ | ------ | ------ |
| 地城中用 `Identify Scrolls` | 背包快滿，但不確定某件高價候選值不值得帶回 | 立刻淘汰低價裝，保留高價或自用候選 |
| 回城用 `Identify All` | 一整包未鑑定裝備 | 快速揭示 mods，再分成自用、銀行、出售 |
| 優先鑑定高價部位 | focus / stave、plate、chest、shield、head、high-level base | 最有機會把鑑定成本轉成額外售價 |
| 留意 talents / res | 裝備看似不適合目前角色時 | 可能給分身、交易或高價出售 |

完整操作可看 [Identification 鑑定指南](nevergrind-online-identification.md) 與 [Apothecary 藥劑店指南](nevergrind-online-apothecary.md)。

## 難度、隊伍與金幣倍率

Fandom mechanics 資料提到隊伍越大，風險、magic find、經驗與 gold 期待也會提高；來源摘要也把 `Heroic` 視為更高風險但更高收益的難度。

| 做法 | 好處 | 風險 |
| ------ | ------ | ------ |
| 組隊 farm | 提高收益期待，也能讓職業分工更完整 | 需要協調 aggro、補給、控制與 loot 節奏 |
| Heroic | 更多壓力換更高 reward 期待 | 裝備、抗性、資源或隊伍不穩時會降低效率 |
| 首通 / boss route | 首通與 boss 本身通常值得打 | 若花太久或翻車，金錢效率會下降 |
| 任務掉落偏好 | 更容易把時間投入到目標部位 | 需要先在 Tavern 確認任務資訊 |

<warning>
<p>來源摘要提到 solo 玩家可用 <code>/players 5</code> 模擬滿隊難度與收益。這類指令是否存在或是否影響 gold，請以目前遊戲內 <code>/help</code>、Tavern tips 與官方說明為準；沒有確認前，不要把它當成固定金幣策略。</p>
</warning>

## 種族與長期經營

來源摘要提到 `Anukari` 有 gold gain 方向優勢。Fandom Races 頁的敘述也說 Anukari 具有比其他種族更容易發現額外 gold 的能力，但同頁的 race bonus 表並未把這點穩定列成明確百分比。因此比較安全的寫法是：若你要為 gold efficiency min-max，先回遊戲內 race tooltip 確認是否仍有 gold bonus，以及具體數值。

| 策略 | 什麼時候值得 |
| ------ | ------ |
| 選擇具 gold bonus 的種族 | 你確定要長期用該角色 farming，且目前 tooltip 明確顯示 gold bonus |
| 高等角色 farm，分身使用 | 共享銀行讓高等角色能把裝備、套裝、抗性裝或高價物留給 alts |
| 分身賣裝或穿裝 | 若版本與交易 / 銀行規則允許，可以把不適合本尊的裝備轉成分身資源 |
| 銀行分類 | 把「自用」、「出售」、「分身」、「交易」、「craft base」分開，避免高價品被誤賣 |

## Gold 的後期流向 {#gold-endgame-sinks}

當技能、背包、補給與基本裝備都穩定後，gold 才適合大量流向高風險系統：

| 系統 | 投入時機 | 注意 |
| ------ | ------ | ------ |
| [Gambling](nevergrind-online-gambling.md) | 已知道要追 elite 飾品、Haniwa、Shako 或特定部位 | 高風險，先確認 quality 與圖示 |
| [Runes](nevergrind-online-runes.md) | 裝備會穿很久，或高 socket 工具裝已確定用途 | 一般鑲嵌通常視為不可逆 |
| [Crafting](nevergrind-online-blacksmith-crafting-recipe-research.md) | 已有正確 socketed base、runes 與 recipe 方向 | base、socket count、required level 都要符合 |
| Item upgrades | 裝備不會很快被替換 | Nevergrind Wiki 描述升級可穩定補強，但成本會增加 |

來源摘要特別看重 Exceptional / Elite 的 ring、amulet、charm gambling，因為這些部位可能更容易導向 unique 以上候選。這條策略很有價值，但仍應放在版本檢查後使用：投入前先 hover quality，看目前 Merchant UI 是否支援你想追的池。

## 每趟地城的金錢流程

1. 出發前空出背包，帶足藥水與 `Identify Scrolls`。
2. 地城中優先撿高稀有度、高價部位、高等 base、socketed item 與當前缺口部位。
3. 背包快滿時，鑑定最有機會升級或最高價的候選。
4. 回城後到 Apothecary 使用 `Identify All`。
5. 自用、分身、交易、craft base 先放銀行或固定背包區。
6. 高價但不自用的裝備賣掉，低價低用途裝備快速清掉。
7. Gold 先回填技能、背包、補給；剩餘再投入 gambling、runes、crafting。

## 參考資料

- [裝備收集路線](nevergrind-online-equipment-collection.md)
- [Identification 鑑定指南](nevergrind-online-identification.md)
- [Merchant 商店指南](nevergrind-online-merchant.md)
- [Gambling 賭博指南](nevergrind-online-gambling.md)
- [Nevergrind Online Wiki: General Game Mechanics](https://nevergrind-online.fandom.com/wiki/General_Game_Mechanics)
- [Nevergrind Online Wiki: Races](https://nevergrind-online.fandom.com/wiki/Races)
- [Nevergrind Wiki: Item Upgrades](https://nevergrind.com/wiki/index.php?title=Item_Upgrades)
