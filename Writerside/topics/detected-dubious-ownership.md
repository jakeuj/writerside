# detected dubious ownership

fatal: detected dubious ownership in repository at

![gtt-fatal.png](gtt-fatal.png){style="block"}

## 設定

```Shell
git config --global safe.directory *
```

## 備註

如果失敗可能要到全域設定檔中清除 [safe] 部分，再重新下一次命令

## 參照

[detected dubious ownership](https://stackoverflow.com/questions/73485958/how-to-correct-git-reporting-detected-dubious-ownership-in-repository-withou)
