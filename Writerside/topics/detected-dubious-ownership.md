# detected dubious ownership

fatal: detected dubious ownership in repository at

![gtt-fatal.png](gtt-fatal.png)

## 設定

```Shell
git config --global safe.directory *
```

## 備註
如果失敗可能要到全域設定檔中清除 [safe] 部分，再重新下一次命令