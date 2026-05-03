# Nevergrind Online Legendary Items 清單筆記

這份 Legendary Items 筆記把玩家整理的試算表當成查裝索引：先用 `Quality`、`Slot`、`Proficiency`、`Level` 篩出角色真的能穿的裝備，再看 `All Talents`、`Tree Talents`、`Specific Talent`、`Specific Skill %` 與核心攻防詞綴。資料表目前整理 65 件 legendary，分成 Normal / Exceptional / Elite 三段；實際數值與掉落狀態仍以遊戲內 tooltip 為準。

- 檢視日期：`2026-05-03`
- 分類：[Nevergrind Online 物品與戰利品總覽](nevergrind-online-items-loot.md)
- 資料來源：玩家整理的 Legendary Items 試算表
- 版本提醒：試算表、公開 wiki 與遊戲內版本可能不同步；交易、鑲嵌高價 rune 或判斷 BiS 前，請先回遊戲內 tooltip 核對

<tldr>
<p>這份表比較適合拿來做「候選裝備索引」，不是直接照表宣告 BiS。</p>
<p>目前讀到 65 筆 item：Normal 22 件、Exceptional 21 件、Elite 22 件，等級從 9 到 75。</p>
<p>表格中的部分 roll range 可能被試算表自動格式化影響；看到可疑數字時，優先用圖片或遊戲 tooltip 確認。</p>
</tldr>

## 試算表結構

這份 workbook 主要有四個 sheet：

| Sheet | 用途 | 筆記 |
| ------ | ------ | ------ |
| `Main Table` | Legendary item 主資料 | 65 筆有效 item，欄位一路展開到 `Stat 23` |
| `Images 1` / `Images 2` | 範例圖片 | 用來核對 tooltip、圖示與數值 |
| `Affixes` | 詞綴名稱整理 | 讀到 141 個 sorted affix 名稱 |

`Main Table` 前段欄位可以先分成幾組看：

| 欄位 | 怎麼用 |
| ------ | ------ |
| `Name`、`Base` | 先確認物品名稱與底材 |
| `Slot`、`Proficiency` | 判斷角色能不能穿、是不是符合武器 / 防具 proficiency |
| `Quality`、`Level` | 判斷裝備階段，Normal / Exceptional / Elite 大致對應前期、中期、後期 |
| `Armor`、`Block`、`Base Damage`、`Base Attack Speed`、`DPS` | 看基礎防禦、格擋或武器輸出底線 |
| `Class Talents`、`All Talents`、`Tree Talents`、`Specific Talent` | 看天賦加成是否真的命中 build |
| `Skill 1 %` 到 `Skill 4 %` | 看特定技能加成與 proc / chance 類線索 |
| `Stat 1` 到 `Stat 23` | 逐條看固定詞綴與隨機詞綴方向 |

<note>
<p>像 <code>1-3</code>、<code>2-4</code> 這種 roll range 在試算表工具裡很容易被當成日期或序號。整理 build 時，不要只複製匯入後的數字；要回原始 tooltip 圖片或遊戲內文字確認。</p>
</note>

## 品質與等級分佈

| Quality | 件數 | 等級範圍 | 判斷方式 |
| ------ | --: | ------ | ------ |
| `Normal` | 22 | 9-35 | 前期成形、補關鍵抗性或技能方向，不一定值得重資源強化 |
| `Exceptional` | 21 | 38-55 | 中期 build 開始定型，可以留意能不能接到後期路線 |
| `Elite` | 22 | 59-75 | 後期候選裝，才比較值得認真比較 roll、socket 與 rune plan |

部位覆蓋很平均，大多數 slot 都有 3 件跨階段 item；`2h Blunt`、`Chest`、`Magic Offhand` 各有 4 件，`2h Staff` 有 2 件。這代表查表時最好先用 slot 篩選，不要只從整份清單硬找名字。

## 快速索引

### Normal

`Death Wish`、`Carpathian Mallet`、`Olivia's Chain of Fealty`、`Goremaggon's Bracer`、`Gaia's Wrath`、`Dyne's Golden Girdle`、`Painbearer's Tome`、`Destructor's Punishment`、`Kingdom's Reckoning`、`Pendleton's Exquisite Knickers`、`Charlemagne's Eminence`、`O'Donnell's Frostweaver`、`Pallbearers's Tome`、`Rasoir Brûlant`、`Icy Punisher`、`Falkland's Refuge`、`McQuaid's Heraldry`、`Crepesculan Lavalier`、`Mercator's Globetrotters`、`Zamza's Glaive`、`Naiko's Cinder`、`Fippy's Shoulder Spikes`

### Exceptional

`Quantum Harmony Crystal`、`Volga's Aurora Robe`、`Fist of the Titan`、`Ameno Ohabari`、`Zebulon's Bloodbath`、`Astrakhan's Griffon Veil`、`Hydrafury Whorl`、`Kylorean Frostshard Bracers`、`Boneclasp`、`Scaled Hierophant Leggings`、`Dhampyre's Lurid Shawl`、`Umkhulu Inkemba`、`Pendant of King Chigowitz`、`Mobius Buster`、`Sinister Bone Sabatons`、`Caitlin's Hawkstrike Bow`、`Victor's Chains of Carthage`、`Goliath's Pendulum`、`Witherstorm`、`Xeronarth's Token`、`Karakum's Orchid`

### Elite

`Firmament Staff of the Crystal Sea`、`Gloom Harvester`、`Saladin's Makhalib`、`Prodigal Thunderguards`、`Starlight Atmos`、`Treewind's Earthcaller`、`McMurdo's Twig`、`Himmelsdolch`、`Agathor's Wurmslaying Boots`、`Reito Doku`、`Damachi's Halycon Cloak`、`Grove Warder's Greaves`、`Ginjirou's Emerald Sash`、`Fuvu Kifo`、`Argent Dread Wristguards`、`Lunatic's Seal`、`Mosby's Ancient Crown`、`Honored Chains of Mallorca`、`Monark's Abstruse Relic`、`Stone of Miracles`、`Bettencourt's Imbued Pauldron's`、`Beads of Chilaga`

## 怎麼判斷一件 Legendary

查到一件 legendary 後，建議照這個順序看：

1. `Level` 是否接近目前角色，避免為了名字硬穿低階裝。
2. `Slot` 和 `Proficiency` 是否符合職業，尤其是 weapon、shield、armor type。
3. 基礎值是否過關：武器看 damage / attack speed / DPS，防具看 armor / block。
4. 天賦線是否命中 build：`All Talents`、`Tree Talents`、`Specific Talent`、`Class Talents`。
5. 技能線是否真的有用，不要被高百分比但錯技能的 roll 迷惑。
6. 生存線是否補到高難度門檻：`All Res %`、`Res Physical %`、`All Status Res %`、health / mana / spirit。
7. 輸出線是否和流派一致：物理、元素、spell power、enemy resistance reduction、attack speed 或 cast rate。
8. 是否值得投入 [符文](nevergrind-online-runes.md)：普通過渡裝先不要塞高價 rune。

## 值得優先看的詞綴

| 類型 | 詞綴例子 | 看法 |
| ------ | ------ | ------ |
| 天賦與技能 | `All Talents`、`Tree Talents`、`Specific Talent`、`Specific Skill %` | 後期價值很高，但要命中核心技能才算真正有效 |
| 施法與輸出節奏 | `Faster Cast Rate`、`Increased Attack Speed %`、`Double Attack` | 會直接影響 rotation 手感與輸出窗口 |
| 物理與元素傷害 | `Enhanced Damage %`、`All Spell Damage %`、`Fire Damage %`、`Arcane Damage to Melee (Flat)` | 先確認你的 build 是 spell、melee、hybrid，避免混錯方向 |
| 破抗與抗性 | `Reduce Enemy Res Fire %`、`All Res %`、`Res Physical %`、`All Status Res %` | Hell 或高難度常比單純面板更重要 |
| 資源與續戰 | `Health Leech`、`Mana Leech`、`Mana Regen`、`Spirit Regen` | 長時間 farm 與 boss 戰會放大這些詞綴的價值 |
| 刷寶 | `Magic Find %`、`Gold Find %`、`Exp Find %` | 有餘裕再堆，不能壓垮輸出與生存 |
| 特殊效果 | `Effect: Earthcaller`、`Effect: Bloodbath`、`Effect: Mobius Crash` 等 | 通常是 legendary 最值得回 tooltip 確認的部分 |

## 和既有裝備筆記怎麼接

這份清單是「找名字與篩候選」用；真正做裝備決策時，還是要回到整體角色路線：

- 先用 [物品與戰利品總覽](nevergrind-online-items-loot.md) 判斷 magic find、商店、升級與掉落邏輯。
- 如果這件裝備有 socket 或會穿很久，再看 [符文 Runes 指南](nevergrind-online-runes.md)。
- Caster / support 類高階武器可以參考 [Cryptic Paragon（Haniwa）](nevergrind-online-cryptic-paragon-haniwa.md) 的判斷方式：名字重要，但 roll、技能、天賦與 build 契合度更重要。

## 常見誤區

- 看到 `Elite` 就直接當 BiS，忽略職業 proficiency 與技能 roll。
- 只看 `Magic Find %`，把生存和輸出壓到無法穩定 farm。
- 把 roll range 的匯入值當成絕對數字，沒有回 tooltip 確認。
- 為了穿 legendary 犧牲抗性、資源或核心技能 breakpoint。
- 低等 legendary 明明只是過渡裝，卻投入太多升級與高階 rune。
