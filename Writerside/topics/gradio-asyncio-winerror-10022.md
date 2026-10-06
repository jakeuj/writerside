# Gradio 在 Windows 反覆出現 WinError 10022 的原因與修正

<web-summary>在 Windows 用 Python 3.10 執行 Gradio（例如 FramePack）時，console 反覆出現 _call_connection_lost 的 OSError WinError 10022；這是 asyncio Proactor 在連線已斷開後呼叫 shutdown 失敗，可以用 sitecustomize.py 只包住這個呼叫來修正。</web-summary>

這段錯誤不影響生成結果，但它不只是洗版：例外會讓後面的 `socket.close()` 被跳過。最乾淨的修法是在該 Python 的 `site-packages` 放一個 `sitecustomize.py`，只對失敗的 `shutdown()` 加上例外處理；不必修改 Gradio 或應用程式本身的程式碼。

<tldr>
<p>觸發時機：每次 Gradio 啟動時，以及瀏覽器連線中斷時。</p>
<p>修正：把下方的 <code>sitecustomize.py</code> 放進 <code>Lib\site-packages\</code>，重新啟動應用程式。</p>
<p>確認：<code>_call_connection_lost.__module__</code> 應顯示 <code>sitecustomize</code>。</p>
</tldr>

## 症狀 {#symptoms}

Gradio 啟動時，以及使用過程中，console 出現：

```text
Exception in callback _ProactorBasePipeTransport._call_connection_lost(None)
handle: <Handle _ProactorBasePipeTransport._call_connection_lost(None)>
Traceback (most recent call last):
  File "asyncio\events.py", line 80, in _run
  File "asyncio\proactor_events.py", line 162, in _call_connection_lost
OSError: [WinError 10022] 提供了一個不正確的引數。
```

英文版 Windows 的訊息是 `An invalid argument was supplied`。

用最小的 Gradio app（Python 3.10.6、gradio 5.23.0、uvicorn 0.27.0.post1）即可重現：還沒開瀏覽器，啟動時就會出現一次。這是因為 Gradio 啟動時會對自己的網址發一次 HTTP 請求來確認 server 已就緒，該連線關閉時就觸發了這個錯誤。使用過程中，瀏覽器連線中斷時（例如重新整理或關閉分頁）也可能再次出現。

## 根本原因 {#root-cause}

錯誤來自 Windows 預設的 `ProactorEventLoop`。以下是 CPython 3.10.6 `Lib/asyncio/proactor_events.py` 的這個方法，第 162 行就是 `shutdown()`：

```python
def _call_connection_lost(self, exc):
    try:
        self._protocol.connection_lost(exc)
    finally:
        if hasattr(self._sock, 'shutdown') and self._sock.fileno() != -1:
            self._sock.shutdown(socket.SHUT_RDWR)  # line 162
        self._sock.close()
        self._sock = None
        server = self._server
        if server is not None:
            server._detach()
            self._server = None
```

server 正常關閉連線時（traceback 中的 `(None)` 代表不是因為錯誤而關閉），如果另一端已經先斷線，`shutdown()` 就會丟出 `WinError 10022`。例外發生在 `finally` 裡，所以後面的 `close()` 與 `server._detach()` 都不會執行，socket 只能等 garbage collection 回收。

## 用 sitecustomize.py 修正 {#sitecustomize-fix}

Python 啟動時會自動 import `sys.path` 上的 `sitecustomize` 模組。把修正放在這裡有兩個好處：不必修改 Gradio 或應用程式的程式碼；應用程式用 `git pull` 或 `git reset --hard` 更新時，修正也不會被洗掉。

內容是 3.10.6 原本的方法，只對 `shutdown()` 加上 `try/except`，後續的清理一定會完成：

```python
# Silence asyncio Proactor WinError 10022 in _call_connection_lost (Python 3.10, Windows).
import sys

if sys.platform == 'win32' and sys.version_info[:2] == (3, 10):
    import socket
    from asyncio import proactor_events

    def _call_connection_lost(self, exc):
        try:
            self._protocol.connection_lost(exc)
        finally:
            if hasattr(self._sock, 'shutdown') and self._sock.fileno() != -1:
                try:
                    self._sock.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass  # peer already gone (WinError 10022 / 10054)
            self._sock.close()
            self._sock = None
            server = self._server
            if server is not None:
                server._detach()
                self._server = None

    proactor_events._ProactorBasePipeTransport._call_connection_lost = _call_connection_lost
```

存成執行該應用程式所用 Python 的 `Lib\site-packages\sitecustomize.py`。以 FramePack Windows 一鍵包為例，路徑是 `system\python\Lib\site-packages\sitecustomize.py`。

- 放之前先確認該目錄沒有既有的 `sitecustomize.py`；如果有，把內容合併進去，不要直接覆蓋。
- 版本判斷限定 Python 3.10，因為方法內容是照 3.10.6 原始碼寫的。其他版本請先核對該版本的原始碼再調整。
- 已在執行的程式不會套用修正，要重新啟動。

其他做法的取捨：

- 改用 `WindowsSelectorEventLoopPolicy` 也能避開這段程式碼，但會改變整個 event loop 的行為，例如不支援 subprocess、socket 數量有上限，影響範圍太大。
- 只用 logging filter 隱藏訊息，socket 仍然不會被關閉。

## 驗證 {#verify}

確認修正已經載入（`$py` 換成應用程式使用的 `python.exe`）：

```powershell
& $py -c "from asyncio import proactor_events as p; print(p._ProactorBasePipeTransport._call_connection_lost.__module__)"
```

輸出 `sitecustomize` 代表已生效；輸出 `asyncio.proactor_events` 代表沒有載入。

用同一個最小 Gradio app 實測前後差異：

| 情境 | 修正前 | 修正後 |
|------|--------|--------|
| 啟動 | 出現 1 次 `WinError 10022` | 0 次 |
| 點擊按鈕、重新整理 2 次、關閉分頁 | 未單獨測試 | 0 次 |

`sitecustomize` 會讓每次啟動 Python 多 import 一次 `asyncio`，實測約多 36 ms；Gradio 應用程式本來就會載入 `asyncio`，所以幾乎沒有額外成本。要還原時刪除 `sitecustomize.py` 即可。

## 參考資料

- [CPython 3.10.6 Lib/asyncio/proactor_events.py](https://github.com/python/cpython/blob/v3.10.6/Lib/asyncio/proactor_events.py)
- [Python site 模組：sitecustomize](https://docs.python.org/3.10/library/site.html)
- [FramePack Windows 一鍵包支援 RTX 5090：升級 PyTorch cu128 與 SageAttention](framepack-rtx-5090-windows.md)
