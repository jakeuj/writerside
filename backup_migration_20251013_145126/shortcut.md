# shortcut

Start typing here...

## 本地自定義快捷鍵

    Press <shortcut>Ctrl+/</shortcut> to commit.

### 輸出

Press <shortcut>Ctrl+/</shortcut> to commit.

### Ref

[shortcut](https://www.jetbrains.com/help/writerside/paragraphs.html#shortcut)

## 全局定義快捷鍵

建立 <path>keymap.xml</path> 檔案，同 `writerside.cfg` 所在目錄，並在其中定義快捷鍵。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<keymap id="my_keymap">
   <layouts>
      <layout name="Windows" platform="PC"/>
      <layout name="macOS" platform="MAC"/>
      <layout name="Linux" platform="PC"/>
   </layouts>
   <actions>
      <action id="$Copy">
         <description>Copy</description>
         <shortcut layout="Windows">Ctrl+C</shortcut>
         <shortcut layout="macOS">⌘ C</shortcut>
         <shortcut layout="Linux">Ctrl+C</shortcut>
      </action>
      <action id="$Paste">
         <description>Paste</description>
         <shortcut layout="Windows">Ctrl+V</shortcut>
         <shortcut layout="macOS">⌘ V</shortcut>
         <shortcut layout="Linux">Ctrl+V</shortcut>
      </action>
   </actions>
</keymap>
```

於 ` cfg/buildprofiles.xml` 中加入 `<shortcuts>` 來指定使用的快捷鍵。

```xml
<shortcuts>
    <src>keymap.xml</src>
    <layout name="Windows" display-name="Windows"/>
    <layout name="macOS" display-name="macOS"/>
</shortcuts>
```

最後就可以使用全域定義快捷

    Press <shortcut key="$Copy"/> to copy.

### 輸出

Press <shortcut key="$Copy"/> to copy.