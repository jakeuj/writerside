# Nevergrind Online 物品與戰利品總覽

Nevergrind Online 的物品系統是遊戲長期黏著度的核心：你不是只在換更高等級的裝備，而是在一件件隨機掉落、商店刷新、boss 掉落、套裝與 unique 裡，尋找剛好符合自己 build 的詞綴組合。新手先學會看稀有度與詞綴，中期開始理解 magic find、首通、組隊與 boss 掉落，後期再用符文與 crafting 把好裝備推成核心裝。

- 檢視日期：`2026-05-03`
- 資料來源：NotebookLM 摘要與心智圖、Fandom Loot / Items 頁、Nevergrind Wiki Magic Find Mechanics、Steam / SteamDB patch notes
- 版本提醒：公開 wiki、Fandom、日文 wiki 與遊戲內版本可能不同步；稀有度顏色、legendary / mythical 名稱、符文與 crafting 規則請以目前遊戲內 tooltip 為準

<tldr>
<p>不要只看顏色。藍裝可以補抗性，黃裝靠隨機詞綴翻身，unique / set 要看固定效果是否支援 build。</p>
<p>Magic find 不是越堆越無腦；官方 wiki 提到裝備 magic find 有遞減與 breakpoints，chain combo、horde bonus、boss 類型也會影響掉落。</p>
<p>後期裝備價值常取決於 sockets、runes、all talents / all skills、抗性、資源與特定技能加成。</p>
</tldr>

![Nevergrind Online 物品與戰利品心智圖](nevergrind-online-items-loot-mind-map.png){thumbnail="true" width="720"}

## 稀有度怎麼看

在更大的 Items & Loot 脈絡下，rarity 不是單純的強度排行，而是「這件掉落物有多少隨機性、多少固定效果、能不能服務 build」的第一層篩選。Fandom Loot 頁目前把物品整理成藍、黃、紫、綠四大類；NotebookLM 摘要與心智圖則提到橙色 legendary。這代表公開資料可能跨版本，判斷時要先看遊戲內 tooltip。

| 顏色 / 類型 | 常見意義 | 看裝重點 |
| ------ | ------ | ------ |
| 藍色 `Magic` | 1 到 2 個隨機詞綴 | 單一詞綴可能很高，適合補抗性、資源或特定缺口 |
| 黃色 `Rare` | 2 到 6 個隨機詞綴 | 詞綴組合對了，可能比固定裝更適合當前 build；例如帶 `All Talents` 的項鍊很值得留意 |
| 紫色 `Unique` | 固定詞綴種類，但數值可能波動 | 看固定效果、技能加成、部位與數值 roll；像 [Cryptic Paragon（Haniwa）](nevergrind-online-cryptic-paragon-haniwa.md) 這類裝備還要看隨機技能是否命中 |
| 綠色 `Set` | 固定詞綴與套裝 bonus | 單件未必最強，多件 bonus 才是重點；可看 [套裝 Set Items 指南](nevergrind-online-set-items.md) |
| 橙色 / Legendary / Mythical | NotebookLM 與新版資料提到的高階裝備概念 | 先以遊戲內顏色、名稱與 patch 說明為準；可用 [Legendary Items 清單筆記](nevergrind-online-legendary-items.md) 查候選名稱 |

舊 Fandom 頁特別提醒，magic 物品雖然詞綴少，但單一詞綴可能比同等級 rare 還高。這在補極端短板時很重要：你不一定要等完美黃裝，早期一件高抗性藍裝就能救你一條命。換句話說，紫色、綠色或橙色通常代表更明確的 build 方向，但一件神 roll 的藍裝或黃裝仍可能在特定場合更好用。

## 品質階級與特殊狀態

顏色 rarity 之外，裝備還有基礎性能階級。來源資料把它整理成 `Normal`、`Exceptional`、`Elite` 三段；同名或同類型裝備若底材階級不同，基礎 armor、damage、level requirement 和可升級價值也會不同。這點在 gambling、查 [Legendary Items](nevergrind-online-legendary-items.md)、比較 set / unique 時都很重要。

| 品質階級 | 常見意義 | 看裝重點 |
| ------ | ------ | ------ |
| `Normal` | 前期底材與低等裝備 | 適合過渡、補抗性、補技能，通常不要太早投入高階 rune |
| `Exceptional` | 中期底材與中段裝備 | 開始能支援 build 成形，值得保留好 roll 或特殊 socket 裝 |
| `Elite` | 後期底材與高階裝備 | 才進入認真比較 perfect roll、set bonus、unique effect 與交易價值的階段 |

來源摘要也提到 `Ethereal` 與 `Indestructible` 這種不完全等同於顏色 rarity 的特殊狀態：

- `Ethereal`：圖示可能呈半透明，來源摘要提到武器基礎攻擊或防具基礎防禦會大幅提高，但會有耐久風險。
- `Indestructible`：若出現在 ethereal 裝備上，代表耐久風險被抵消，通常會把裝備價值拉高。

<warning>
<p>Ethereal / Indestructible 的實際數值、耐久規則與出現方式請以目前遊戲內 tooltip 為準。這類狀態會直接影響是否值得投入 rune、升級或交易成本。</p>
</warning>

## 戰利品為什麼有趣

NGO 的 loot 設計比較接近老派 dungeon crawler：商店刷新、地城掉落、boss、chest、未鑑定裝備都可能出現驚喜。Fandom 入門頁也把它描述成「社交、管理裝備與技能、出任務、殺怪、拿 loot」的核心循環。

判斷一件裝備時，順序可以這樣抓：

1. 部位是否正在拖累你。
2. 詞綴是否支援目前 build。
3. 是否補上抗性、生命、armor、mana / spirit、haste 或命中。
4. unique / set 的固定效果是否能改變 rotation。
5. 是否有 sockets，可以接 [符文](nevergrind-online-runes.md) 做後期強化。
6. 是否值得花金幣升級、鑲嵌或留給分身。

## Magic find 與掉落機制

官方 Nevergrind Wiki 的 Magic Find Mechanics 頁把掉落流程拆成幾層：怪物死亡後先判斷是否掉物品，再判斷 set / unique、rare、magic，最後才可能成為白裝。這代表 magic find 不是單純「多掉東西」，而是影響物品品質判定。

常見提升方向：

- 裝備上的 magic find。
- chain combo。
- horde bonus，也就是同時打多個怪物的風險獎勵。
- monster type，例如 boss 本身就比普通怪更容易掉好東西。
- first-time boss kill / first dungeon bonus。
- monster con，也就是怪物名稱顏色所暗示的等級與危險度。
- heroic difficulty 與隊伍人數帶來的風險 / 獎勵提升。
- quest preferred item types；若任務偏好特定裝備類型，farm 特定部位時就有更明確方向。

<note>
<p>官方 wiki 提到裝備 magic find 有遞減，並列出 20、40、60、80 等 breakpoints；超過 80 後仍有收益，但效率會變差。刷寶裝不是完全不能堆，只是要和輸出、生存、資源取得平衡。</p>
</note>

## 首通、難度與組隊

NotebookLM 摘要與 Fandom 入門頁都強調：完成不同地城、打更高難度、組隊挑戰，都是提升掉落體驗的重要方式。

重點整理：

- 第一次完成地城或 boss，通常值得打，因為首通 / first-time boss kill 會提高 loot 價值。
- Heroic 比 normal 更危險，但會有更多怪與更好的 loot 機會。
- 隊伍最多 5 人；高難度與多人組隊會把風險、經驗、金幣與 rare item 期待一起拉高。
- act boss 通常比 zone boss 更硬，也更值得期待掉落。
- 怪物名稱顏色，也就是 con，能幫你判斷風險和獎勵是否值得。

如果你在 farm 特定部位，不要只打一條路線。Fandom 入門頁提到任務可能有偏好的掉落物品類型，因此你可以用任務目標與 boss 類型來提高特定裝備的期待值。

## 鑑定與整理

地城裡撿到的裝備常需要回城鑑定。NotebookLM 摘要提到可以用 identify scroll，也可以到城鎮的 Apothecary 用全部鑑定類功能；這類便利操作請以目前 UI 為準。

整理原則：

- 早期不要每件都留，先看部位、等級、職業可用性與主詞綴。
- 背包空間很值錢，Fandom 入門頁提到起始 bag space 很少，後續可用金幣擴充。
- 銀行適合放分身裝、特定抗性裝、套裝件與高價交易品。
- 未鑑定裝備如果部位和等級不對，不一定值得帶回。

## 金幣與商店策略

商店不是只買藥水。Fandom Loot 頁提到 merchants 會依角色等級提供裝備並定期 restock；不同商人偏好的裝備類型也不同，例如 alchemist 偏 caster / cloth，blacksmith 偏 mail / plate 與重武器。

金幣花法建議：

1. 先買必要補給、鑑定、技能升級與背包。
2. 中期開始檢查商店刷新，尤其是缺特定部位時。
3. 有餘裕後再碰 gambling 或高風險投資。
4. 值錢裝備優先帶回，例如 NotebookLM 摘要提到的 focus / stave、板甲、高等級 weapon base。
5. 鑲嵌符文前，先確認這件裝備值得長期穿。

## BiS 與關鍵物品

NotebookLM 摘要提到 [Cryptic Paragon（Haniwa）](nevergrind-online-cryptic-paragon-haniwa.md)、`Charlatan's Crest` 這類社群常討論的高價值裝備，也在 Cleric / caster build 中反覆出現。若要用試算表快速查 legendary item 名稱、品質、部位與詞綴方向，可以接著看 [Legendary Items 清單筆記](nevergrind-online-legendary-items.md)。這類名字值得記，但不要只靠名字判斷強度。

看高階裝時，至少確認：

- 等級需求與職業可用性。
- all talents / all skills 是否真的支援你的 build。
- magic find 是否犧牲太多輸出或生存。
- sockets 數與 rune plan。
- 詞綴 roll 是否接近你要的方向。
- 交易市場價格是否比自己硬 farm 合理。

## 後期客製化

後期把裝備推到下一層，常靠三件事：

- Item upgrades：官方 wiki 提到裝備可以在城鎮升級，提升防具或武器相關性能。
- Runes：Season 2 patch note 顯示 Blacksmith 的 enchanting counter 已啟用，可用 runes 強化 socketed items。
- Crafting：2025 patch note 顯示 crafting counter 後續加入 rune upgrade 與 crafting UI 改良。

前面提到的 ethereal / indestructible 類特殊狀態，也會直接影響後期客製化判斷。若 ethereal 的基礎性能提升存在於目前版本，耐久風險、是否同時有 indestructible、以及裝備本身 socket / roll 是否夠好，都會影響它值不值得投入符文。

## 參考資料

- [Nevergrind Online on Steam](https://store.steampowered.com/app/853450/Nevergrind_Online/)
- [Nevergrind Online Wiki: Loot](https://nevergrind-online.fandom.com/wiki/Loot)
- [Nevergrind Online Wiki: Items](https://nevergrind-online.fandom.com/wiki/Items)
- [Nevergrind Online Wiki: What Is Nevergrind Online?](https://nevergrind-online.fandom.com/wiki/What_Is_Nevergrind_Online%3F){ignore-vars="true"}
- [Nevergrind Wiki: Magic Find Mechanics](https://nevergrind.com/wiki/index.php?title=Magic_Find_Mechanics)
- [Nevergrind Wiki: Item Upgrades](https://nevergrind.com/wiki/index.php?title=Item_Upgrades)
- [SteamDB: Enchanting With Runes Enabled](https://steamdb.info/patchnotes/16172899/)
- [SteamDB: Added ability to upgrade runes via crafting](https://steamdb.info/patchnotes/18527675/)
