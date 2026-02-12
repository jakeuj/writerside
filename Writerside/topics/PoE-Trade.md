# PoE Trade

自動點擊 PoE2 線上搜尋的 傳送 按鈕

## Tampermonkey

https://www.tampermonkey.net/

## Script

注意：@match 的 `Fate%20of%20the%20Vaal` 需根據實際搜尋的聯盟名稱修改

```javascript
// ==UserScript==
// @name         PoE2 Auto Click Trade Button
// @namespace    http://tampermonkey.net/
// @version      2025-09-16
// @description  自動點擊線上搜尋的 傳送 按鈕
// @author       JKiritoI
// @match        https://www.pathofexile.com/trade2/search/poe2/Fate%20of%20the%20Vaal/*/live
// @icon         https://www.google.com/s2/favicons?sz=64&domain=pathofexile.com
// @grant        none
// ==/UserScript==


(function() {
'use strict';

    function isClickable(btn) {
        return btn && !btn.disabled && !btn.classList.contains("disabled");
    }

    function clickFirstButton(root = document) {
        const btn = root.querySelector("button.btn.btn-xs.btn-default.direct-btn");
        if (isClickable(btn)) {
            console.log("點擊第一個按鈕:", btn);
            btn.click();
        }
    }

    function setupObserver(tradeList) {
        console.log("找到 trade 列表，開始監聽");
        // 初始掃描一次
        clickFirstButton(tradeList);

        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) {
                        // 只點擊第一個可點的新按鈕
                        clickFirstButton(node);
                    }
                });
            });
        });

        observer.observe(tradeList, { childList: true, subtree: true });
    }

    function waitForTradeList() {
        const tradeList = document.querySelector("#trade .results");
        if (tradeList) {
            setupObserver(tradeList);
        } else {
            console.log("還沒找到 trade 列表，繼續等待...");
            setTimeout(waitForTradeList, 1000);
        }
    }

    waitForTradeList();
})(); 
```
