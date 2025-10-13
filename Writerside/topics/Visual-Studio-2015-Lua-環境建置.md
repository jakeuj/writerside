# Visual Studio 2015 Lua 環境建置

> **原文發布日期:** 2016-03-21
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2016/03/21/lua
> **標籤:** 無

---

Visual Studio 2015 Lua 環境建置

2016/05/10 修正內文

第13步驟 由 "選擇資料夾" 改為 "類別庫名稱"

新增紅色重點並附上範例專案檔案(VS 2016 Project)

環境：Visual Studio 2015 UPDATE 1 & Lua 5.3.2 (.Net 4.6.1)

1.下載Lua：[Source](http://www.lua.org/download.html)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555440_83912.png)

2.解壓縮該壓縮檔：D:\lua-5.3.2

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555449_76311.png)

3.開啟Visual Studio 2015→新增專案→Visual C++→Win32→Win32 主控台應用程式→Lua5.3→確定→下一步→靜態程式庫→取消勾選"先行編譯標頭檔"→完成

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555486_23457.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555486_71823.png)

4.方案總管→標頭檔→加入→現有項目→D:\lua-5.3.2\src→選取全部 \*.h 檔案(所有C/C++ Header檔案，可先依檔案類型排序後方便選擇)→加入

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555520_35931.png)

上圖右邊有誤：應該是要選取"新增項目"下方的"現有項目"

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555528_04548.png)

5.方案總管→原始程式檔→加入→現有項目→D:\lua-5.3.2\src→選取全部 \*.c 檔案(所有C/C++ Header檔案，可先依檔案類型排序後方便選擇)→取消選擇 lua.c與luac.c兩個檔案→加入

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555544_10871.png)

6.專案→屬性→C/C++→一般→其他 Include 目錄→編輯→加入目錄"D:\lua-5.3.2\src"→選擇資料夾→確定

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555578_27266.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555578_3986.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555579_24148.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555579_4915.png)

7.專案→屬性→C/C++→進階→編譯成→編輯→編譯成 C 程式碼(/TC)→確定

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555602_0563.png)

8.開始建置(Release編譯)→產生lib檔案→位於"方案"目錄下的Release資料夾(非"專案"目錄下的Release資料夾)

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555620_53776.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555620_20965.png)

(D:\User\Documents\visual studio 2015\Projects\Lua5.3\Release\Lua5.3.lib)

9.將編譯完成所產生的lib檔案(Lua5.3.lib)複製到Lua Source目錄D:\lua-5.3.2

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555631_74659.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458555638_80252.png)

10.開啟Visual Studio 2015(或於上面原方案按右鍵點選加入)→新增專案→Visual C++→Win32→Win32 主控台應用程式→LuaTest→確定→下一步→完成

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458613075_53495.png)

11.同上述第6步驟：專案→屬性→C/C++→一般→其他 Include 目錄→編輯→加入目錄"D:\lua-5.3.2\src"→選擇資料夾→確定

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458613814_61591.png)

12.專案→屬性→連接器→一般→其他程式庫目錄→編輯→加入目錄"D:\lua-5.3.2"→選擇資料夾→確定

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458613105_77563.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458613110_94112.png)![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458613131_11536.png)

13.專案→屬性→連接器→輸入→其他相依性→編輯→加入類別庫名稱"Lua5.3.lib"→確定

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458615457_4052.png)

14.原始程式檔→加入→新增項目→C++ 檔(.cpp)→"main.lua"(注意是lua不是原本的.cpp)→新增

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458613140_57805.png)

15.修改main.lua程式碼內容 print("Hello World.");

```

print("Hello World.");
```

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458615471_03996.png)

16.修改LuaTest.cpp程式碼內容

```

#include "stdafx.h"
#include <iostream>
using namespace std;
#include <lua.hpp>

int main()
{
	lua_State *l = luaL_newstate();
	luaL_openlibs(l);
	luaL_dofile(l, "main.lua");
	lua_close(l);
	system("pause");
    return 0;
}
```

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458615478_86804.png)

17.編譯LuaTest專案並執行後顯示完成結果

![](https://dotblogsfile.blob.core.windows.net/user/jakeuj/293febdc-4e32-48b4-915f-33eb58861fe4/1458616577_29333.png)

參照：[Lua學習筆記](http://www.byjth.com/lua/33.html)

範例檔案：[下載位置](https://mega.nz/#!vFA1lIYZ!8YP51emAZH5luIVQMtyrTSrIcVsE18Zrmceu8QzxzIQ) (懶人包：全部解壓縮到D即可，內含Lua Source)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* VisualStudio
* Lua

* 回首頁

---

*本文章從點部落遷移至 Writerside*
