# Nevergrind Online 職業系統總覽

Nevergrind Online 的職業系統可以先用「坦克、治療、物理輸出、魔法輸出、支援」五種角色來理解，但後期真正決定強度的是技能循環、天賦、裝備詞綴與隊伍 synergy。選職業時先選自己想承擔的隊伍責任，再慢慢把角色推向特定流派。

- 檢視日期：`2026-05-03`
- 本文整理來源：官方 Steam 頁、Nevergrind Wiki、Fandom 職業頁，以及 NotebookLM 摘要
- 版本提醒：職業名稱、技能與天賦可能因版本或 wiki 更新不同而有差異，實際名稱以遊戲內與官方 wiki 為準

<tldr>
<p>新手先用五大定位選職業：tank、healer、physical DPS、magical DPS、utility。</p>
<p>中後期不要只看職業標籤，要看 rotation、talents、armor / weapon access、haste、抗性與隊伍補位能力。</p>
<p>種族屬性有影響，但通常不是第一優先；先選你願意長期玩的外觀與職業節奏。</p>
</tldr>

## 名詞先對齊

目前公開資料有一個容易混淆的地方：Nevergrind Wiki 的 `Classes` 頁列出 14 個職業為 `Warrior`、`Monk`、`Rogue`、`Paladin`、`Shadow Knight`、`Ranger`、`Bard`、`Druid`、`Cleric`、`Shaman`、`Necromancer`、`Enchanter`、`Magician`、`Wizard`；Fandom 職業頁與部分 NotebookLM 摘要則使用 `Crusader`、`Warlock`、`Templar` 等名稱。

本文為了避免和官方 wiki、leaderboard 顯示名稱衝突，主文採官方 wiki 名稱；看到社群資料時，可以先這樣判讀：

| 社群 / Fandom 名稱 | 本文採用名稱 | 判讀方式 |
| ------ | ------ | ------ |
| `Crusader` | `Paladin` | 以防禦、暈眩、治療與對不死生物加成來理解 |
| `Warlock` | `Necromancer` 或 DoT 法系流派 | 以 DoT、恐懼、吸血、召喚與黑暗法術來判讀 |
| `Templar` | 需回遊戲內確認 | 若資料描述為魔法支援與治療，先不要直接套到官方 class list |

<note>
<p>如果你正在照 Fandom 或舊攻略配點，先確認遊戲內角色建立畫面、技能頁與排行榜顯示的職業名稱。名稱不一致時，優先對照技能組，而不是只看翻譯。</p>
</note>

## 中文職業與定位速查

下表以這次來源資料的英文名稱為主；如果和 Nevergrind Wiki 常見名稱不同，先用技能組與遊戲內顯示再確認一次。

| 中文名稱 | 來源英文名稱 | 角色定位 | 名稱備註 |
| ------ | ------ | ------ | ------ |
| 戰士 | `Warrior` | Tank | 官方 wiki 也使用此名稱 |
| 十字軍 | `Crusader` | Tank | 可先對照官方 wiki 的 `Paladin` 方向 |
| 暗影騎士 | `Shadow Knight` | Tank | 近戰與法術混合坦 |
| 牧師 | `Cleric` | Healer | 直接治療、防禦與板甲容錯 |
| 德魯伊 | `Druid` | Healer | HoT、自然法術與元素支援 |
| 薩滿 | `Shaman` | Healer | Debuff、DoT 與治療混合 |
| 武僧 | `Monk` | Physical DPS | Hand-to-hand / 鈍器近戰 |
| 遊俠 | `Ranger` | Physical DPS | 弓術與近戰混合 |
| 盜賊 | `Rogue` | Physical DPS | 攻速、背刺、毒素與爆發 |
| 巫師 | `Wizard` | Magical DPS | 元素法術輸出 |
| 術士 | `Warlock` | Magical DPS | 可先對照官方 wiki 的 `Necromancer` / DoT 法系方向 |
| 天騎士 | `Templar` | Magical DPS / Utility | 來源資料視為靈活法系支援；需回遊戲內確認對應技能組 |
| 吟遊詩人 | `Bard` | Utility | 歌曲、buff 與隊伍支援 |
| 恩路者 / 幻術師 | `Enchanter` | Utility | 控場、haste、緩速與魅惑 |

## 五大定位

Steam 頁面把職業大方向描述為 tank、healer、DPS 或 utility，而且也提醒這些定位不是硬限制。實務上可以先用五大定位建立概念：

| 定位 | 代表職業 | 核心責任 |
| ------ | ------ | ------ |
| Tank | `Warrior`、`Paladin` / `Crusader`、`Shadow Knight` | 建立 aggro、承受傷害、控制戰鬥節奏 |
| Healer | `Cleric`、`Druid`、`Shaman` | 抬血、穩定血線、補 buff / debuff 與救場 |
| Physical DPS | `Monk`、`Ranger`、`Rogue` | 透過武器、攻速、爆發或持續物理傷害處理目標 |
| Magical DPS | `Wizard`、`Necromancer` / `Warlock`、`Magician` / `Templar` | 用元素、DoT、召喚、範圍或控制法術輸出 |
| Utility | `Bard`、`Enchanter`，也包含部分 hybrid | 透過歌曲、haste、控制、魅惑、緩速與資源支援放大隊伍效益 |

這個分類適合新手理解「進隊伍後我要做什麼」，但不適合拿來判斷一個角色的上限。NGO 的後期玩法常常是混合的：治療職可以輸出，坦職可以打傷害，支援職可能是整隊 DPS 的真正來源。

定位可以再用這種方式快速抓：

- Tank：`Warrior` 物理防禦最直覺；`Crusader` / `Paladin`、`Shadow Knight` 則把近戰承傷和法術工具混在一起。
- Healer：`Cleric` 偏直接治療與板甲防禦，`Druid` 偏 HoT 和自然法術，`Shaman` 偏 debuff、DoT 與戰局穩定。
- Physical DPS：`Monk` 靠拳掌 / 鈍器節奏，`Ranger` 是弓術代表，`Rogue` 追攻速、背刺與毒素。
- Magical DPS：`Wizard` 偏元素爆發，`Warlock` / `Necromancer` 偏 DoT、恐懼或黑暗系玩法，`Templar` / `Magician` 類資料需按技能組確認。
- Utility：`Bard` 用歌曲強化全隊，`Enchanter` 用控場、haste、緩速與魅惑改變整場戰鬥節奏。

## 裝備適性與職業彈性

職業能穿的防具會影響容錯率，也會影響你在隊伍裡敢不敢站前排。來源資料採「階級機制」：能穿較高階防具的職業，也能穿其下位防具；例如 plate 職可以穿 mail、leather、cloth。來源資料也提到所有職業都可以裝備盾牌，但實戰上仍要看職業技能、武器需求與裝備詞綴是否支援目前流派。

| 防具階級 | 可用職業 | 包含下位防具 | 實戰意義 |
| ------ | ------ | ------ | ------ |
| Plate | `Warrior`、`Crusader` / `Paladin`、`Shadow Knight`、`Cleric`、`Bard` | Mail、Leather、Cloth | 高容錯，適合承傷、近戰支援或容易吃到傷害的位置 |
| Mail | `Ranger`、`Rogue`、`Shaman` | Leather、Cloth | 介於生存與輸出之間，適合物理或混合節奏 |
| Leather | `Druid`、`Monk`、`Templar`、`Wizard`、`Warlock` | Cloth | 靠技能、控制、輸出或機動性彌補防禦 |
| Cloth | `Enchanter` | Cloth | 控場與支援上限高，但更需要 aggro 管理與站位 |

## 職業裝備可用性速查

下表整理來源資料中的防具、武器與特殊規則。武器名稱以資料表常見英文 proficiency 對照中文，方便和 [Legendary Items 清單](nevergrind-online-legendary-items.md) 一起查。

| 職業 | 防具 | 武器 | 特殊規則 |
| ------ | ------ | ------ | ------ |
| `Warrior` | Cloth、Leather、Mail、Plate | `1h Slash`、`1h Blunt`、`1h Pierce`、`Archery`、`Hand-to-Hand`、`2h Slash`、`2h Blunt` | 等級 13 習得 dual wield；來源資料稱可同時持兩把兩手武器 |
| `Crusader` / `Paladin` | Cloth、Leather、Mail、Plate | `1h Slash`、`1h Blunt`、`Archery`、`Hand-to-Hand`、`2h Slash`、`2h Blunt` | 具備 dual wield，主要用於副手魔法武器 |
| `Shadow Knight` | Cloth、Leather、Mail、Plate | `1h Slash`、`1h Blunt`、`Archery`、`Hand-to-Hand`、`2h Slash`、`2h Blunt` | 等級 20 習得 dual wield，主要用於副手魔法武器 |
| `Cleric` | Cloth、Leather、Mail、Plate | `1h Blunt`、`2h Blunt`、`Hand-to-Hand` | 等級 20 習得 dual wield |
| `Bard` | Cloth、Leather、Mail、Plate | `1h Slash`、`1h Blunt`、`1h Pierce`、`Archery`、`Hand-to-Hand` | 等級 17 習得 dual wield |
| `Ranger` | Cloth、Leather、Mail | `1h Slash`、`1h Blunt`、`1h Pierce`、`Archery`、`Hand-to-Hand`、`2h Slash`、`2h Blunt` | 等級 17 習得 dual wield；來源資料稱是弓術強化代表職 |
| `Rogue` | Cloth、Leather、Mail | `1h Slash`、`1h Blunt`、`1h Pierce`、`Archery`、`Hand-to-Hand` | 具備 dual wield 與 double attack |
| `Shaman` | Cloth、Leather、Mail | `1h Blunt`、`1h Pierce`、`2h Blunt`、`Hand-to-Hand` | 具備 dual wield，主要用於副手魔法武器 |
| `Druid` | Cloth、Leather | `1h Slash`、`1h Blunt`、`2h Blunt`、`Hand-to-Hand` | 具備 dual wield，主要用於副手魔法武器 |
| `Monk` | Cloth、Leather | `1h Blunt`、`2h Blunt`、`Hand-to-Hand` | 無法使用弓箭；遠程欄位改用 charm；具備 dual wield 與 double attack |
| `Templar` | Cloth、Leather | `1h Blunt`、`1h Pierce`、`2h Blunt`、`Hand-to-Hand` | 具備 dual wield，主要用於副手魔法武器 |
| `Wizard` | Cloth、Leather | `1h Blunt`、`1h Pierce`、`2h Blunt`、`Hand-to-Hand` | 具備 dual wield，主要用於副手魔法武器 |
| `Warlock` | Cloth、Leather | `1h Blunt`、`1h Pierce`、`2h Blunt`、`Hand-to-Hand` | 具備 dual wield，主要用於副手魔法武器 |
| `Enchanter` | Cloth | `1h Blunt`、`1h Pierce`、`2h Blunt`、`Hand-to-Hand` | 具備 dual wield，主要用於副手魔法武器 |

<note>
<p>這張表以來源資料整理，且使用了部分 Fandom / NotebookLM 名稱。若角色建立畫面或官方 wiki 名稱不同，請先用技能組、可裝備 proficiency 與遊戲內 tooltip 對齊。</p>
</note>

來源資料對高階玩法的共同看法是：角色界線會變模糊。`Cleric` 不只是補師，能靠暈眩、buff、神聖傷害與對特定怪物的加成打輸出；`Warrior` 也不只是木樁坦，若武器與裝備成形，會同時承擔輸出與承傷。

## 團隊 synergy 怎麼看

NGO 的職業系統不是 14 個人在各打各的，而是看誰能把別人的優點放大。

常見協作方式：

- Tank 先建立 aggro，讓 healer 和 DPS 不要開場被秒。
- Healer 不只抬血，也要管理 spirit、威脅值與救場技能。
- `Enchanter` 的 haste、控制、緩速與魅惑可以大幅改變物理職與整隊節奏。
- `Bard` 的歌曲能補屬性、資源恢復、抗性與群體支援，常是隊伍穩定度來源。
- Hybrid 職業像 `Paladin`、`Shadow Knight`、`Ranger`、`Druid`、`Shaman`，會依裝備與天賦在不同隊伍裡補不同洞。

對新手來說，最重要的隊伍禮儀不是打最高傷害，而是知道自己什麼時候該等 tank、什麼時候該控場、什麼時候該停手。DPS 和 healer 如果在 tank 建立穩定 aggro 前過度施法，很容易把怪拉到自己身上。

## 種族與屬性怎麼選

NotebookLM 摘要提到種族會提供不同初始屬性與被動傾向，例如力量、耐性、抗恐懼或技能加成。這些差異會影響前期手感，但在長期角色培養中，通常不應壓過職業節奏與外觀喜好。

可以先用這個方向選：

- 物理輸出與坦克：優先看 `Strength`、`Stamina`、武器適性與生存。
- 治療與 wisdom 系：優先看 `Wisdom`、`Spirit`、資源與治療相關詞綴。
- 法系輸出與控制：優先看 `Intelligence`、施法速度、魔法傷害與資源續航。
- 支援職：看你的主技能吃哪個屬性，再補生存與資源。

如果你還沒打算衝高階排行榜，先選想看的角色外觀與想玩的戰鬥節奏。願意長期玩下去，比起前期多一點屬性更重要。

## 職業發展的三個層次

1. 技能等級
   - 在城鎮的 academy 學新技能或升級常用技能，讓核心 rotation 成形。
2. 天賦
   - 每個職業有不同 talent 方向，通常會把職業推向輸出、治療、控制、生存或支援。
3. 裝備詞綴
   - 後期 build 會被裝備重塑。技能加成、haste、抗性、資源、暴擊與特殊 unique / set 效果，常常比職業預設定位更關鍵。

所以「哪個職業最強」通常不是好問題。更實用的問法是：這個職業在我的隊伍裡補哪個洞？我的技能循環是否有足夠 haste、資源與保命？我的裝備是否真的服務於這個流派？

## 參考資料

- [Nevergrind Online on Steam](https://store.steampowered.com/app/853450/Nevergrind_Online/)
- [Nevergrind Wiki: Classes](https://nevergrind.com/wiki/index.php?title=Classes)
- [Nevergrind Wiki: Cleric](https://nevergrind.com/wiki/index.php?title=Cleric)
- [Nevergrind Wiki: Druid](https://nevergrind.com/wiki/index.php?title=Druid)
- [Nevergrind Wiki: Shaman](https://nevergrind.com/wiki/index.php?title=Shaman)
- [Nevergrind Online Wiki: Classes](https://nevergrind-online.fandom.com/wiki/Classes)
