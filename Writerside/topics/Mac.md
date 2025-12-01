# Mac

記錄台版嘗試跑 Macbook M4 的過程

## XIV ON MAC
[XIV ON MAC 官網](https://www.xivmac.com/)
[Github XIV-on-Mac](https://github.com/marzent/XIV-on-Mac)
[巴哈自制 XIV ON MAC](https://forum.gamer.com.tw/Co.php?bsn=17608&sn=110287)
[巴哈可運行 CorssOver](https://forum.gamer.com.tw/C.php?bsn=17608&snA=25995)

## Git Clone 子模組
直接 Clone 這個專案會遇到錯誤
`XIV-on-Mac/XIV on Mac/XIVLauncher.NativeAOT/XIVLauncher.NativeAOT.dylib : No such file or directory`
這是因為這個專案使用了 Git 子模組來管理依賴項目。如果你直接克隆這個專案而沒有初始化子模組，會導致缺少必要的檔案。
因此，建議使用以下指令來克隆這個專案，並同時初始化子模組：
```bash
git clone --recurse-submodules https://github.com/marzent/XIV-on-Mac.git
```
如果你已經下載了這個專案，但沒有使用 `--recurse-submodules` 參數，你可以使用以下指令來更新子模組：
```bash
git submodule update --init --recursive
```

## 安裝 Wine
直接使用 XCode 會遇到錯誤
`XIV-on-Mac/XIV on Mac/wine lstat(XIV-on-Mac/XIV on Mac/wine): No such file or directory (2)`
因此需要安裝 Wine 來執行 Windows 應用程式。
[Github winecx](https://github.com/marzent/winecx)

```bash
./configure
make
```

按照說明安裝又會遇到錯誤
```
configure: error: Your bison version is too old. Please install bison version 3.0 or newer.
make: *** No targets specified and no makefile found.  Stop.
```

因此需要先安裝 Bison
```bash
brew install bison
```
並將新版 bison 加入環境變數（建議加到 ~/.zshrc 或 ~/.bash_profile）：
```bash
export PATH="/opt/homebrew/opt/bison/bin:$PATH"
export LDFLAGS="-L/opt/homebrew/opt/bison/lib"
export CPPFLAGS="-I/opt/homebrew/opt/bison/include"
```

再次執行安裝會遇到錯誤
```
onfigure: error: PE cross-compilation is required for aarch64, please install clang/llvm-dlltool/lld, or llvm-mingw.
make: *** No targets specified and no makefile found.  Stop.
```

## 安裝 llvm
[llvm-mingw](https://github.com/mstorsjo/llvm-mingw)

```bash
git clone https://github.com/mstorsjo/llvm-mingw
cd llvm-mingw
```

先手動建立資料夾
`llvm-project/llvm/build/include/lldb`
否則會遇到錯誤
`FileNotFoundError: [Errno 2] No such file or directory: 'llvm-project/llvm/build/include/lldb/lldb-defines.h'`

```bash
./build-all.sh ./llvm-mingw-install
```

然後會遇到錯誤
`./strip-llvm.sh: line 129: cd: share: No such file or directory`

