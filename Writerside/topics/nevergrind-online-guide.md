# Nevergrind Online（絕不刷怪）遊戲指南

Nevergrind Online 可以先當成「短場次、重刷寶、重組隊協作」的第一人稱地城 RPG 來玩：先選一個你喜歡的職業定位，把技能等級和背包空間補上，反覆接任務、進隨機地城、打王、鑑定裝備，再用掉落、商店、交易與升級系統慢慢把角色推向流派成形。

- 檢視日期：`2026-05-03`
- 適用對象：剛入坑 NGO、想理解職業分工與刷寶邏輯，或想把新手操作整理成一份可重讀筆記的玩家
- 版本提醒：MMORPG 的技能、物品、掉落與指令可能會隨更新調整；具體數值請以遊戲內說明、官方 Steam 頁與 wiki 當下資料為準

<tldr>
<p>新手最短路徑是先理解核心循環：回城補給與升技能，進地城完成任務，打王拿掉落，回城鑑定、出售、升級或保留裝備。</p>
<p>職業不要只看坦、補、輸出、支援的固定標籤；NGO 的後期價值常來自技能循環、裝備詞綴、攻速與隊伍 synergy。</p>
<p>刷寶時不要只追稀有度顏色。正確詞綴、可用部位、技能加成、haste、抗性與資源恢復，常比單純高稀有度更重要。</p>
</tldr>

## 這款遊戲在玩什麼

Nevergrind Online 是一款即時戰鬥的多人第一人稱地城爬行 RPG。官方 Steam 頁面把它定位成可以單人遊玩，也可以最多 5 人組隊的 treasure hunting / dungeon crawl RPG；角色建立時有 14 個種族與 14 個職業，每個職業有 12 個獨特技能。

它的節奏比較像把老派 MMORPG 的職業分工、聊天社交、隊伍推進，濃縮進一場一場短地城。想先看整體系統地圖，可以從 [Nevergrind Online 遊戲核心架構心智圖](nevergrind-online-core-structure.md) 開始，再回來讀各主題細節。

1. 在城鎮接任務、補藥水、買卷軸、升級技能、管理銀行與背包。
2. 進入隨機生成的地城，由隊長帶路，隊伍沿路處理怪群。
3. 找到任務目標或 boss，控制威脅值、資源與技能冷卻，把戰鬥收掉。
4. 撿掉落、回城鑑定、出售、保留、交易或升級裝備。

如果只想休閒玩，NGO 的單場戰鬥通常很短；如果想鑽研，它又會把職業循環、裝備詞綴、haste、抗性、資源恢復與隊伍配合全部疊在一起。好上手，但真的要玩深也很深。

## 職業定位怎麼看

NGO 的職業可以先用五大定位入門，但不要太早把角色鎖死在單一標籤。官方頁面也提到職業大致設計成 tank、healer、DPS 或 utility，不過定位不是硬性限制。更完整的分類、名詞差異與職業協作整理在 [Nevergrind Online 職業系統總覽](nevergrind-online-classes.md)。

| 定位 | 常見職業方向 | 新手判斷 |
| ------ | ------ | ------ |
| 坦克 | Warrior、Paladin、Shadow Knight | 先學會開場建立 aggro，讓輸出與治療不要被怪轉頭 |
| 治療 | Cleric、Druid、Shaman | 除了補血，也要看資源恢復、仇恨與隊友承傷節奏 |
| 物理輸出 | Monk、Rogue、Ranger、Warrior | 重點是武器、攻速、技能冷卻與目標選擇 |
| 魔法輸出 | Wizard、Magician、Necromancer，也包含部分 Cleric / Druid 流派 | 重點是施法速度、魔法傷害、控制與資源續航 |
| 支援 / 控制 | Bard、Enchanter、Shaman | 不一定是傷害最高，但常能讓整隊輸出或生存質變 |

入門時可以先問自己三件事：

- 你想負責節奏：選 tank 或 utility。
- 你想救場與穩定隊伍：選 healer 或 hybrid healer。
- 你想追傷害與刷寶效率：選 DPS，但要學會等坦克抓穩仇恨。

後期更像是在玩「流派」而不是「純職」。同一個 Cleric 可能偏治療，也可能靠不死系目標、神聖傷害或特定控制條件打出高輸出；Warrior 也不只是坦，若裝備與武器配置到位，可能成為非常強的物理核心。判斷角色強不強，最終要回到技能循環與裝備詞綴，而不是只看職業名稱。

## 戰鬥與隊伍配合

NGO 的戰鬥不是站樁按亮的技能而已。新手最容易出事的點通常是 aggro、資源、目標位置與技能優先順序。

### Aggro 是第一個要學的團隊語言

在組隊地城裡，坦克還沒建立威脅值之前，輸出職搶開爆發，或治療太早大量補血，都可能讓怪物轉向脆皮角色。社群指南也特別提醒，治療與施法本身就可能快速累積威脅，所以進高難度地城時先讓坦克開場，是很實際的生存技巧。

簡單抓法：

1. 坦克先碰怪，建立初始 aggro。
2. 控制或 debuff 接上，降低怪物壓力。
3. 輸出再進入主要循環。
4. 治療看血線與資源，不要把每次小傷都立刻補成大仇恨。

### 技能循環先排優先順序

不要只看單一技能傷害。比較穩的方式是把技能分成：

- 開場技能：建立威脅、上 debuff、召喚、控制或鋪增傷條件。
- 核心輸出：冷卻短、收益穩定、可以反覆使用的主技能。
- 爆發技能：等 boss、精英怪、暈眩目標或隊伍 buff 開窗時使用。
- 保命技能：不要用來補傷害，留給轉火、失控或補師資源低的時候。

有些職業需要配合特定狀態，例如暈眩、流血、召喚物、combo / technique point、目標排位或不死系標籤。高階攻略之所以常討論 rotation，本質上就是在找「哪個條件先成立，後面的技能才值得按」。

### 位置與攻擊範圍會影響輸出

地城戰鬥裡有前排、後排與不同範圍類型。Fandom 的 mechanics 筆記提到，後排怪物受到物理攻擊時通常會減傷，因此物理職要注意技能是否能打到後排，法系與範圍技能也要看目標型態。

常見判斷：

- 物理職不要只盯著最高傷害技能，先確認它能不能有效打到當前目標。
- AoE 技能要看範圍是前排、後排、cone，還是多目標隨機。
- 控制技能優先交給會威脅隊伍節奏的怪，而不是無腦丟在第一個目標。

## 裝備與刷寶哲學

NGO 的長期樂趣很大一部分來自「每次掉落都有機會翻出好東西」。Steam 頁面提到 magical、rare、set、unique 物品，且 magical、rare、unique 具有動態屬性；Fandom mechanics 目前也把常見掉落整理成藍、黃、紫、綠四類。更完整的稀有度、magic find、商店、鑑定與符文強化整理在 [Nevergrind Online 物品與戰利品總覽](nevergrind-online-items-loot.md)。

| 顏色 / 類型 | 大致意義 | 觀察重點 |
| ------ | ------ | ------ |
| 藍色 Magic | 少量隨機詞綴 | 前期很常換裝，不要太早投入太多資源 |
| 黃色 Rare | 多個隨機詞綴 | 好詞綴組合時可能比固定裝更適合當前流派 |
| 紫色 Unique | 固定詞綴類型，但數值可能浮動 | 適合追特定技能、部位或 build 核心 |
| 綠色 Set | 套裝，穿多件會啟用套裝效果 | 要看套裝 bonus 是否真的支援你的循環；可接著看 [套裝 Set Items 指南](nevergrind-online-set-items.md) |

<note>
<p>有些玩家整理或舊攻略會提到橘色、傳奇、BiS 名單或特定神裝。若你的遊戲版本已加入新的稀有度或新裝備階層，請以遊戲內 tooltip 與目前 wiki 為準；公開頁面的分類可能落後於遊戲更新。</p>
</note>

刷寶時可以照這個順序看：

1. 這件裝備的部位是不是你目前最缺的洞。
2. 詞綴是否支援你的主要技能、傷害型態、haste、命中、暴擊或資源。
3. 抗性、生命、護甲與減傷是否補上你會暴斃的原因。
4. 如果是 unique / set，固定效果是否能改變技能循環，而不只是帳面數字高。
5. 如果是社群常提的 BiS，例如 `Cryptic Paragon`、`Charlatan's Crest` 這類名字，先查當前版本資料與掉落來源，再決定要不要專門 farm。

## 金幣、升級與資源管理

金幣不是只拿來買藥水。城鎮裡的裝備升級、技能升級、背包擴充、補給與交易都會吃資源。

比較穩的使用順序：

1. 先升常用技能，讓核心循環成形。
2. 擴背包，降低每場地城因滿包而損失掉落的機率。
3. 補足鑑定、藥水與必要卷軸。
4. 對真正會穿一段時間的武器、防具做 item upgrade。
5. 有餘裕後再針對特定部位、商店刷新、交易或社群推薦路線投入金幣。

Nevergrind Wiki 的 Item Upgrades 頁面提到，城鎮升級裝備可以把一件物品升級最多 10 次；防具偏護甲與抗性，武器偏物理或魔法傷害，且成功是保證的。這代表升級比較像穩定補強，而不是賭爆裝的強化系統。

## 組隊是 NGO 的核心體驗

NGO 可以 solo，但組隊才比較能看出它的設計味道。官方 Steam 頁面與 wiki 都提到最多 5 人隊伍；Fandom mechanics 也整理過，隊伍越大，風險越高，但 magic find、經驗與金幣收益也會提高。

一個舒服的隊伍通常需要：

- 有人能穩定建立 aggro。
- 有人能處理治療、緩回、解壓或救場。
- 有人能快速處理高威脅目標。
- 有 utility 職補 haste、控制、buff、debuff 或資源壓力。
- 隊長知道怎麼帶路，而其他人知道什麼時候該等、該爆發、該停手。

如果你是新手，加入隊伍時可以先講清楚自己職業與等級，並觀察隊伍節奏。不要害怕問「等 tank 開嗎？」這種問題；在 NGO 裡，這比安靜地搶開怪更像老手。

## 操作與指令速查

Fandom 的 Chat Commands 頁面整理了不少常用指令。下面先列最常用、也最不容易踩坑的部分：

```text
/party message
/invite playerName
/promote playerName
/who
/who 5 10 dwarf cleric
/friend add playerName
/friends
/join channelName
/played
/clear
/camp
```

其他好用操作：

- 技能列：右鍵點一個技能，再右鍵另一個技能，可以交換快捷鍵位置。
- 商店：社群 tips 提到開商人介面時，`Shift + Left Click` 可以快速買賣。
- 聊天：方向鍵上可以找回先前送出的訊息，找隊伍時很省事。
- 背包：能擴就慢慢擴，地城裡滿包代表你開始跟 RNG 說不要。
- 地圖：隨機地城每次布局都不同，養成看小地圖、確認路線與 boss 方向的習慣；若你的版本或設定支援縮放，也可以用來找隱藏房與減少迷路。

<warning>
<p>有些舊攻略可能會提到特定難度或玩家數調整指令，例如 <code>/players #</code>。這類指令若沒有出現在目前遊戲內 <code>/help</code> 或官方文件，先不要當成一定可用。</p>
</warning>

## 新手成長路線

剛開始玩不要急著追終極裝備，先讓角色的基本循環穩定。

1. 選一個職業，先看 12 個技能大概支援什麼打法。
2. 前期裝備先看主屬性、生命、資源、抗性與主要傷害詞綴。
3. 每次回城都檢查技能升級與背包空間。
4. 第一次進組隊地城時，先保守打，觀察 aggro 和補師資源。
5. 中期開始記錄自己最缺的是傷害、命中、生存、回魔、回 spirit 還是冷卻。
6. 後期再查 class guide、unique / set 清單、BiS 討論與掉落目標。

這款遊戲的樂趣不是只在「刷到神裝」那一秒，而是在你逐漸看懂一件裝備為什麼好、某個職業為什麼突然強、某個隊友的 buff 為什麼讓整隊節奏變快。它很復古，但不是粗糙；它很刷寶，但不是只靠運氣。

## 參考資料

- [Nevergrind Online on Steam](https://store.steampowered.com/app/853450/Nevergrind_Online/)
- [Nevergrind Wiki Main Page](https://nevergrind.com/wiki/index.php?title=Main_Page)
- [Nevergrind Wiki: Item Upgrades](https://nevergrind.com/wiki/index.php?title=Item_Upgrades)
- [Nevergrind Wiki: Magic Find Mechanics](https://nevergrind.com/wiki/index.php?title=Magic_Find_Mechanics)
- [Nevergrind Online Wiki: Loot](https://nevergrind-online.fandom.com/wiki/Loot)
- [Nevergrind Online Wiki: Items](https://nevergrind-online.fandom.com/wiki/Items)
- [Nevergrind Online Wiki: What Is Nevergrind Online?](https://nevergrind-online.fandom.com/wiki/What_Is_Nevergrind_Online%3F){ignore-vars="true"}
- [Nevergrind Online Wiki: General Game Mechanics](https://nevergrind-online.fandom.com/wiki/General_Game_Mechanics)
- [Nevergrind Online Wiki: Chat Commands](https://nevergrind-online.fandom.com/wiki/Chat_Commands)
- [Nevergrind Online Wiki: Classes](https://nevergrind-online.fandom.com/wiki/Classes)
- [Re-actor: Nevergrind Online - Tips & Tricks](https://re-actor.net/nevergrind-online-tips-tricks/)
