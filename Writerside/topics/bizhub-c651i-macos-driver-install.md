# bizhub C651i Mac 印表機驅動安裝說明

<web-summary>在 macOS 安裝 KONICA MINOLTA bizhub C651i 印表機驅動，並用固定 IP、IPP 佇列與 C651i PS driver 重新加入印表機。</web-summary>

印表機 IP 沒變、但設備換成 KONICA MINOLTA bizhub C651i 時，不要只沿用舊印表機佇列；先安裝 C651i 系列 macOS 驅動，再用同一個 IP 重新加入印表機，並在 `Use` 選單指定 `KONICA MINOLTA C651i PS`。

> 本文中的 IP、佇列名稱與本機路徑皆使用範例值；請替換成自己的印表機 IP 與環境設定。

<tldr>
<ul>
<li>下載並掛載 KONICA MINOLTA macOS driver DMG。</li>
<li>macOS 11 或更新版本使用 `C750i_C287i_C4050i_C751i_C4751i_11.pkg` 安裝。</li>
<li>新增 IP 印表機時選 `IPP`，Queue 用 `ipp`，Driver 選 `KONICA MINOLTA C651i PS`。</li>
<li>安裝完成後確認預設紙張大小是 `A4`。</li>
</ul>
</tldr>

## 適用情境

這篇筆記適合以下情境：

- 原本的印表機 IP 沒變，但實體設備更換成 bizhub C651i。
- macOS 的「印表機與掃描器」裡沒有自動選到正確機型。
- 新增時只看到 AirPrint 或 Generic PostScript Printer，缺少 C651i 的完整功能選項。
- 需要保留裝訂、紙匣、雙面列印、Account Track 或 User Authentication 等 KONICA MINOLTA driver 功能。

KONICA MINOLTA 香港產品頁將 bizhub C651i 列在數碼多功能彩色系統，主要特色包含彩色列印、高達每分鐘 65 張 A4，以及雲端與資安相關功能；規格頁也列出支援 macOS 10.14 or later。實際安裝時仍以下載到的驅動包 Readme 與企業 IT 規範為準。

## 前置條件

- 下載驅動 [C651i macOS driver](https://public.integration.yamayuri.kiku8101.com/publicdownload/download?fileId=D227C181-27CF-4BB2-BBE5-1DF725EA4541)
- 已知道印表機固定 IP，例如 `<printer-ip>`。
- macOS 使用者帳號具備管理員權限。
- 已下載 C651i 對應的 macOS driver DMG。
- Mac 可以連到印表機所在網段。

<note>
如果舊印表機佇列仍存在，建議先刪除再重加。IP 沒變不代表 driver 可以沿用，因為 macOS 可能仍套用舊型號的 PPD 或 AirPrint 設定。
</note>

## 安裝驅動

<procedure>
<step>
<p>下載驅動程式。</p>
<p>可從本文參考資料中的 KONICA MINOLTA Drivers &amp; Downloads 入口搜尋，也可以使用指定的 C651i macOS driver 下載連結。</p>
<p>從官方 Drivers &amp; Downloads 頁面找檔案時，搜尋 `bizhub C651i`，或用下拉選單選 <control>Office Colour A3</control> 與 <control>bizhub C651i</control>。進入結果後切到 <control>Driver</control>，語言選 <control>Traditional Chinese</control>，OS 則選目前使用的 macOS 版本，例如 <control>macOS Tahoe 26</control>。</p>
<img src="bizhub-c651i-drivers-downloads-language-os.png" alt="KONICA MINOLTA Drivers &amp; Downloads 頁面搜尋 bizhub C651i，Driver 語言選 Traditional Chinese，OS 選 macOS Tahoe 26" width="720" border-effect="line"/>
</step>
<step>
<p>打開下載到的 DMG，例如 `IT6PSMACOS_536AMU.dmg`。</p>
<p>如果點兩下後看起來沒有事情發生，先打開 Finder，在左側 <control>位置</control> 找已掛載的 `IT6_536A`；DMG 會像外接磁碟一樣出現在那裡。</p>
<img src="bizhub-c651i-finder-mounted-dmg.png" alt="Finder 左側位置顯示 IT6_536A 已掛載，右側有 Readme 與 C651i pkg 安裝程式" width="720" border-effect="line"/>
</step>
<step>
<p>在 DMG 內執行 macOS 11 以上使用的 installer：</p>

```text
C750i_C287i_C4050i_C751i_C4751i_11.pkg
```
</step>
<step>
<p>依序按 <control>Continue</control>、同意授權條款，最後按 <control>Install</control>。</p>
</step>
<step>
<p>輸入 macOS 管理員密碼，等到安裝程式顯示安裝完成。</p>
</step>
</procedure>

## 用系統設定新增印表機

<procedure>
<step>
<p>打開 <ui-path>系統設定 | 印表機與掃描器</ui-path>。</p>
</step>
<step>
<p>如果已有舊印表機，先移除舊佇列。</p>
</step>
<step>
<p>按 <control>加入印表機、掃描器或傳真機</control>，切到 <control>IP</control> 分頁。</p>
</step>
<step>
<p>填入 IP 與佇列資訊。</p>

| 欄位 | 建議值 |
|---|---|
| Address | `<printer-ip>` |
| Protocol | `IPP` |
| Queue | `ipp` |
| Name | `KONICA MINOLTA C651i` |
| Location | 可填辦公室位置或留空 |

</step>
<step>
<p>在 <control>Use</control> 或 <control>使用</control> 欄位選 <control>Select Software...</control>。</p>
</step>
<step>
<p>搜尋 `C651i`，選擇 `KONICA MINOLTA C651i PS`。</p>
</step>
<step>
<p>按 <control>Add</control> 完成新增，必要時依照實際配備設定紙匣、Finisher、Punch Unit 或其他選購配件。</p>
</step>
<step>
<p>回到 <ui-path>系統設定 | 印表機與掃描器</ui-path>，確認預設印表機是 `KONICA MINOLTA C651i`，並把 <control>預設紙張大小</control> 改為 `A4`。</p>
<img src="bizhub-c651i-printer-added-a4.png" alt="macOS 印表機與掃描器顯示 KONICA MINOLTA C651i 已加入，預設紙張大小設定為 A4" width="720" border-effect="line"/>
</step>
</procedure>

<warning>
不要選 `AirPrint` 或 `Generic PostScript Printer` 作為主要 driver。這兩者通常可以列印基本文件，但可能缺少紙匣、裝訂、Account Track、Secure Print 等機型功能。
</warning>

## Terminal 新增方式

如果已確認 driver 安裝完成，也可以用 Terminal 建立 CUPS 佇列。下面範例使用 IPP，請把 `<printer-ip>` 換成實際印表機 IP。

```bash
sudo lpadmin -p KONICA_MINOLTA_C651i \
  -E \
  -v ipp://<printer-ip>/ipp \
  -P /Library/Printers/PPDs/Contents/Resources/KONICAMINOLTAC651i.gz

sudo lpoptions -d KONICA_MINOLTA_C651i
```

如果要移除舊佇列：

```bash
sudo lpadmin -x <old-printer-queue-name>
```

## 驗證

確認 C651i driver 已被系統辨識：

```bash
lpinfo -m | grep -i 'C651i'
```

預期會看到類似：

```text
Library/Printers/PPDs/Contents/Resources/KONICAMINOLTAC651i.gz KONICA MINOLTA C651i PS
```

確認目前佇列：

```bash
lpstat -v
lpstat -p
lpstat -d
```

如果 driver、IP 與預設印表機都正確，再從「印表機與掃描器」或應用程式印一張測試頁。

在 <ui-path>系統設定 | 印表機與掃描器</ui-path> 也要確認：

- 預設印表機：`KONICA MINOLTA C651i`
- 預設紙張大小：`A4`

## 常見問題

### 找不到 `KONICA MINOLTA C651i PS`

先確認 pkg 是否安裝完成，再關閉並重新打開「系統設定」。如果還是找不到，重新執行 DMG 內的 pkg，或用下面指令確認 PPD 是否存在：

```bash
test -f /Library/Printers/PPDs/Contents/Resources/KONICAMINOLTAC651i.gz && echo installed
```

### macOS 提示 printer driver 已停用或未來 CUPS 不支援

新版 macOS 在使用傳統 PPD driver 時，可能會提示 printer driver 已停用或未來 CUPS 版本不再支援。若需要 KONICA MINOLTA 的完整列印功能，仍可先使用 vendor driver；如果只需要基本列印，才評估改用 AirPrint。

### IP 沒變，為什麼還要刪掉重加

因為「IP 位址」和「driver 型號」是兩件事。設備換成 C651i 後，舊佇列可能仍指向舊機型 driver，導致紙匣、雙面列印、裝訂或驗證功能異常。刪掉舊佇列再重新選 `KONICA MINOLTA C651i PS`，比較乾淨。

### 需要 Account Track 或 User Authentication

如果印表機端啟用了 Account Track 或 User Authentication，macOS 端也要在列印對話框或 driver 設定裡填入正確帳號資訊。不然工作可能送出後被設備拒收，或停在佇列中不列印。

## 參考資料

- [KONICA MINOLTA Hong Kong: bizhub C651i](https://www.konicaminolta.hk/hk/zh-hk/product/bizhub-c651i/)
- [KONICA MINOLTA Drivers & Downloads](https://www.btapac.konicaminolta.com/)
- [C651i macOS driver download](https://public.integration.yamayuri.kiku8101.com/publicdownload/download?fileId=D227C181-27CF-4BB2-BBE5-1DF725EA4541)
- 驅動包 `IT6PSMACOS_536AMU` 內的 `Readme.txt`
