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

<tip>
<p>如果你只是一般家用或工作機重灌，先求穩再求新。比起追最新 Insider build，通常選正式公開版會省掉更多後續麻煩。</p>
</tip>

## 第二步：把 Ventoy 安裝到 USB

Ventoy 的優點是先把 USB 做成可開機載具，之後只要把 ISO 複製進去就能直接開。這和 Rufus 這類一次寫一個映像檔的工具相比，維護起來輕鬆很多。

<warning>
<p>第一次把 Ventoy 安裝到 USB 時，目標隨身碟上的資料會被清掉。開始前先確認你選到的是正確的 USB，不是外接硬碟或其他資料碟。</p>
</warning>

<tabs>
    <tab title="Windows">
        <p>在 Windows 上是最直接的做法：</p>
        <ol>
            <li>到 <a href="https://github.com/ventoy/Ventoy/releases/latest">Ventoy Releases</a> 下載 Windows 版壓縮檔。</li>
            <li>解壓縮後，以系統管理員身分執行 <code>Ventoy2Disk.exe</code>。</li>
            <li>選擇要安裝 Ventoy 的 USB 隨身碟。</li>
            <li>首次安裝按下 <code>Install</code>，如果已經做過 Ventoy，只是要升級版本，則使用更新流程即可。</li>
            <li>安裝完成後，把剛剛做好的 Windows ISO 複製到 USB 第一分割區。</li>
        </ol>
        <p>補充幾個我自己會注意的點：</p>
        <ul>
            <li>大多數情況維持預設設定就夠了，不用一開始就改很多選項。</li>
            <li>如果目標機器開著 Secure Boot，再考慮把 Secure Boot support 一起打開。</li>
            <li>MBR 和 GPT Ventoy 都支援，沒有特別需求時，我通常先用預設值。</li>
        </ul>
    </tab>
    <tab title="macOS">
        <p>我目前沒有把 macOS 原生安裝 Ventoy 寫成主流程，原因是官方文件主要寫 Windows 與 Linux，官方 release 頁面也以 Windows zip、Linux tar.gz、LiveCD ISO 為主。若你手邊是 Mac，最穩的做法是透過 Linux VM，或借一台 Windows/Linux 電腦先把 USB 做成 Ventoy。</p>
        <p>如果你要在 Mac 上完成這件事，我會建議這樣做：</p>
        <ol>
            <li>在 Mac 上開一台 Linux VM，並把 USB 裝置直通給 VM。</li>
            <li>下載 <a href="https://github.com/ventoy/Ventoy/releases/latest">Ventoy 最新 Linux 安裝包</a> 並解壓縮。</li>
            <li>在 Linux VM 中用 <code>lsblk</code> 確認 USB 裝置名稱，例如 <code>/dev/sdb</code>。</li>
            <li>切到解壓縮後的目錄，執行以下指令安裝 Ventoy：</li>
        </ol>

        <code-block lang="bash">sudo bash Ventoy2Disk.sh -i /dev/sdX</code-block>

        <p>如果你的目標機器需要 Secure Boot，可改用：</p>

        <code-block lang="bash">sudo bash Ventoy2Disk.sh -i -s /dev/sdX</code-block>

        <p>如果你很明確知道自己要 GPT，也可以加上 <code>-g</code>：</p>

        <code-block lang="bash">sudo bash Ventoy2Disk.sh -i -g /dev/sdX</code-block>

        <p>完成後，把 USB 從 VM 卸載，再接回 macOS，將 Windows ISO 複製到 Ventoy 的主要分割區即可。</p>
        <note>
            <p>上面這段是在 Linux VM 裡執行，不是直接在 macOS Terminal 用 <code>/dev/diskX</code> 跑。這樣做比較符合 Ventoy 官方目前提供的安裝方式，也比較不容易踩到平台相容性問題。</p>
        </note>
    </tab>
</tabs>

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
