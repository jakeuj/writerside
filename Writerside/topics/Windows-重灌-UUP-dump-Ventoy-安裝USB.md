# Windows 重灌筆記：用 UUP dump 下載 ISO，搭配 Ventoy 製作安裝 USB

想重灌 Windows 11 或 Windows 10，但又不想每次換版本都重做一次開機隨身碟，我自己比較偏好這個組合：先用 UUP dump 準備 ISO，再把 ISO 放進 Ventoy 隨身碟。之後如果只是想換版本、補新映像檔，通常只要複製新的 ISO 進去就可以了。

## 這篇筆記適合的情境

- 想自己選 Windows 版本、語言、架構，甚至指定特定 build
- 想把同一支 USB 同時放 Windows 安裝檔、Linux ISO、救援工具
- 不想每次換 ISO 都重新燒錄一次 USB

<note>
<p>如果你只是想拿一份一般穩定版的 Windows 安裝媒體，直接使用 Microsoft 官方 ISO 或 Media Creation Tool 通常會更省事。UUP dump 比較適合想自己挑版本、語言、架構，或想拿到較新整合更新映像的人。</p>
</note>

## 重灌前先確認

- 先備份桌面、文件、下載資料夾、瀏覽器書籤與常用設定
- 如果系統磁碟有開 BitLocker，先把 Recovery Key 留好
- 確認這台電腦原本的 Windows 版本與啟用方式，避免重灌後裝錯版本
- 準備一支至少 16GB 的 USB 隨身碟
- 如果是比較舊的機器，先把網卡或儲存控制器驅動備份起來

## 整體流程

<procedure title="Windows 重灌流程" id="windows-reinstall-flow">
    <step>
        <p>先用 UUP dump 準備想安裝的 Windows ISO。</p>
    </step>
    <step>
        <p>把 Ventoy 安裝到 USB 隨身碟。</p>
    </step>
    <step>
        <p>把 ISO 直接複製到 Ventoy 分割區，不用額外解壓縮。</p>
    </step>
    <step>
        <p>從 USB 開機，在 Ventoy 選單中選擇要進入的 ISO。</p>
    </step>
    <step>
        <p>完成 Windows 安裝後，跑 Windows Update，補驅動與常用工具。</p>
    </step>
</procedure>

## 第一步：用 UUP dump 下載 Windows ISO

[UUP dump](https://uupdump.net/?lang=zh-tw) 的定位很簡單，就是幫你從 Windows Update 伺服器整理出可下載、可轉成 ISO 的 Windows 映像檔。一般重灌我會優先選正式公開版，不太會拿 Dev 或 Canary 來當主力工作機的重灌來源。

### 先查組建號碼會比較準

如果你想透過 UUP dump 下載特定組建版本的 ISO，先知道組建號碼通常會比直接用關鍵字搜尋更快也更準。只用關鍵字查詢時，結果常常很多，對一般使用者來說很容易混淆。

所以我的做法通常是：

1. 先到微軟官方的 Windows release health 頁面查版本與組建號碼。
2. 確認自己要的是哪個正式發行組建。
3. 回到 UUP dump 直接用組建號碼搜尋。

常用參考：

- [Windows 11 正式發行組建](https://learn.microsoft.com/zh-tw/windows/release-health/windows11-release-information)
- [Windows 10 正式發行組建](https://learn.microsoft.com/zh-tw/windows/release-health/release-information)

### 選版本時我的習慣

- `Latest Public Release`：一般使用者優先，最適合重灌主力機
- `Release Preview` 或 `Beta`：想先看下一版功能時再用
- `Dev` 或 `Canary`：偏測試用途，不建議直接拿來當日常工作機重灌來源

### 下載流程

1. 打開 [UUP dump](https://uupdump.net/?lang=zh-tw)。
2. 選你要的 Windows 版本、架構與語言。
3. 選 edition，例如 `Windows 11 Pro` 或 `Windows 11 Home`。
4. 到下載選項時，優先選擇能直接轉成 ISO 的方式。
5. 依照 UUP dump 提供的下載腳本，把檔案抓回來並完成 ISO 轉換。
6. 確認最後有拿到 `.iso` 檔即可。

### UUP dump 詳細操作步驟

如果你希望和參考教學一樣，照畫面一步一步操作，可以直接走下面這個流程。

#### STEP 1：搜尋 OS 組建

1. 打開 [UUP dump](https://uupdump.net/?lang=zh-tw)。
2. 在搜尋框輸入你查好的組建號碼。
3. 如果不知道 build，也可以先用關鍵字搜尋，但結果通常比較多、比較容易混淆。

#### STEP 2：選擇下載版本

搜尋結果通常會看到不同架構與不同類型的版本，這裡至少先看兩件事：

- 架構是不是你要的，例如 `x64` 或 `arm64`
- 是否帶有 `Cumulative`

我自己的習慣是優先選 `Cumulative` 的版本，因為它通常已經先整合重要更新，安裝完後還要補的更新量會少一些，ISO 也相對精簡。

#### STEP 3：選擇 ISO 語言

依照你實際要安裝的語系選擇即可。像我自己是繁體中文使用者，通常就會選 `中文（繁體）`。

#### STEP 4：選擇 ISO 版本

這一步是決定 ISO 裡要包含哪些 edition。

- 如果你只需要單一版本，例如 `Pro`，只勾那一個就好
- 如果你想把 `Home`、`Pro`、`Enterprise` 等一起做進去，後面下載選項就要改成支援額外版本的模式

#### STEP 5：下載套件

這一步很重要，因為很多人會以為這裡按下載之後拿到的就是 ISO，但其實不是。

比較實用的選法：

- 一般情況：選 `使用 aria2 下載並轉換`
- 想把多個版本一起做進同一份 ISO：選 `使用 aria2 下載、轉換並建立額外版本`

另外，下方的轉換選項可以依需求調整。如果有勾選清理類型的選項，完成後殘留的中間檔通常會少一些。

<note>
<p>這個步驟下載下來的通常不是 ISO 本體，而是包含設定與下載邏輯的腳本／套件。真正的 ISO 下載與合併會在你執行腳本之後才開始。</p>
</note>

#### STEP 6：執行下載腳本

1. 把剛剛下載回來的套件解壓縮。
2. 進到資料夾後，執行裡面的命令腳本。
3. 在 Windows 環境下，通常會是 `.cmd` 之類的批次檔。

#### STEP 7：開始下載檔案

當你執行腳本後，這時才會真正開始下載 ISO 所需的元件檔案。前面在網站上勾選的語言、版本、架構與整合選項，都會在這一步反映到實際下載內容。

#### STEP 8：開始合併生成 ISO

當所有必要檔案都下載完成後，腳本通常會自動進入下一步，把這些元件整合並生成 ISO。這個過程通常不需要手動另外下指令，等它跑完即可。

#### STEP 9：確認 ISO 製作完成

如果腳本最後出現類似 `Press 0 to exit.` 這種提示，通常就代表 ISO 已經建立完成了。離開腳本後，回到原本的資料夾確認是否已經看到輸出的 `.iso` 檔。

<tip>
<p>如果你只是要單純重灌 Windows，不特別追求多版本整合，建議先做一份單一版本、單一語言的 ISO。流程會更單純，也比較不容易在後面選錯版本。</p>
</tip>

<tip>
<p>如果你只是一般家用或工作機重灌，先求穩再求新。比起追最新 Insider build，通常選正式公開版會省掉更多後續麻煩。</p>
</tip>

## 第二步：把 Ventoy 安裝到 USB

Ventoy 的優點是先把 USB 做成可開機載具，之後只要把 ISO 複製進去就能直接開。這和 Rufus 這類一次寫一個映像檔的工具相比，維護起來輕鬆很多。

<warning>
<p>第一次把 Ventoy 安裝到 USB 時，目標隨身碟上的資料會被清掉。開始前先確認你選到的是正確的 USB，不是外接硬碟或其他資料碟。</p>
</warning>

### Windows

在 Windows 上是最直接的做法：

1. 到 [Ventoy Releases](https://github.com/ventoy/Ventoy/releases/latest) 下載 Windows 版壓縮檔。
2. 解壓縮後，以系統管理員身分執行 `Ventoy2Disk.exe`。
3. 選擇要安裝 Ventoy 的 USB 隨身碟。
4. 首次安裝按下 `Install`，如果已經做過 Ventoy，只是要升級版本，則使用更新流程即可。
5. 安裝完成後，把剛剛做好的 Windows ISO 複製到 USB 第一分割區。

補充幾個我自己會注意的點：

- 大多數情況維持預設設定就夠了，不用一開始就改很多選項。
- 如果目標機器開著 Secure Boot，再考慮把 Secure Boot support 一起打開。
- MBR 和 GPT Ventoy 都支援，沒有特別需求時，我通常先用預設值。

### macOS

我目前沒有把 macOS 原生安裝 Ventoy 寫成主流程，原因是官方文件主要寫 Windows 與 Linux，官方 release 頁面也以 Windows zip、Linux tar.gz、LiveCD ISO 為主。若你手邊是 Mac，最穩的做法是透過 Linux VM，或借一台 Windows/Linux 電腦先把 USB 做成 Ventoy。

如果你要在 Mac 上完成這件事，我會建議這樣做：

1. 在 Mac 上開一台 Linux VM，並把 USB 裝置直通給 VM。
2. 下載 [Ventoy 最新 Linux 安裝包](https://github.com/ventoy/Ventoy/releases/latest) 並解壓縮。
3. 在 Linux VM 中用 `lsblk` 確認 USB 裝置名稱，例如 `/dev/sdb`。
4. 切到解壓縮後的目錄，執行以下指令安裝 Ventoy：

```bash
sudo bash Ventoy2Disk.sh -i /dev/sdX
```

如果你的目標機器需要 Secure Boot，可改用：

```bash
sudo bash Ventoy2Disk.sh -i -s /dev/sdX
```

如果你很明確知道自己要 GPT，也可以加上 `-g`：

```bash
sudo bash Ventoy2Disk.sh -i -g /dev/sdX
```

完成後，把 USB 從 VM 卸載，再接回 macOS，將 Windows ISO 複製到 Ventoy 的主要分割區即可。

<note>
<p>上面這段是在 Linux VM 裡執行，不是直接在 macOS Terminal 用 <code>/dev/diskX</code> 跑。這樣做比較符合 Ventoy 官方目前提供的安裝方式，也比較不容易踩到平台相容性問題。</p>
</note>

## 第三步：把 ISO 複製到 Ventoy 隨身碟

Ventoy 和傳統燒錄工具最大的差別，就是你不用把 ISO 解開，也不用重新格式化 USB。只要把 `.iso` 檔直接複製到隨身碟裡，Ventoy 開機時就會自動把它列進選單。

我通常會這樣整理：

- `/Windows/Windows11-24H2-zh-tw.iso`
- `/Linux/ubuntu-24.04.iso`
- `/Tools/Clonezilla.iso`

這不是 Ventoy 的硬性要求，只是自己之後比較好找。它支援多個映像檔一起放，開機時再從選單挑要進哪一個。

## 第四步：從 USB 開機並安裝 Windows

1. 把做好的 Ventoy USB 插到要重灌的電腦。
2. 開機時按 Boot Menu 快捷鍵，例如 <code>F12</code>、<code>F11</code>、<code>Esc</code> 或主機板對應按鍵。
3. 選擇 USB 開機，通常看到 <code>UEFI</code> 的項目就優先選它。
4. 進入 Ventoy 選單後，挑你要的 Windows ISO。
5. 進到 Windows 安裝程式後，再照需求選語言、版本與安裝位置。

<warning>
<p>如果你是做真正的乾淨重灌，在選磁碟與分割區時要非常小心。刪錯分割區就是直接清資料，尤其是有多顆 SSD 或外接硬碟時更容易誤刪。不確定時，先停下來確認磁碟容量與編號，不要硬按下一步。</p>
</warning>

## 重灌後我會先做的事

- 先跑一次 Windows Update，把系統更新與大部分驅動補齊
- 裝晶片組、顯卡、網卡等必要驅動
- 確認 Windows 啟用狀態是否正常
- 把瀏覽器同步、密碼管理器、雲端同步資料拉回來
- 再回頭補安裝常用軟體，可以參考這篇 [初始安裝](初始安裝.md)

## 常見問題

### UUP dump 跟 Microsoft 官方 ISO 有什麼差別

如果你只是要一份穩定、正常可安裝的 Windows ISO，官方來源最單純。UUP dump 的價值在於你可以自己挑版本、語言、架構與更新整合，彈性比較大。

### Ventoy 和 Rufus 最大差別是什麼

我自己的理解很簡單：

- Rufus 比較像一次把單一映像檔寫進 USB
- Ventoy 比較像先把 USB 變成可開機平台，之後只管把 ISO 複製進去

如果你常常換 ISO、常常重灌不同機器，Ventoy 真的方便很多。

### 我只有 Mac，可不可以直接做 Ventoy USB

如果你想要的是穩定、少踩雷的流程，我會建議透過 Linux VM 或另一台 Windows/Linux 電腦來安裝 Ventoy。至少以 Ventoy 官方目前公開的文件與發行檔來看，主力教學仍然是 Windows 與 Linux 兩條路線。

## 參考資料

- [UUP dump 官網](https://uupdump.net/?lang=zh-tw)
- [UUP dump｜3 分鐘學會如何下載整合更新的 Win10/Win11 映像檔 (ISO)](https://adersaytech.com/tools/online-tool/uup-dump-review.html)
- [Ventoy 官方 GitHub](https://github.com/ventoy/Ventoy)
- [Ventoy 官方文件：Get Started](https://www.ventoy.net/en/doc_start.html)
- [Ventoy INSTALL/README](https://raw.githubusercontent.com/ventoy/Ventoy/master/INSTALL/README)
- [Ventoy2Disk.sh](https://github.com/ventoy/Ventoy/blob/master/INSTALL/Ventoy2Disk.sh)
