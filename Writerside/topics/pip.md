# pip

Start typing here...

## Install pip

```bash
sudo apt update
sudo apt install python3-pip
```

如果您的 Ubuntu 系統已經安裝了 Python3,但缺少 pip 工具,您可以按照以下步驟來安裝 pip:

1. 首先,更新 apt 套件索引:

```
sudo apt update
```

1. 安裝 pip 套件:

```
sudo apt install python3-pip
```

這將安裝最新版本的 pip3 (適用於 Python 3)。

1. 驗證 pip3 是否正確安裝:

```
pip3 --version
```

您應該會看到類似這樣的輸出,顯示 pip 的版本:

```
pip 21.2.4 from /usr/lib/python3/dist-packages/pip (python 3.8)
```

1. 如果您想讓所有使用者都能使用 pip3 命令,而不只是當前使用者,您可以將 pip3 的可執行檔案路徑加入到系統路徑中。首先,找到 pip3 路徑:

```
which pip3
```

這將顯示 pip3 可執行檔案的路徑,通常是 `/usr/bin/pip3`

1. 接著使用 nano 或其他文字編輯器編輯 /etc/bash.bashrc 檔案:

```
sudo nano /etc/bash.bashrc
```

在檔案末尾加入下列行:

```
export PATH=$PATH:/usr/bin/pip3
```

這將把 /usr/bin/pip3 加入系統路徑中。

1. 儲存並退出編輯器。重新載入 bash 設定:

```
source /etc/bash.bashrc
```

現在所有使用者應該都可以直接執行 `pip3` 指令來管理 Python3 套件了。

如果您需要為特定使用者安裝套件,可以使用 `pip3 install --user` 命令,而不需要 root 權限。對於系統級別的安裝,您仍然需要使用 `sudo pip3 install`。
