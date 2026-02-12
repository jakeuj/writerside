# requirements

紀錄一下安裝套件的方法。

## 手動建立

requirements.txt 是一個紀錄專案所需套件的檔案，可以透過以下指令建立：

```
requests==2.25.1
numpy==1.24.3
matplotlib==3.7.1
```

## 自動建立

透過 `pip freeze` 指令可以自動建立 requirements.txt：

```Bash
pip freeze > requirements.txt
```

## 安裝套件

透過 `pip install -r requirements.txt` 可以安裝所有套件。

## 更新套件

透過 `pip install --upgrade -r requirements.txt` 可以更新所有套件。

## 移除套件

透過 `pip uninstall -r requirements.txt` 可以移除所有套件。
