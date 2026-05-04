# Nevergrind Online FC2 攻略 DB 連結索引

FC2 的 Nevergrind Online 攻略 DB 是高密度玩家資料庫，適合查日文 build、職業裝備例、符文、製作、套裝與 Unique 裝備分頁。這篇只整理「每個入口去哪裡、適合查什麼」，不複製原站的完整數值表；實際採用任何技能、裝備或刷圖建議前，仍要回遊戲內 tooltip 和官方公告確認。

- 檢視日期：`2026-05-04`
- 分類：[Nevergrind Online（絕不刷怪）遊戲指南](nevergrind-online-guide.md)
- 來源首頁：[Nevergrind Online 攻略DB](https://atelier3.web.fc2.com/ngo/index.html)
- 抓取範圍：以 `index.html` 與側欄 `menu.html` 為入口，收錄同網域 `/ngo/*.html` 內部頁；不收錄 CSS、JavaScript、圖片與 FC2 系統 footer
- 收錄數量：1 個首頁、1 個側欄、34 個主選單內容頁、21 個 Unique 部位分頁、49 個 Set 明細頁，合計 106 個內部 HTML
- 版本提醒：FC2 首頁本次回應的 `Last-Modified` 為 `2025-06-26`；站內 build、裝備、掉落與版本假設可能落後目前遊戲版本

<tldr>
<p>想照 FC2 讀攻略時，先看 <a href="https://atelier3.web.fc2.com/ngo/chart.html">ゲームの流れ</a> 抓成長節點，再用職業頁查 talent / gear / rotation，最後才進 item、set、rune、crafting 頁查終局素材。</p>
<p>FC2 的 class 頁多半是高階玩家視角，常預設已經有套裝、Unique、Legendary 或高技能 rank；新手不要直接照抄滿裝範例。</p>
<p>本地筆記若要引用 FC2，優先把它當「日文索引與玩家 meta snapshot」，不要把數值、掉落、season 或指令寫成官方保證。</p>
</tldr>

## 本地筆記對應方式

| FC2 資料類型 | 本地應補位置 | 讀法 |
| ------ | ------ | ------ |
| 成長、FAQ、縮寫 | [進度路線與 FC2 攻略讀法](nevergrind-online-progression-roadmap.md)、[中英名詞對照](nevergrind-online-terminology.md) | 用來補讀法、術語與操作提醒，不直接搬完整 Q&A |
| 職業 build | [職業系統總覽](nevergrind-online-classes.md) 與各職業專頁 | 用來標示「高階方向」與裝備依賴，不當成新手唯一模板 |
| Unique、Set、Legendary | [物品與戰利品總覽](nevergrind-online-items-loot.md)、[裝備收集路線](nevergrind-online-equipment-collection.md) | 用來查部位與候選裝，再回遊戲內 tooltip 驗證 |
| Crafting、Recipe、Rune | [鐵匠鋪](nevergrind-online-blacksmith.md)、[製作與配方](nevergrind-online-blacksmith-crafting-recipe-research.md)、[符文](nevergrind-online-runes.md) | 用來補製作流程、配方查詢與 rune 選擇，避免浪費不可逆素材 |
| Boss、怪物、狀態 | [地城冒險與任務攻略](nevergrind-online-dungeons.md)、[怪物分類與特性](nevergrind-online-monsters.md) | 用來補 boss 分布、怪物類型與狀態異常，但實戰仍看當前 UI |

## 首頁與全般

| FC2 連結 | 內容資訊 | 本地用途 |
| ------ | ------ | ------ |
| [Top](https://atelier3.web.fc2.com/ngo/index.html) | 攻略 DB 首頁、更新履歷與 Steam 入口圖 | 當 FC2 引用根入口；記錄站點更新日期與資料庫定位 |
| [menu.html](https://atelier3.web.fc2.com/ngo/menu.html) | 側欄導航，列出全般、物品、地城、職業與其他工具 | 抓完整站內連結時要從 iframe 側欄讀，不只看首頁本體 |
| [ゲームの流れ](https://atelier3.web.fc2.com/ngo/chart.html) | Normal、Nightmare、Hell、Heroic 的成長節點、抗性門檻、Lv25 / Lv45 talent 轉折與 Heroic 周回候選 | 對應本地進度路線；適合補「何時轉 build、何時補抗性」 |
| [よくある質問](https://atelier3.web.fc2.com/ngo/faq.html) | 角色建立、Ladder / Eternal、Season、城鎮操作、裝備比較、聊天指令、UI 卡住與物品重疊等 FAQ | 對應熱鍵、城鎮與來源判讀；版本敏感指令要回 `/help` 確認 |
| [キャラメイク関連](https://atelier3.web.fc2.com/ngo/charamake.html) | 性別、種族與職業 bonus 相關資訊 | 對應職業總覽；適合補種族選擇不必過度最佳化的提醒 |
| [各職の代表スキル](https://atelier3.web.fc2.com/ngo/selectlist.html) | 各職業代表技能速查 | 對應職業頁；只用來理解戰鬥語言，不直接取代技能 tooltip |
| [各職の厳選ユニーク](https://atelier3.web.fc2.com/ngo/selectlist2.html) | 各職常見武器、防具、飾品 Unique 候選 | 對應裝備收集；適合當高階裝備查表入口 |

## 物品主選單

| FC2 連結 | 內容資訊 | 本地用途 |
| ------ | ------ | ------ |
| [ユニーク](https://atelier3.web.fc2.com/ngo/unique.html) | Unique 裝備總入口，分武器、防具與飾品部位 | 對應 Unique 指南與收集路線 |
| [セット](https://atelier3.web.fc2.com/ngo/set.html) | Set 裝備總入口，按 Normal、Exceptional、Elite 分段 | 對應 Set 指南；用來查套裝名稱與部位 |
| [レジェンダリー](https://atelier3.web.fc2.com/ngo/legendary.html) | Legendary 清單，按武器、防具與飾品部位分段 | 對應 Legendary 筆記；具體數值仍需回遊戲內核對 |
| [クラフト](https://atelier3.web.fc2.com/ngo/mythical.html) | Crafting 基本、素材、socket、底材、需求等級、技能 mod 與 Ethereal 影響 | 對應鐵匠鋪製作與配方深度筆記 |
| [レシピ](https://atelier3.web.fc2.com/ngo/recipe.html) | Craft recipe 查表，按頭、胴體、武器、盾、弓等部位分類 | 對應配方查詢；適合補「先查部位再查 rune 組合」流程 |
| [ルーン](https://atelier3.web.fc2.com/ngo/rune.html) | Rune 清單與 rune 效果 | 對應符文指南；高價 rune 使用前要先確認裝備可用期 |
| [装備Mods](https://atelier3.web.fc2.com/ngo/itemmods.html) | 傷害、攻速、block、防禦、talent、stat、resource、resist、proc、Ethereal、socket 等 mod 類型 | 對應名詞表與裝備判斷；適合補詞綴分類 |

## Unique 部位分頁

| FC2 連結 | 內容資訊 |
| ------ | ------ |
| [ユニーク武器/片手斬り](https://atelier3.web.fc2.com/ngo/u1hs.html) | 片手斬り Unique，按 Normal / Exceptional / Elite 分段查物品 |
| [ユニーク武器/両手斬り](https://atelier3.web.fc2.com/ngo/u2hs.html) | 両手斬り Unique，按 Normal / Exceptional / Elite 分段查物品 |
| [ユニーク武器/片手鈍器（物）](https://atelier3.web.fc2.com/ngo/u1hbp.html) | 物理 one-hand blunt Unique，按階級查物品 |
| [ユニーク武器/片手鈍器（魔）](https://atelier3.web.fc2.com/ngo/u1hbm.html) | 魔法 one-hand blunt / focus 類 Unique，包含 Cryptic Paragon 等查表入口 |
| [ユニーク武器/両手鈍器（物）](https://atelier3.web.fc2.com/ngo/u2hbp.html) | 物理 two-hand blunt Unique，按階級查物品 |
| [ユニーク武器/両手鈍器（魔）](https://atelier3.web.fc2.com/ngo/u2hbm.html) | 魔法 two-hand blunt / staff 類 Unique，按階級查物品 |
| [ユニーク武器/刺突](https://atelier3.web.fc2.com/ngo/upiercer.html) | Piercer Unique，按階級查物品 |
| [ユニーク武器/盾](https://atelier3.web.fc2.com/ngo/ushield.html) | Shield Unique，按階級查物品 |
| [ユニーク武器/弓術](https://atelier3.web.fc2.com/ngo/ubow.html) | Bow Unique，按階級查物品 |
| [ユニーク武器/チャーム](https://atelier3.web.fc2.com/ngo/ucharm.html) | Charm Unique，按階級查物品 |
| [ユニーク防具/頭](https://atelier3.web.fc2.com/ngo/uhead.html) | Head Unique，分 cloth / leather / mail / plate 與階級查物品 |
| [ユニーク防具/胴体](https://atelier3.web.fc2.com/ngo/uchest.html) | Chest Unique，分 armor type 與階級查物品 |
| [ユニーク防具/肩](https://atelier3.web.fc2.com/ngo/ushoulder.html) | Shoulder Unique，分 armor type 與階級查物品 |
| [ユニーク防具/腕](https://atelier3.web.fc2.com/ngo/ubracer.html) | Bracer Unique，分 armor type 與階級查物品 |
| [ユニーク防具/手](https://atelier3.web.fc2.com/ngo/uglove.html) | Glove Unique，分 armor type 與階級查物品 |
| [ユニーク防具/腰](https://atelier3.web.fc2.com/ngo/ubelt.html) | Belt Unique，按階級查物品 |
| [ユニーク防具/太腿](https://atelier3.web.fc2.com/ngo/uleg.html) | Leg Unique，分 armor type 與階級查物品 |
| [ユニーク防具/靴](https://atelier3.web.fc2.com/ngo/uboot.html) | Boot Unique，分 armor type 與階級查物品 |
| [ユニーク防具/背中](https://atelier3.web.fc2.com/ngo/uback.html) | Cloak / back Unique，按階級查物品 |
| [ユニーク防具/ネックレス](https://atelier3.web.fc2.com/ngo/uamulet.html) | Amulet Unique，按階級查物品 |
| [ユニーク防具/指輪](https://atelier3.web.fc2.com/ngo/uring.html) | Ring Unique，按階級查物品 |

## Set 明細頁

| FC2 連結 | 內容資訊 |
| ------ | ------ |
| [Alderon's セット](https://atelier3.web.fc2.com/ngo/alderon.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Aradune's セット](https://atelier3.web.fc2.com/ngo/aradune.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Asaph's セット](https://atelier3.web.fc2.com/ngo/asaph.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Bishop's セット](https://atelier3.web.fc2.com/ngo/bishop.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Chancellor's セット](https://atelier3.web.fc2.com/ngo/chancellor.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Daahoud's セット](https://atelier3.web.fc2.com/ngo/daahoud.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Daiyo's セット](https://atelier3.web.fc2.com/ngo/daiyo.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Demetrium's セット](https://atelier3.web.fc2.com/ngo/demetrium.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Edarion's セット](https://atelier3.web.fc2.com/ngo/edarion.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Emissary's セット](https://atelier3.web.fc2.com/ngo/emissary.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Falzain's セット](https://atelier3.web.fc2.com/ngo/falzain.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Fanatic's セット](https://atelier3.web.fc2.com/ngo/fanatic.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Fansy's セット](https://atelier3.web.fc2.com/ngo/fansy.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Furor's セット](https://atelier3.web.fc2.com/ngo/furor.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Golem's セット](https://atelier3.web.fc2.com/ngo/golem.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Jibekn's セット](https://atelier3.web.fc2.com/ngo/jibekn.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Magnate's セット](https://atelier3.web.fc2.com/ngo/magnate.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Martyr's セット](https://atelier3.web.fc2.com/ngo/martyr.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Minotaur's セット](https://atelier3.web.fc2.com/ngo/minotaur.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Miranda's セット](https://atelier3.web.fc2.com/ngo/miranda.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Noik's セット](https://atelier3.web.fc2.com/ngo/noik.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Nylith's セット](https://atelier3.web.fc2.com/ngo/nylith.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Orator's セット](https://atelier3.web.fc2.com/ngo/orator.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Procyon's セット](https://atelier3.web.fc2.com/ngo/procyon.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Sage's セット](https://atelier3.web.fc2.com/ngo/sage.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Samurai's セット](https://atelier3.web.fc2.com/ngo/samurai.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Sarvida's セット](https://atelier3.web.fc2.com/ngo/sarvida.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Scourge's セット](https://atelier3.web.fc2.com/ngo/scourge.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Scryer's セット](https://atelier3.web.fc2.com/ngo/scryer.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Servant's セット](https://atelier3.web.fc2.com/ngo/servant.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Sidey's セット](https://atelier3.web.fc2.com/ngo/sidey.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Sinifay's セット](https://atelier3.web.fc2.com/ngo/sinifay.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Spinalzz's セット](https://atelier3.web.fc2.com/ngo/spinalzz.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Starcaller's セット](https://atelier3.web.fc2.com/ngo/starcaller.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Stockade's セット](https://atelier3.web.fc2.com/ngo/stockade.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Swiftraven's セット](https://atelier3.web.fc2.com/ngo/swiftraven.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Tigole's セット](https://atelier3.web.fc2.com/ngo/tigole.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Tsubodai's セット](https://atelier3.web.fc2.com/ngo/tsubodai.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Tunso's セット](https://atelier3.web.fc2.com/ngo/tunso.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Tyranid's セット](https://atelier3.web.fc2.com/ngo/tyranid.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Ubar's セット](https://atelier3.web.fc2.com/ngo/ubar.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Vagabond's セット](https://atelier3.web.fc2.com/ngo/vagabond.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Vagrant's セット](https://atelier3.web.fc2.com/ngo/vagrant.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Volaki's セット](https://atelier3.web.fc2.com/ngo/volaki.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Wyvern's セット](https://atelier3.web.fc2.com/ngo/wyvern.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Yizeren's セット](https://atelier3.web.fc2.com/ngo/yizeren.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Zak's セット](https://atelier3.web.fc2.com/ngo/zak.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Zamtil's セット](https://atelier3.web.fc2.com/ngo/zamtil.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |
| [Zarth's セット](https://atelier3.web.fc2.com/ngo/zarth.html) | Set 明細頁，列部位、套裝 bonus 與可查錨點 |

## 地城、怪物與 Boss

| FC2 連結 | 內容資訊 | 本地用途 |
| ------ | ------ | ------ |
| [状態異常一覧](https://atelier3.web.fc2.com/ngo/statuseffect.html) | 狀態異常列表 | 對應怪物 traits、控場與抗性說明 |
| [特殊モンスター](https://atelier3.web.fc2.com/ngo/unimon.html) | Monster mods、monster type、champion / unique / boss 類型 | 對應怪物分類與特性指南 |
| [ボスまとめ](https://atelier3.web.fc2.com/ngo/boss.html) | Act I 到 Act IV 的地區與 boss 分布 | 對應地城路線、boss 目標與刷圖候選 |

## 職業頁

| FC2 連結 | 內容資訊 | 本地用途 |
| ------ | ------ | ------ |
| [ウォーリアー](https://atelier3.web.fc2.com/ngo/warrior.html) | Warrior 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應戰士（Warrior）高階 build 讀法 |
| [クルセイダー](https://atelier3.web.fc2.com/ngo/crusader.html) | Crusader 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應十字軍（Crusader）/ 神聖近戰讀法 |
| [シャドウナイト](https://atelier3.web.fc2.com/ngo/shadowknight.html) | Shadow Knight 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應暗影騎士（Shadow Knight）坦輸混合讀法 |
| [モンク](https://atelier3.web.fc2.com/ngo/monk.html) | Monk 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應武僧（Monk）物理輸出讀法 |
| [ローグ](https://atelier3.web.fc2.com/ngo/rogue.html) | Rogue 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應盜賊（Rogue）輸出與裝備依賴提醒 |
| [レンジャー](https://atelier3.web.fc2.com/ngo/ranger.html) | Ranger 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應遊俠（Ranger）弓術與隊伍工具讀法 |
| [バード](https://atelier3.web.fc2.com/ngo/bard.html) | Bard 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應吟遊詩人（Bard）buff / support 讀法 |
| [ドルイド](https://atelier3.web.fc2.com/ngo/druid.html) | Druid 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應德魯伊（Druid）治療、元素與隊伍讀法 |
| [クレリック](https://atelier3.web.fc2.com/ngo/cleric.html) | Cleric 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應牧師（Cleric）與 Scion 輸出筆記 |
| [シャーマン](https://atelier3.web.fc2.com/ngo/shaman.html) | Shaman 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應薩滿（Shaman）治療、debuff 與 DoT 讀法 |
| [ウォーロック](https://atelier3.web.fc2.com/ngo/warlock.html) | Warlock 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應術士（Warlock）DoT / fear / spell build 讀法 |
| [エンチャンター](https://atelier3.web.fc2.com/ngo/enchanter.html) | Enchanter 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應恩路者 / 幻術師（Enchanter）haste、control 與支援讀法 |
| [テンプラー](https://atelier3.web.fc2.com/ngo/templar.html) | Templar 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應天騎士（Templar）混合支援 / 法系讀法 |
| [ウィザード](https://atelier3.web.fc2.com/ngo/wizard.html) | Wizard 基本資訊、talent 範例、裝備例與戰鬥節奏 | 對應巫師（Wizard）元素輸出與 resist reduction 讀法 |

## 其他工具與查表

| FC2 連結 | 內容資訊 | 本地用途 |
| ------ | ------ | ------ |
| [英語・略語など](https://atelier3.web.fc2.com/ngo/english.html) | 英文縮寫、組隊常用語與翻譯工具提示 | 對應中英名詞對照與社群溝通 |
| [武器DPS計算機](https://atelier3.web.fc2.com/ngo/dpscalc.html) | Weapon DPS 輸入表單與計算結果 | 對應裝備判斷；僅當輔助估算，不取代遊戲內面板 |
| [ルーンの選び方](https://atelier3.web.fc2.com/ngo/runeselect.html) | 武器與防具 rune 選擇，分物理、弓、魔法、命中、mana recovery 等情境 | 對應符文指南與 crafting 成本判斷 |
| [持ち帰るアイテム](https://atelier3.web.fc2.com/ngo/loot.html) | 裝備收集、金錢效率與值得帶回城的項目 | 對應裝備收集路線與金錢效率 |
| [ギャンブルのすすめ](https://atelier3.web.fc2.com/ngo/gambling.html) | Gambling 規則與推薦項目，包含飾品、特定 Unique / Set / Legendary 方向 | 對應賭博指南與 gold sink 判斷 |

## 外部連結

| 來源位置 | 連結 | 用途 |
| ------ | ------ | ------ |
| FC2 首頁主圖 | [Steam 商店頁](https://store.steampowered.com/app/853450/Nevergrind_Online/) | 官方商店、公告與更新入口；版本敏感資訊優先回這裡查 |

## 更新本地筆記時的注意事項

- 若只需要「FC2 哪頁查什麼」，連回本文即可，不要在攻略首頁重複 106 筆清單。
- 若要補職業頁，只摘出該職 build 的方向、裝備依賴與新手不宜照抄的風險。
- 若要補物品頁，優先整理「部位、用途、查表方式」，不要搬完整 item stat。
- 若要補 crafting / rune，先標記不可逆成本與版本風險，再引用 FC2 的對應頁面。
- 若 FC2、Fandom、Steam 或遊戲內資料互相衝突，回到 [公開來源判讀與疑難排解](nevergrind-online-public-source-notes.md) 的來源優先順序。
