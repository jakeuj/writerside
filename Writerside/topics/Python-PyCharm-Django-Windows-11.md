# Python PyCharm Django Windows 11

> **原文發布日期:** 2023-05-25
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2023/05/25/Python-PyCharm
> **標籤:** 無

---

奇怪的荊棘之路展開

## 步驟

1. PyCharm 建立新專案
2. pip install Django==4.0.3
3. PS> `django-admin startproject TestProject`
4. 用 PyCharm 導覽到 requirements.txt 點安裝全部套件
5. PS> `python manage.py runserver`
6. PS> `python manage.py createsuperuser`

徵狀

```
Fatal Python error: init_stdio_encoding: failed to get the Python codec name of the stdio encoding
Python runtime state: core initialized
LookupError: unknown encoding: x-windows-950
```

結論

bin\pycharm64.exe.vmoptions

`-Dfile.encoding=UTF-8`

參照

[2022.2.3: Fatal Python error: init\_stdio\_encoding: failed to get the Python codec name of the stdio encoding - LookupError: unknown encoding : PY-56723 (jetbrains.com)](https://youtrack.jetbrains.com/issue/PY-56723/2022.2.3-Fatal-Python-error-initstdioencoding-failed-to-get-the-Python-codec-name-of-the-stdio-encoding-LookupError-unknown)

[Fatal Python error: Py\_Initialize: can't initialize sys standard streams, LookupError: unknown encoding: x-windows-950 : PY-15921 (jetbrains.com)](https://youtrack.jetbrains.com/issue/PY-15921)

徵狀

ModuleNotFoundError: No module named 'xxxxxxxxxx'

結論

pip install xxxxxxxxxx

說明

專案沒有 requirements.txt 或 requirements.txt 遺漏該模組 => 只好自己手動安裝

參照

[MH の 資源筆記: [Python] 使用XlsxWriter (mh-resource.blogspot.com)](https://mh-resource.blogspot.com/2017/10/python-xlsxwriter.html)

徵狀

`FileNotFoundError: [Errno 2] No such file or directory:`

說明

確認專案內該路徑有指定檔案，但實際執行卻找不到檔案

執行 python 時，需先行切到專案目錄下，對齊相對路徑

結論

原為

`python D:\repos\test\manage.py runserver 0.0.0.0:80`

改為

```
cd 'D:\repos\test\'
python manage.py runserver 0.0.0.0:80
```

備註

查詢當前執行目錄 `print(os.getcwd())`

## 資料表大小寫不一致

使用 root 登錄，修改 /etc/my.cnf 檔，在 [mysqld] 節點下，加入一行。 `lower_case_table_names=1`

P.S. 這動作要在初始化資料庫之前做，否則會報錯誤…

備註

你需要重新啟動 MySQL 數據目錄。

根據 https://dev.mysql.com/doc/refman/8.0/en/identifier-case-sensitivity.html

lower\_case\_table\_names 只能在初始化服務器時配置。

如果你運行的是 Ubuntu，你可以使用這個腳本

https://github.com/igrmk/ubuntu-reinit-mysql。

請注意，你的數據將被銷毀！

因此，在運行它之前，請創建一個備份！

參照

[MySQL 8.0 版本 lower\_case\_table\_names 参数踩坑记 - 墨天轮 (modb.pro)](https://www.modb.pro/db/48280)

### IDE 記憶體不足

[Increase the memory heap of the IDE | PyCharm Documentation (jetbrains.com)](https://www.jetbrains.com/help/pycharm/increasing-memory-heap.html)

### WSL MySQL 8

[Win10 WSL下 Ubuntu20.04 安装与卸载 Mysql 8.0-CSDN博客](https://blog.csdn.net/ychen219/article/details/123711116)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* PyCharm

* 回首頁

---

*本文章從點部落遷移至 Writerside*
