# 用 graphify 把 repo 做成知識圖，發布到 GitHub Pages

<web-summary>用 graphify 把 repo 的程式、文件與截圖整理成可互動的知識圖，補上 viewport、noindex 與返回連結後發布到 GitHub Pages；附建圖 token 成本實測、增量更新做法，以及 AST 與 LLM 節點 ID 對不上的修法。</web-summary>

在 repo 根目錄用 Claude Code 跑 `/graphify .`，會產生一個資料內嵌的 `graphify-out/graph.html`，可以直接放上 GitHub Pages。不過它是給本機看的：沒有 viewport、標題是檔案路徑，所以發布前要補上手機版面、`noindex` 與返回連結，並用 `.graphifyignore` 排除發布出去的那一頁，免得下次建圖把它抽回圖裡。以下以 [原價屋估價單分享](https://pc.jakeuj.com/) 為例，成品在 [pc.jakeuj.com/graph/](https://pc.jakeuj.com/graph/)。

<tldr>
<p>第一次建圖：<code>/graphify .</code>；之後只重抽有改的檔案：<code>/graphify . --update</code></p>
<p>發布：<code>python3 scripts/publish_graph.py</code> 寫出 <code>docs/graph/index.html</code></p>
<p>排除發布頁：<code>.graphifyignore</code> 加一行 <code>docs/graph/</code></p>
</tldr>

以下內容整理於 2026 年 10 月，graphify 版本為 `0.9.66`。

## graphify 會產出什麼 {#what-graphify-produces}

[graphify](https://github.com/Graphify-Labs/graphify)（PyPI 套件名 `graphifyy`，Apache-2.0）是給 AI coding assistant 用的 skill，把一個資料夾裡的程式、文件、PDF、圖片整理成知識圖：

- **程式碼**用 AST 做結構抽取，不呼叫 LLM、不花 token。
- **文件、PDF、圖片**要 LLM 讀：有設定 `GEMINI_API_KEY` 時用 Gemini；沒有的話，Claude Code 會自己分批派 subagent 去讀，截圖也會用 vision 看懂版面。
- 每條邊都標記 `EXTRACTED`（原文明寫）、`INFERRED`（推論）或 `AMBIGUOUS`（不確定），推論的邊附信心分數。

輸出在 `graphify-out/`：

| 檔案 | 用途 |
| --- | --- |
| `graph.html` | 互動圖（vis-network），可搜尋節點、看鄰居、依社群篩選 |
| `graph.json` | 圖的原始資料，之後 `/graphify query` 直接查它 |
| `GRAPH_REPORT.md` | 連結最多的節點、意外的跨檔關聯、社群凝聚度與建議問題 |
| `manifest.json`、`cache/` | `--update` 用來判斷哪些檔案改過、哪些可以沿用 |

社群（community）是演算法自動分的群，名稱則要由 agent 看完成員後命名；我讓它用繁體中文命名，例如「抓價與 Big5 解碼」、「店家報價計算」。

## 建圖成本實測 {#build-cost}

這個 repo 有 Python 腳本、前端 JS、GitHub Actions、技能文件、SDD 規格與驗收截圖。三次建圖的實測：

| 情境 | 抽取的檔案 | subagent token | 結果（節點／邊／社群） |
| --- | --- | --- | --- |
| 第一次全量建圖 | 62 個（程式 33、文件 19、圖片 10） | 約 74 萬 | 461／902／21 |
| `--update`：新增一批驗收截圖與 PDF | 9 個 | 約 24 萬 | 515／1,030／26 |
| `--update`：新功能改到兩份約 94KB 的 HTML | 25 個 | 約 81 萬 | 680／1,628／26 |

- token 是各 subagent 回報的總量，工具沒有拆成輸入與輸出。
- 程式碼只走 AST，不算在內；成本幾乎都花在文件與截圖。單一大型 HTML 一個檔就吃掉十幾萬 token，`--update` 只要碰到它就很貴。
- graphify 內建的 benchmark 估算，用圖回答一個問題約 1.5 萬 token，直接讀全部文字約 4.5 萬 token，大約省 3 倍。

## 建圖時踩到的坑 {#pitfalls}

### `.claude` 底下的節點 ID 對不上 {#pitfall-dot-path-id}

graphify 的節點 ID 是「repo 相對路徑 + 名稱」轉成小寫底線。AST 把 `.claude/skills/coolpc/scripts/fetch_coolpc.py` 轉成 `claude_skills_coolpc_scripts_fetch_coolpc`（去掉開頭的點），但讀文件的 subagent 照「非英數字元換成底線」的規則，產生的是 `_claude_skills_...`。結果文件指向程式碼的 27 條邊全部懸空。

合併前把語意抽取結果的 ID 開頭底線去掉就能對齊：

```python
def norm(node_id):
    return node_id.lstrip("_")

for n in chunk["nodes"]:
    n["id"] = norm(n["id"])
for e in chunk["edges"]:
    e["source"], e["target"] = norm(e["source"]), norm(e["target"])
for h in chunk.get("hyperedges", []):
    h["nodes"] = [norm(x) for x in h["nodes"]]
```

之後派 subagent 時，直接在 prompt 寫明「`.claude/` 底下的 ID 以 `claude_` 開頭」，就不會再發生。

### 發布出去的頁面被抽回圖裡 {#pitfall-self-ingest}

`docs/graph/index.html` 在 repo 裡，下一次 `--update` 會把它當成一份 80 萬 bytes 的 HTML 文件去抽，圖就變成在描述自己，還白花 token。在 repo 根目錄加 `.graphifyignore`（語法同 `.gitignore`）：

```text
# 發布出去的知識圖本身，不要再抽進圖裡
docs/graph/
```

### 重抽一個檔案會整批換掉它的節點 {#pitfall-reextract-ids}

`--update` 以檔案為單位：先刪掉該檔上次產生的所有節點，再放入這次的結果。如果 LLM 這次給同一個概念換了 ID，其他沒改的檔案連過來的邊就斷了。

做法是把「這個檔案上次產生的節點 ID 清單」連同 graph 裡的程式碼節點 ID 一起交給 subagent，要求仍存在的概念沿用舊 ID、只有新東西才取新 ID。照這樣做之後，兩份大型 HTML 重抽後舊 ID 全數保留，健康檢查沒有任何懸空的邊。

### 健康檢查的雜訊與推論邊 {#pitfall-health-noise}

`/graphify` 建完會跑健康檢查，第一次出現的警告大多不是真問題：

- **懸空的邊**：AST 記錄了 `import pathlib`、`import json` 這類標準庫，圖裡沒有對應節點；兩個腳本互相 import 時，相對 import 也可能對不到完整路徑的 ID。
- **self-loop**：Cloudflare Worker 的 `fetch` handler 裡呼叫全域 `fetch()`，被當成遞迴。
- **沒有節點的檔案**：純 JSON 檔（例如量測結果）AST 不產生節點，被文件引用時要自己補一個檔案節點。

另外，subagent 自己也會回報「這條是猜的」，例如截圖裡根本看不到某個功能，卻被連到該功能。這種邊我改成 `AMBIGUOUS`，報告的「建議問題」會把它列出來，提醒之後確認。

## 發布到 GitHub Pages {#publish}

`graph.html` 本身就適合靜態託管：

- 資料全部內嵌，只從 unpkg 載入 vis-network，而且帶 SRI 雜湊。
- 節點的 `source_file` 是 repo 相對路徑，沒有本機絕對路徑；發布前仍可以用 `grep -c '/Users/' graph.html` 確認是 0。
- 這個 repo 的圖約 80 萬 bytes，gzip 後約 5.9 萬 bytes，而且只有點進該頁才會載入，不影響主網站。

要補的是 metadata 與手機版面。我寫了一支 [publish_graph.py](https://github.com/jakeuj/architect-pc-builder/blob/main/scripts/publish_graph.py) 讀 `graphify-out/graph.html`，修改後寫到 `docs/graph/index.html`。核心是幾個「只取代一次、找不到就報錯」的替換，graphify 改版導致格式不同時會直接失敗，不會悄悄發布一頁壞掉的圖：

```python
def replace_once(text, pattern, repl, what):
    out, n = re.subn(pattern, lambda _: repl, text, count=1)
    if n != 1:
        raise SystemExit(f"publish_graph: 找不到 {what}, graphify 的輸出格式可能改了")
    return out

page = replace_once(page, r'<html lang="[^"]*">', '<html lang="zh-Hant">', "<html lang>")
page = replace_once(page, r"<title>.*?</title>", HEAD, "<title>")
page = replace_once(page, r"</style>", CSS + "</style>", "</style>")
page = replace_once(page, r'<div id="sidebar">', '<div id="sidebar">\n' + NOTE, '<div id="sidebar">')
```

`HEAD` 換掉原本的 `<title>`，補上 viewport、`noindex`、description 與 favicon：

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>專案知識圖｜原價屋估價單分享</title>
<meta name="description" content="原價屋估價單分享的程式、文件與驗收截圖關係圖，由 graphify 產生，給開發者參考。">
<link rel="icon" href="../favicon.svg" type="image/svg+xml" sizes="any">
```

`NOTE` 在側欄頂端放「回到主網站」的連結與產生日期。`CSS` 讓手機改成上下排：上面是圖，下面是可捲動的側欄。

```css
@media (max-width: 768px) {
  body { flex-direction: column; height: 100dvh; }
  #graph { flex: 1 1 auto; min-height: 0; }
  #sidebar { width: 100%; height: 45dvh; flex: none; border-left: none; overflow-y: auto; }
  #sidebar > * { flex-shrink: 0; }
  #search { font-size: 16px; }
}
```

`#sidebar > * { flex-shrink: 0; }` 不能省：側欄是 flex 直排，改成可捲動後子區塊仍會被壓縮，「Node Info」和「Communities」兩塊會疊在一起。`#search` 用 16px 是避免 iOS 點輸入框時自動放大。

## 為什麼設 noindex {#why-noindex}

從搜尋進到估價網站的是要配電腦的人，一張程式架構圖被收錄，只會稀釋網站主題，對這些訪客也沒有用。所以：

- 用 `<meta name="robots" content="noindex">`，**不要**在 `robots.txt` 擋這個路徑。Google 要能爬到頁面才看得到 `noindex`；被 `robots.txt` 擋掉的網址，仍可能因外部連結出現在搜尋結果裡。
- 不放進 sitemap，主網站也不放入口，只從 repo 的 README 與這篇筆記連過去。

## 之後怎麼更新 {#update-flow}

文件和截圖要靠 LLM 讀，所以我沒有把它接進每小時抓價的 GitHub Actions，而是在程式或文件有較大改動時手動更新：

```bash
# 1. 在 Claude Code 對話框輸入：/graphify . --update
# 2. 把新圖補上 metadata 後寫進網站目錄
python3 scripts/publish_graph.py
# 3. 只提交發布頁
git add docs/graph/index.html
git commit -m "更新專案知識圖"
```

`graphify-out/` 加進 `.gitignore`，但要留在本機：裡面的 `manifest.json` 與 `cache/` 是 `--update` 判斷哪些檔案改過、哪些結果可以沿用的依據，刪掉就只能重新全量建圖。

## 參考資料 {#references}

- [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)
- [scripts/publish_graph.py](https://github.com/jakeuj/architect-pc-builder/blob/main/scripts/publish_graph.py)
- [專案知識圖成品](https://pc.jakeuj.com/graph/)
- [Google Search Central：使用 noindex 封鎖搜尋索引](https://developers.google.com/search/docs/crawling-indexing/block-indexing)
- [Side Projects](Side-Projects.md)
