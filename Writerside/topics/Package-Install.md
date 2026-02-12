# Package Install

Start typing here...

## 遠端無法安裝套件

```
/usr/bin/python3.10
/home/x/.cache/JetBrains/RemoteDev/dist/pycharm/plugins/python/helpers/packaging_tool.py install
py-cpuinfo
```

```
Error: Traceback (most recent call last):
  File "/home/x/.cache/JetBrains/RemoteDev/dist/pycharm/plugins/python/helpers/packaging_tool.py", line 85, in run_pip
    runpy.run_module(module_name, run_name='__main__', alter_sys=True)
  File "/usr/lib/python3.10/runpy.py", line 220, in run_module
    mod_name, mod_spec, code = _get_module_details(mod_name)
  File "/usr/lib/python3.10/runpy.py", line 140, in _get_module_details
    raise error("No module named %s" % mod_name)
ImportError: No module named pip
```

## 安裝 pip

```Bash
sudo apt install python3-pip
```
