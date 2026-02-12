# Python venv

如何使用 Python 的虚拟环境

## 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv myenv
```

## 激活虚拟环境

```bash
# 激活虚拟环境
source myenv/bin/activate
```

## 安装依赖

```bash
# 安装依赖
pip install -r requirements.txt
```

## 退出虚拟环境

```bash
# 退出虚拟环境
deactivate
```

## 删除虚拟环境

```bash
# 删除虚拟环境
rm -rf myenv
```

## Ubuntu 22.04 安裝 Python 3

正常安裝 Ubuntu 會內建 Python 3.10.12，但沒有 pip3 和 venv：

```bash
sudo apt install python3-pip python3-venv
```

## python3 與 python 的問題

沒有啟動虛擬環境時，需要輸入 python3 才能正常呼叫。

```Bash
# 虛擬環境啟動前
$ python -V
Command 'python' not found, did you mean:
  command 'python3' from deb python3
  command 'python' from deb python-is-python3
$ python3 -V
Python 3.10.12
$ which python3
/usr/bin/python3
```

如果想要讓 python 與 python3 指向同一個版本，
可以安裝 python-is-python3：

```Bash
sudo apt install python-is-python3
```

這種方法更簡單而且官方推薦，適合不熟悉符號連結操作的使用者。
也可以手動建立連結：

```Bash
$ sudo ln -s /usr/bin/python3 /usr/bin/python
$ python -V
Python 3.10.12
```

安裝 pip3 時，會同時將 pip 與 pip3 連結到 python3：

```Bash
# 虛擬環境啟動前
$ pip -V
pip 22.0.2 from /usr/lib/python3/dist-packages/pip (python 3.10)
$ pip3 -V
pip 22.0.2 from /usr/lib/python3/dist-packages/pip (python 3.10)
```

## 虛擬環境啟動後

當啟動虛擬環境時，python, python3, pip, pip3 就會指向虛擬環境的版本。

```Bash
# 啟動虛擬環境
$ source ~/myenv/bin/activate
# 虛擬環境啟動後
$ which python
/home/jakeuj/myenv/bin/python
$ which python3
/home/jakeuj/myenv/bin/python
$ pip -V
pip 22.0.2 from /home/jakeuj/myenv/lib/python3.10/site-packages/pip (python 3.10)
$ pip3 -V
pip 22.0.2 from /home/jakeuj/myenv/lib/python3.10/site-packages/pip (python 3.10)
```

## REF

[Python venv](https://docs.python.org/3/library/venv.html)
