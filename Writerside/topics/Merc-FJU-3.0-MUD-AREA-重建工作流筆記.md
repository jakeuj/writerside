# Merc-FJU 3.0 MUD AREA 重建工作流筆記

這篇筆記整理 [merc-fju-3.0](https://github.com/jakeuj/merc-fju-3.0/tree/codex/world-map-area-rebuild) 在 `codex/world-map-area-rebuild` 分支上的 AREA rebuild workflow。重點不是單一 area 的房間描述怎麼寫，而是怎麼把 `world map -> area plan -> mapmd-json -> .roo -> runtime validation` 串成一條可持續迭代的開發鏈。

- 檢視時間：`2026-03-26`
- 本機 HEAD：`e85a5bb9`
- HEAD 訊息：`Add city_hongnong implementation milestone`

## 這個分支目前在做什麼

這個分支把舊 MUD 的區域開發整理成比較明確的 `spec-first` 流程：

1. 先用 `area/world_map.md` 決定世界拓樸、母城位置與交通主骨架。
2. 再用 `plans/area/*.md` 與 `area/rebuild_plan.md` 管單區 queue、`delivery_gate` 與下一步。
3. 單區設計落在 `area/<area>/map.md`，其中的 `mapmd-json` 是 machine-readable canonical graph。
4. 接著用 generator 投影 `.roo`，再補 `index / mob / obj / res / shp / directory.lst`。
5. 最後用 build、startup smoke、`log/*`、`debug/*` 與 world checker 證明 area 真的可載入。

以 `2026-03-26` 這次檢視為例，tracker 的狀態大致如下：

| 日期 | Area | 狀態 |
| ------ | ------ | ------ |
| `2026-03-24` | `road_north_border` | 完成第一輪 runtime implementation |
| `2026-03-25` | `fort_northern_watch` | 完成 implementation commit `f9b06073` |
| `2026-03-26` | `city_hongnong` | 仍在 `In Progress`，但 `delivery_gate` 已是 `implementation_ready_for_commit` |

也就是說，這個分支不是零散地補房間，而是持續沿著 world graph 把單區 spec、runtime 邊界與驗證證據一起補齊。

## Source of Truth 順序

這個 repo 對 area rebuild 的事實來源有明確順位，讀檔順序大致如下：

| 層級 | 主要檔案 | 作用 |
| ------ | ---------- | ------ |
| 1 | `AGENTS.md` | repo 級規則、環境、驗證節奏與 area rebuild 約束 |
| 2 | `plans/0001-world-map-area-rebuild.md` | 全局 workflow、`delivery_gate`、固定 prompt 與 queue 規則 |
| 3 | `area/rebuild_plan.md` | 日常看板，決定 `todo / in_progress / done / blocked` |
| 4 | `plans/area/NNNN-*.md` | 單區題材、world links、保留房號與驗證意圖 |
| 5 | `area/<area>/map.md` | 單區 narrative spec；其中 `mapmd-json` 是 canonical graph |
| 6 | `area/directory.lst`、`area/<area>/*`、`src/load.c`、`src/act_move.c` | 真正會被 loader 吃到的 runtime 資料與載入規則 |

有一條很重要的判讀原則：

- 如果 `map.md` 的 prose 和 `mapmd-json` 不一致，先以 `mapmd-json` 為準，再回頭修 prose。

## 七層開發流程

整條 AREA rebuild pipeline 可以拆成七層：

1. `World Graph`
   - 入口是 `area/world_map.md`
   - 用來決定城市、驛站、關隘、野外與地下鏈在世界骨架上的相對位置
2. `Area Queue`
   - 入口是 `area/rebuild_plan.md`
   - 決定現在該做哪一區，而不是想到哪就補哪
3. `Area Plan`
   - 入口是 `plans/area/NNNN-*.md`
   - 固定 `level_range`、`reserved_room_block`、`external_links`、`theme_basis`
4. `Area Spec`
   - 入口是 `area/<area>/map.md`
   - 把 narrative spec 與 `mapmd-json` 寫在同一份檔案裡
5. `Projection + Implementation`
   - 用 generator 產出 `.roo`
   - 再補 `index / mob / obj / res / shp / directory.lst`
6. `Runtime Validation`
   - 跑 spec validate、world checker、build、startup smoke、log/debug 檢查
7. `Commit / Merge Gate`
   - 依 `delivery_gate` 決定是繼續修、先 commit，還是可以進下一區

## 新 AREA 的最小操作流程

如果要照這個分支的方式新增或重建一個 area，最小流程可以抓成下面這樣：

1. 先讀 `AGENTS.md`、`area/rebuild_plan.md`、對應 `plans/area/NNNN-*.md`。
2. 確認 area slug、`level_range`、`reserved_room_block`、`planned_vnum_range`、`external_links`。
3. 撰寫 `area/<area>/map.md`，把 narrative spec 與 `mapmd-json` 一次補齊。
4. 先驗證 spec，再決定要不要輸出 `.roo`。
5. `.roo` 穩定後，再補 `index / mob / obj / res / shp`。
6. 把 area 掛進 `area/directory.lst`，並同步 boundary room。
7. 跑 build、startup smoke、`log/*`、`debug/*`、world checker。
8. 更新 tracker、單區 plan、必要的 current-game registry，最後再看 `delivery_gate` 能不能前進。

常用命令大致會長這樣：

```bash
# 1. 驗證單區 map.md / mapmd-json
python3 tools/mapmd_validate.py area/city_hongnong/map.md

# 2. 只驗證 spec，不輸出 .roo
python3 .agents/skills/merc-area-builder/scripts/generate_roo_from_map_md.py \
  area/city_hongnong/map.md \
  --validate-only

# 3. 正式輸出 .roo scaffold
python3 .agents/skills/merc-area-builder/scripts/generate_roo_from_map_md.py \
  area/city_hongnong/map.md

# 4. 檢查 world consistency
python3 scripts/world_consistency_checker.py --fail-on-warning

# 5. 本機編譯
make -C src clean && make -C src merc

# 6. startup smoke
cd src
./startup.bash merc.ini

# 7. 判斷目前 area 應該停在哪個 gate
python3 tools/area_acceptance_gate.py city_hongnong
```

## `reload` 指令不要誤會

> **注意**
>
> 這個分支目前的 `reload` 指令只定義了 `reload object <號碼>` 與 `reload mobile <號碼>`。
> 也就是說，這套 AREA rebuild workflow 不能直接假設存在 `reload area <slug>` 這種熱重載流程。
> 真正的驗證閉環，還是 `mapmd_validate.py`、`.roo` 生成、`world_consistency_checker.py`、編譯、`startup.bash`、`log/*` 與 `debug/*`。

這點很重要，因為它會直接影響你怎麼設計開發節奏：

- 單區修改完成後，不是只靠遊戲內重載指令就算驗證完畢。
- 真正可信的證據是 loader 可讀、邊界相通、build 成功、startup 有成功訊號，而且 `debug/*` 沒冒出新的 area 相關錯誤。

## `city_hongnong` 為什麼值得拿來當樣板

如果要找一個目前最適合拿來參考的 area，我會優先看 `city_hongnong`，原因是它把整條鏈串得很完整：

- 有單區計畫：`plans/area/0102-city-hongnong.md`
- 有完整 spec：`area/city_hongnong/map.md`
- 有 `mapmd-json`
- 有 generator 輸出的 `roo/18701-18711`
- 有 `index / mob / obj / res / shp`
- 有 `fort_hulao/14101 <-> city_hongnong/18701` 的 runtime boundary
- 有 tracker 記錄 validation 結果，最後停在 `implementation_ready_for_commit`

如果想看不同 family 的對照樣板，也可以一起讀：

- `road_north_border`
  - 看道路型 area 怎麼接城市邊界
- `fort_northern_watch`
  - 看關隘 / watch 類型的 runtime milestone 怎麼收斂成可提交狀態

## 目前 queue 的節奏

這個 workflow 不是單純照世界圖一路往西抄，而是刻意維持 queue variety。`2026-03-26` 檢視時：

- `Todo` 是空的
- `In Progress` 只有 `city_hongnong`
- `Current Recommended Next Step` 是先 commit `city_hongnong`
- commit 後，下一個 west-line actionable area 才是 `wild_hongnong_farmland`

這代表固定 prompt `繼續實作下一個待建 area` 的真正意思是：

- 先續做目前可執行的 area
- 只有當 `delivery_gate` 允許，才切到下一區
- 不能因為想先做新題材，就跳過還沒收乾淨的 `in_progress`

## 參考入口

- [AGENTS.md](https://github.com/jakeuj/merc-fju-3.0/blob/codex/world-map-area-rebuild/AGENTS.md)
- [plans/0001-world-map-area-rebuild.md](https://github.com/jakeuj/merc-fju-3.0/blob/codex/world-map-area-rebuild/plans/0001-world-map-area-rebuild.md)
- [area/rebuild_plan.md](https://github.com/jakeuj/merc-fju-3.0/blob/codex/world-map-area-rebuild/area/rebuild_plan.md)
- [area/world_map.md](https://github.com/jakeuj/merc-fju-3.0/blob/codex/world-map-area-rebuild/area/world_map.md)
- [docs/area-development-handbook.md](https://github.com/jakeuj/merc-fju-3.0/blob/codex/world-map-area-rebuild/docs/area-development-handbook.md)
- [docs/codex-area-workflow.md](https://github.com/jakeuj/merc-fju-3.0/blob/codex/world-map-area-rebuild/docs/codex-area-workflow.md)
- [area/city_hongnong/map.md](https://github.com/jakeuj/merc-fju-3.0/blob/codex/world-map-area-rebuild/area/city_hongnong/map.md)
