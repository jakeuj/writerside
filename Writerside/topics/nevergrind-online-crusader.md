# Nevergrind Online 十字軍（Crusader / Paladin）坦克與神聖混合指南

十字軍（Crusader / Paladin）在 Tank 脈絡裡不是單純的高防禦職，而是把板甲、盾牌 threat、暈眩、自補、短暫無敵與神聖 / arcane 範圍傷害放在同一個角色裡。新手可以先把它理解成「能承傷的功能型前排」；進入中後期後，再依隊伍需求切向物理型續航、魔法型 AoE，或 undead / demon 特攻路線。

- 檢視日期：`2026-05-05`
- 分類：[Nevergrind Online 職業系統總覽](nevergrind-online-classes.md)
- 延伸閱讀：[進度路線與 FC2 攻略讀法](nevergrind-online-progression-roadmap.md)、[Set Items](nevergrind-online-set-items.md)、[Zamtil's Plenitude](nevergrind-online-set-items.md#zamtils-plenitude)
- 資料來源：Nevergrind Wiki `Paladin`、Fandom `Crusader` / `Classes` / `General Game Mechanics`、FC2 / atelier3 `Crusader` 職業頁
- 版本提醒：`Crusader` 與 `Paladin` 名稱在來源間可能不一致；技能名稱、threat 數值、rank 斷點與裝備例請以目前遊戲內 tooltip 為準

<tldr>
<p>Fandom 把 <code>Crusader</code> 列為 Tank，並描述為可穿 plate armor、混合 melee skills 與 spells 的職業。</p>
<p>Nevergrind Wiki 的 <code>Paladin</code> 說法也接近：defensive hybrid melee、plate armor、stuns、healing，以及對 undead 的強化。</p>
<p>FC2 的讀法更偏玩家 meta：十字軍雖在 Tank 分類中，但後期常以範圍輸出、自給自足與特定地城適性來評估。</p>
</tldr>

## 在 Tank 脈絡中的定位 {#crusader-tank-context}

Tank 的基礎任務是建立威脅值（Threat / Aggro）並承受危險窗口。Fandom 的 general mechanics 說明，怪物通常會看誰的 threat 最高；如果脆皮輸出一開場就丟大型 AoE，很容易被怪轉頭。十字軍的特殊之處在於，它不是只靠血量或護甲接怪，而是用多種「打、暈、補、擋、短暫無敵」工具把前排壓力拆開處理。

和另外兩個 Tank 比較時，可以這樣讀：

| Tank | 主要語言 | 和十字軍的差異 |
| ------ | ------ | ------ |
| 戰士（Warrior） | 最直覺的物理前排；Fandom 說明其物理防禦與生命值最高 | 戰士更像標準節奏控制者；十字軍則用法術、治療、stun 與 undead / demon bonus 補出混合價值 |
| 暗影騎士（Shadow Knight） | 攻擊性最強的 Tank，帶 fear、life tap 與 debuff | 暗影騎士靠攻擊壓力與吸血維持節奏；十字軍更常被拿來處理神聖 AoE、無敵窗口與自保 |
| 十字軍（Crusader） | 板甲 + 盾牌 threat + healing + stun + arcane / holy 類輸出 | 不是最單純的肉盾，而是能依地城與隊伍補洞的功能型 Tank |

<note>
<p>FC2 甚至把十字軍描述成「雖然曾被分類為 Tank，但現在更像範圍 DPS」的玩家觀點。公開筆記中適合把這句理解成 meta 觀察：高階玩家不只問十字軍能不能扛，還會問它能不能同時清怪、補耐性與處理 undead / demon 場景。</p>
</note>

## 核心戰術工具 {#crusader-tools}

Fandom `Crusader` 頁列出的技能 threat 顯示，十字軍有多個能主動建立 threat 的技能，而且部分技能在裝備盾牌時會放大 threat。

| 技能 | 來源重點 | 實戰讀法 |
| ------ | ------ | ------ |
| `Zealous Slam` | Fandom 列為 225% threat、taunt target；裝盾時 threat amplified | 單體開怪與穩住目標的核心語言之一 |
| `Rebuke` | Fandom 列為 180% threat，cone 3 stagger，裝盾時 threat amplified | 面對多怪或前排壓力時，用來補範圍 threat 與打斷節奏 |
| `Vengeance` | Fandom 列為 150% threat，taunt target，並讓下一次物理攻擊有 riposte 互動 | 讓十字軍不是純施法前排，仍保留近戰反擊語言 |
| `Consecrate` | Fandom 列為 200% threat，可疊自身 `Consecrate`，提高 all resists | FC2 也把它當成物理型十字軍補耐性與循環的重要技能 |
| `Holy Wrath` | Fandom 說明會 stun；FC2 提到可作為 `Rampage` 對策 | 危險怪物連擊或關鍵技能前，用 stun 爭取安全窗口 |
| `Seal of Sanctuary` | Fandom 說明短時間保護自身免受傷害，並強化 healing 與 arcane damage | 戰鬥前或高壓組合出現時使用，是十字軍最像功能型 Tank 的保命按鍵 |
| `Divine Grace` / `Benevolence` | Fandom 列為單體與群體治療工具 | 自保與補位能力強，但治療也會影響 threat 節奏，不能取代正式 healer 的全程責任 |
| `Blessed Hammer` / `Divine Judgment` | Fandom 說明可造成 arcane damage，且對 undead / demon 有 bonus | 讓魔法型十字軍在特定地城中兼任 AoE / 特攻輸出 |

## 物理型與魔法型怎麼分 {#crusader-build-directions}

FC2 把十字軍拆成偏魔法與偏物理的裝備 / talent 讀法。這些不是唯一答案，但很適合用來理解中後期轉向。

| 方向 | 核心技能 / 斷點 | 適合情境 | 注意 |
| ------ | ------ | ------ | ------ |
| 魔法型（Judicator） | `Blessed Hammer`、`Divine Judgment`、`Seal of Sanctuary` | 對 undead / demon、Riven Grotto 類目標、需要 AoE 或 arcane 方向時 | 會更吃技能 rank、施法節奏、arcane 相關裝備與抗性補洞 |
| 物理型（Herald / Protector） | `Consecrate`、`Zealous Slam`、`Holy Wrath` | 單體、較不挑地城、需要穩定前排續航時 | FC2 認為物理型對 Enchanter 支援依賴很高；沒有 haste / support 時循環手感會下降 |
| 混合前排 | shield threat、stun、自補、耐性裝 | 小隊缺前排控制或需要 someone to hold the room 時 | 不要同時追所有方向；先決定這場要補 threat、生存、AoE，還是 undead / demon 特攻 |

<tip>
<p>如果你還在前中期，先把十字軍玩成穩定前排：補 armor、resists、stun、healing 與常用技能 rank。等能穩定刷 Hell / Heroic 後，再追 FC2 那種以技能斷點與特定裝備組合為核心的高階模板。</p>
</tip>

## 裝備與隊伍協作 {#crusader-gear-team}

十字軍能穿 plate，也能使用多種近戰武器與弓術欄位；Fandom 也提到它取得 dual wield，但主要常被理解成能在副手裝 caster weapon 的彈性。作為 Tank 時，盾牌很重要，因為 general mechanics 說所有職業都能用盾牌格擋部分物理或 magic nuke 傷害，而十字軍本身又有多個「裝盾時 threat amplified」的技能。

裝備判斷可以先問三件事：

1. 這件裝有沒有讓我更穩：armor、stamina、all resists、stun / silence resistance、block、healing 或 resource。
2. 這件裝有沒有讓核心循環到斷點：`Blessed Hammer`、`Consecrate`、`Zealous Slam`、`Judicator`、`Herald` 或相關 mastery。
3. 這件裝有沒有服務地城目標：undead / demon bonus、arcane damage、enemy resistance reduction、magic find 或特定 route。

FC2 的魔法型十字軍裝備例提到，雖然 `Consecrate` 可疊抗性，但高壓地城仍可能需要額外抗性腿；像 [Zamtil's Plenitude](nevergrind-online-set-items.md#zamtils-plenitude) 這種跨職業抗性裝就屬於「為了通過高難度生存檢查而借 slot」的案例。

隊伍上，十字軍和支援職的關係很密切。恩路者 / 幻術師（Enchanter）提供的 haste / control 會改善部分循環；吟遊詩人（Bard）則能用歌曲提高團隊節奏與容錯。相反地，如果輸出和治療在十字軍還沒建立 threat 前就爆發，十字軍再硬也很難把每隻怪立刻拉回來。

## 讀來源時的注意事項 {#crusader-source-notes}

- Fandom 適合確認職業分類、技能名、threat、shield threat 與基礎 mechanics。
- Nevergrind Wiki `Paladin` 是舊式 / 官方 wiki 命名脈絡，適合確認「defensive hybrid melee、plate armor、stun、healing、undead」這條核心身份。
- FC2 適合讀高階 build、rank、裝備例與玩家 meta，但不要把它寫成官方規則。
- `Crusader` / `Paladin` 名稱不一致時，優先看技能組：板甲、stun、healing、undead / demon bonus、shield threat 與神聖 / arcane 工具。

## 參考資料

- [Nevergrind Online Wiki: Classes](https://nevergrind-online.fandom.com/wiki/Classes)
- [Nevergrind Online Wiki: General Game Mechanics](https://nevergrind-online.fandom.com/wiki/General_Game_Mechanics)
- [Nevergrind Online Wiki: Crusader](https://nevergrind-online.fandom.com/wiki/Crusader)
- [Nevergrind Online Wiki: Warrior](https://nevergrind-online.fandom.com/wiki/Warrior)
- [Nevergrind Online Wiki: ShadowKnight](https://nevergrind-online.fandom.com/wiki/ShadowKnight)
- [Nevergrind Wiki: Paladin](https://nevergrind.com/wiki/index.php?title=Paladin)
- [FC2 攻略 DB：Crusader](https://atelier3.web.fc2.com/ngo/crusader.html)
- [FC2 攻略 DB：Warrior](https://atelier3.web.fc2.com/ngo/warrior.html)
