# CrossOver 升頻技術：DLSS、XeSS、TSR 與 MetalFX

在 Apple Silicon（M1 到 M4）上使用 CrossOver 選升頻技術時，結論先講：TSR 是 Unreal Engine 內建的 temporal upscaler，通常是 Mac + CrossOver 情境下最「原生」也最穩的選項；CrossOver 的 DLSS 不是 NVIDIA 原生 DLSS，而是 `DLSS powered by MetalFX`；XeSS 則不能走 Intel Arc / XMX 最佳路徑，實際效果要視遊戲與圖形 backend 而定。

<tldr>
    <p>TSR 是 Unreal Engine 內建方案；如果遊戲有 TSR，通常先測它。</p>
    <p>DLSS 在 CrossOver Mac 26 是 MetalFX 路徑，不是 NVIDIA Tensor Core DLSS。</p>
    <p>XeSS 在 Mac 上通常不是 Intel XMX 加速路徑，優先度通常低於 TSR、FSR、DLSS / MetalFX 實測。</p>
</tldr>

## 白話結論

在 Windows PC 上，DLSS、XeSS、FSR、TSR 都是「降低內部渲染解析度，再重建成較高輸出解析度」的升頻技術；差別在於誰提供、靠不靠特定硬體，以及演算法在哪一層運作。

到了 Mac + CrossOver，差異會變成：

```text
DLSS -> CrossOver 攔截 / 對應 -> MetalFX
XeSS -> Intel XMX 路徑不可用，視遊戲走跨廠商 fallback 或直接無效
TSR  -> Unreal Engine 內建 temporal upscaler，通常不需要 GPU 廠商專屬硬體
```

所以實務上可以先這樣排：

1. Unreal Engine 遊戲有 TSR：先測 TSR。
2. 遊戲有 FSR：拿 FSR 當穩定基準。
3. CrossOver 26 有 DLSS 開關且 backend 是 D3DMetal / DXMT：再測 DLSS / MetalFX。
4. XeSS 有選項時可以測，但不要預設它會比 TSR 或 FSR 更好。

## 技術差異速查

| 技術 | 來源 | 在原生 Windows 的定位 | 在 Mac + CrossOver 的理解 |
| ---- | ---- | --------------------- | ------------------------- |
| DLSS | NVIDIA | RTX GPU 上的 AI / neural rendering 技術，DLSS Super Resolution 會用 AI 從低解析度輸出重建高解析度畫面。 | Apple Silicon 沒有 NVIDIA GPU；CrossOver Mac 26 的 DLSS 是 powered by MetalFX，必須搭配 D3DMetal 或 DXMT，且遊戲內也要啟用 DLSS。 |
| XeSS | Intel | AI-based temporal super sampling / anti-aliasing。Intel Arc / Iris Xe 有最佳化路徑，也提供跨廠商實作。 | 不能走 Intel Arc XMX 最佳路徑；若遊戲與 backend 支援，通常是跨廠商 fallback 或轉譯後路徑，效果高度看遊戲。 |
| TSR | Epic / Unreal Engine | Unreal Engine 5 內建、platform-agnostic 的 temporal upscaler，用較低內部解析度重建 4K 等輸出。 | 對 Unreal Engine 遊戲來說通常最直接，較少依賴 GPU 廠商 SDK 或 CrossOver 的特殊替換。 |
| FSR | AMD | 跨廠商升頻技術，許多遊戲內建，通常不鎖特定 GPU。 | 常是 Mac + CrossOver 的穩定基準選項；畫質與版本差異要實測。 |

## DLSS 在 CrossOver 裡是什麼？

不是「CrossOver 把 DLSS 關掉」，而是「CrossOver 提供一個 DLSS 相容路徑，背後改用 MetalFX」。

可以把流程想成：

```text
Windows 遊戲的 DLSS 路徑
  -> CrossOver 的 D3DMetal / DXMT backend
  -> MetalFX
  -> Apple GPU 執行升頻或相關影像處理
```

所以遊戲選單裡看到 DLSS，不代表 Mac 突然有 NVIDIA DLSS 硬體。比較精準的說法是：CrossOver 讓部分遊戲的 DLSS 選項可以在 Mac 上透過 MetalFX 產生類似升頻效果。

CodeWeavers 在 CrossOver Mac 26 的 Advanced Settings 文件中，將 `DLSS` 描述為 `DLSS powered by MetalFX`。同一段文件也明講兩個限制：

- 遊戲內必須啟用 DLSS。
- CrossOver 必須使用 D3DMetal 或 DXMT，這個設定才會生效。

也就是說，只有在「遊戲本身有 DLSS 路徑」且「CrossOver 的 backend 支援」時，這個開關才有機會發揮作用。不是每款遊戲看到選項都一定有效，也不是所有 CrossOver 版本都會有同樣的行為。

### 為什麼不是真正的 NVIDIA DLSS？

NVIDIA DLSS 是 NVIDIA 的 AI / neural rendering 技術，DLSS Super Resolution、Frame Generation、Ray Reconstruction 等功能依賴 GeForce RTX GPU 的硬體與 NVIDIA 軟體堆疊。Apple Silicon 內建的是 Apple GPU，不是 NVIDIA GPU，也沒有 NVIDIA Tensor Core。

因此在 M4、M3、M2、M1 Mac 上：

- 不會有原生 NVIDIA DLSS。
- 不會因為 CrossOver 打開 DLSS，就變成 GeForce RTX 硬體路徑。
- 實際效果要看 CrossOver、MetalFX、遊戲本身與圖形 backend 的支援程度。

<note>
    <p>這裡的重點不是「DLSS 這個選項是假到完全沒用」，而是它不是 NVIDIA 原生實作。實測仍可能帶來 FPS 或畫面穩定度改善。</p>
</note>

## XeSS 在 Mac + CrossOver 怎麼看？

Intel XeSS-SR 是 AI-based temporal super sampling / anti-aliasing 技術。Intel 官方文件提到，XeSS 有 Intel 最佳化實作，也有 HLSL-based cross-vendor implementation；D3D12 需求包含 DirectX 12、SM 6.4 與建議 DP4a 或等價硬體加速，D3D11 則有限制，只支援 Intel Arc Graphics 或更新的 Intel GPU。

放到 Apple Silicon + CrossOver：

- 不會走 Intel Arc / XMX 最佳化路徑。
- 若遊戲是 D3D12 且 XeSS 跨廠商路徑能在轉譯後正常跑，才可能有可用效果。
- 若遊戲是 D3D11，官方限制本來就更嚴格，在 Mac + CrossOver 下不要期待它一定有效。
- 實務上常常會是「能開不代表值得開」，畫質、延遲、FPS 都要跟 TSR / FSR / DLSS-MetalFX 實測比較。

所以可以把 XeSS 排在「有空再測」的位置。它不是不能用，而是在 Mac + CrossOver 的風險與不確定性比 TSR 或 FSR 高。

## TSR 在 Mac + CrossOver 怎麼看？

TSR 是 Unreal Engine 的 Temporal Super Resolution，官方定位是 platform-agnostic temporal upscaler。它不屬於 NVIDIA、Intel 或 AMD 的 GPU vendor SDK，而是遊戲引擎渲染管線內建的 temporal upscaling / anti-aliasing 方案。

白話說，TSR 比較像「Unreal Engine 自己的強化版 TAA + 升頻」。

在 Mac + CrossOver 這種轉譯環境下，TSR 的優勢是：

- 不需要 NVIDIA Tensor Core。
- 不需要 Intel XMX。
- 不需要 CrossOver 把某個 vendor SDK 特別替換成 MetalFX。
- 如果遊戲本身是 Unreal Engine 5 且有暴露 TSR，通常相容性比較直覺。

缺點也很現實：

- 效能提升不一定比 DLSS / XeSS / FSR 大。
- 有些場景可能模糊、拖影或細節不穩。
- TSR 只在採用 Unreal Engine 且遊戲有提供相關選項時才有意義。

## CrossOver 相關名詞

| 名詞 | 白話說明 |
| ---- | -------- |
| Bottle | CrossOver 裡的隔離環境。每個 bottle 有自己的 Windows 檔案、登錄檔、runtime 與進階設定。 |
| Backend | 圖形轉譯後端。決定 DirectX 要怎麼被轉成 macOS 能跑的圖形 API。 |
| D3DMetal | Apple Game Porting Toolkit 來源的圖形 API 轉譯層，支援 DirectX 11 / DirectX 12 遊戲，最後走 Metal。 |
| DXMT | Metal-based 的 Direct3D 11 實作。遇到 D3D11 遊戲時，有時比 D3DMetal 或 DXVK 更適合。 |
| DXVK | 將 Direct3D 10 / 11 轉成 Vulkan 的轉譯層。macOS 上還需要再透過其他層銜接到 Metal，路徑與 D3DMetal / DXMT 不同。 |
| WineD3D | Wine 內建的 Direct3D 實作，相容性和效能通常不是現代遊戲的首選，但可作為 fallback。 |
| MetalFX | Apple 的升頻與 temporal anti-aliasing 相關技術。CrossOver Mac 26 的 DLSS 開關就是 powered by MetalFX。 |
| FSR | AMD FidelityFX Super Resolution，通常比較跨平台。很多遊戲內建 FSR，實務上常是 Mac/CrossOver 排錯時的穩定選項。 |
| TSR | Unreal Engine 內建 temporal upscaler。對 UE5 遊戲來說，通常比 vendor SDK 替換路徑更單純。 |
| XeSS | Intel 的 AI-based temporal upscaler。Mac 上沒有 Intel Arc / XMX 路徑，能不能好用要看遊戲和 backend。 |

## 建議設定方式

1. 在 CrossOver 選取遊戲所在的 bottle。
2. 打開該 bottle 的進階設定。
3. 圖形 backend 優先測試 <control>Auto</control>，不穩時再手動切 <control>D3DMetal</control> 或 <control>DXMT</control>。
4. 如果要測 DLSS / MetalFX，啟用 CrossOver 的 <control>DLSS</control> 開關，並在遊戲內也選 DLSS。
5. 如果遊戲提供 TSR、FSR、XeSS，分別測試相同品質檔位，例如 Quality / Balanced / Performance。
6. 每次只改一個變數：先固定 backend，再換升頻技術；或先固定升頻技術，再換 backend。
7. 觀察 FPS、frame time、輸入延遲、拖影、閃爍、UI 銳利度與場景切換是否破圖。

## 實務選擇建議

- **UE5 遊戲有 TSR**：先測 TSR。它通常是 Mac + CrossOver 下最單純的引擎內建路徑。
- **想穩定**：測 TSR 或 FSR。FSR 通常不依賴 NVIDIA / Intel 專用硬體，也比較常見於跨平台遊戲。
- **想畫質**：可以試 CrossOver 的 DLSS / MetalFX 路徑。有些遊戲畫面會比 FSR 更順眼。
- **看到 XeSS**：可以測，但優先度通常最低；在 Apple Silicon 上不要期待 Intel 最佳化路徑。
- **想效能**：TSR、FSR、DLSS / MetalFX、XeSS 都跑一次。不同遊戲的瓶頸不同，沒有絕對答案。
- **遇到 bug**：先切回 FSR 或關掉升頻，再換 D3DMetal / DXMT 測試，不要只改一個選項就下結論。

## 常見誤解

### 開 DLSS 就一定比較快？

不一定。升頻通常可以降低內部渲染解析度，但 CrossOver 還有轉譯成本、記憶體壓力、shader 編譯、遊戲自身 bug 等變數。某些遊戲打開 DLSS / MetalFX 會變快，某些遊戲可能沒差，甚至會出現破圖或閃退。

### Frame Generation 也是真的 NVIDIA Frame Generation？

不是。若遊戲在 CrossOver 環境中出現 frame generation 類功能，仍要視為轉譯或替代路徑，不是 NVIDIA RTX 40 / RTX 50 GPU 上的原生 DLSS Frame Generation 或 Multi Frame Generation。

### XeSS 在任何 GPU 上都等於 DLSS？

不等於。XeSS 有跨廠商實作，但 Intel 官方仍有 Intel GPU 最佳化路徑與 API / backend 條件。Apple Silicon + CrossOver 多了一層圖形 API 轉譯，所以更要用實測判斷。

### TSR 一定畫質最好？

不一定。TSR 的優勢是相容性和引擎整合，不代表每款遊戲都比 DLSS / XeSS / FSR 清楚。某些遊戲的 TSR 可能比較自然，某些遊戲則可能有模糊、拖影或銳化不足。

### 要不要永遠固定 D3DMetal？

不一定。D3DMetal 支援 DirectX 11 / 12，通常是現代遊戲的重要選項；DXMT 則是 Metal-based Direct3D 11 實作，有些 D3D11 遊戲會更適合 DXMT。最實用的做法是先用 Auto，再針對單一遊戲測 D3DMetal、DXMT 與遊戲內升頻設定。

## 參考資料

- [CodeWeavers: Advanced Settings in CrossOver Mac 26](https://support.codeweavers.com/en_US/advanced-settings-in-crossover-mac-26)
- [Apple Developer: Applying temporal antialiasing and upscaling using MetalFX](https://developer.apple.com/documentation/MetalFX/applying-temporal-antialiasing-and-upscaling-using-metalfx)
- [NVIDIA: DLSS Technology](https://www.nvidia.com/en-us/geforce/technologies/dlss/)
- [Intel: XeSS Super Resolution Developer Guide](https://www.intel.com/content/www/us/en/developer/articles/technical/xess-sr-developer-guide.html)
- [Epic Games: Temporal Super Resolution in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/temporal-super-resolution-in-unreal-engine)
- [How-To Geek: DLSS vs. XeSS vs. FSR](https://www.howtogeek.com/xess-vs-dlss-vs-fsr-upscaling-technology/)
- [CrossOver 中文官網：《燕云十六声》如何开启 DLSS 和帧生成](https://www.crossoverchina.com/faq/mac-plkdj.html)
