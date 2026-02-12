# PyInstaller

將 python 程式打包成執行檔的工具。
如果要打包成 Linux 的執行檔，就需要在 Linux 中打包。
Windows 上可以使用 WSL 來打包 Linux。

## 安裝

[安裝說明](https://pyinstaller.org/en/stable/#quickstart)

```bash
pip install -U pyinstaller
```

- 其中 -u 是更新到最新版本。

## requirements.txt

需先安裝所需套件後再打包，我是先切到虛擬環境後安裝套件，然後再打包。

## 使用

```bash
pyinstaller ./src/main.py 
--onefile 
--specpath . 
--paths "/mnt/d/repos/MyProject/src" 
--add-data "src/a/b/config/db.ini:a/b/config" 
--add-data "src/a/b/config/*.json:a/b/config"
```

- `--onefile` : 打包成單一檔案
- `--specpath .` : 將此次部署參數儲存至指定位置，以此為例會產生 main.spec 檔案
- `--paths` : 指定 python 檔案的位置，如果起始檔不在專案根目錄，就需要指定位置，否則 import 會找不到檔案
- `--add-data` : 指定要加入的非程式碼檔案
  - 例如：*.json,*.ini 等等。
  - 格式：`"來源檔案:輸出檔案"`

這會建立 main.spec 檔案，類似 publish 組態設定檔，之後可以直接用此設定檔進行打包，省得每次重新打參數。

```bash
pyinstaller main.spec
```

## 注意事項

因為打包時會把程式碼變成一個檔，所以原本專案的資料夾結構會消失，如果有需要讀取檔案的話，就需要注意檔案的位置。

例如：如果原本是這樣的結構：

src/a/b/config.json
src/a/b/service/test/config.py

config.py

```Python
base_path = os.path.dirname(os.path.abspath(__file__))
config = os.path.join(base_path, '../../config.json')
```

這會引發錯誤，因為打包後的結構，並不會有 service/test 的資料夾(config.py 已經變成單一執行檔)

所以要改成這樣：

config.py

```Python
# 检查是否在打包后的环境中运行
if hasattr(sys, '_MEIPASS'):
    base_path = os.path.join(sys._MEIPASS, 'a/b')
else:
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

config = os.path.join(base_path, 'config.json')
```

這樣就可以正確讀取到檔案了。

## 執行

打包後會產生一個 dist 資料夾，裡面就是打包好的檔案。

```bash
./dist/main
```

## 參考

- [PyInstaller](https://pyinstaller.org/)
