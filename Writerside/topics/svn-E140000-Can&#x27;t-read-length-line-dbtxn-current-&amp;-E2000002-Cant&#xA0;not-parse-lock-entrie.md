# svn: E140000: Can&#x27;t read length line: db/txn-current &amp; E2000002: Cant&#xA0;not parse lock / entries hashfile &#x27;{0}&#x27;

> **原文發布日期:** 2019-01-09
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/01/09/txn-current
> **標籤:** 無

---

svn: E140000: Can't read length line: db/txn-current

svn : E2000002: Cant not parse lock / entries hashfile '{0}'

> 在commit文件時，svn服務器被強行關閉了，導致版本信息文件寫入不成功，重啟後讀取信息就不正確了！

比如送交版本時磁碟空間剛好滿了導致svn停止運作(查了一下好像在某版本已經針對此狀況做修復)

這時 db/txn-current 這個檔案沒有被正確寫入資料，導致後續commit會報錯

在修復之前先弄清楚這檔案的作用會比較知道該如何處理

其實查看該目錄會找到另一個87分像的檔案 => db/current

這檔案打開會發現裡頭其實是目前的版本號

然後這路徑下有一個資料夾 db/revprops

裡頭會發現有若干資料夾而且名稱都是數字 db/revprops/0,1,2,3...

再點進去其實就是版本號 0001~0999 ,1000~1999

所以結構是

db/revprops/0/0001 , db/revprops/0/0002, ... , db/revprops/0/0999

db/revprops/1/1000 , db/revprops/1/0001, ... , db/revprops/1/1999

從中可以發現格式其實是 db/revprops/{0}/{1}

其中{1}代表版本號也就是 db/current 這檔案中應該出現的值

current應該蠻好理解是目前的版本號，也就是最大的版號

然後回到第一個 {0} 這個資料夾名稱其實是版號的千位數

他會把 1xxx 版號都放進 1這個資料夾, 2xxx版號放進2這個資料夾

這邊這個 {0} 也就是 db/txn-current 這裡面應該記錄的，同樣是當前值也就是最大值

到這邊我們應該可以知道處理流程是找到 db/revprops/ 內的最大號碼 寫入到 db/txn-current

然後找到 db/revprops/最大號碼/ 內的最大號碼(也就是版號) 寫入到 db/current

就可以修復這兩個檔案

參照：https://blog.csdn.net/lemonay/article/details/14160619

---

> The "txn-current" file is a file with a single line of text that contains only a base-36 number. The current value will be used in the next transaction name, along with the revision number the transaction is based on. This sequence number ensures that transaction names are not reused, even if the transaction is aborted and a new transaction based on the same revision is begun.

這篇是說該檔案會被用來當作產生交易識別碼，為保證唯一性會在每次交易時自動進為，格式是英數字構成的36進位

所以嘛定一個相對大的數字進去不要重複好像就可以繼續用了的樣子...

參照：http://svn.apache.org/repos/asf/subversion/trunk/subversion/libsvn\_fs\_fs/structure

---

> E2000002: Cant not parse lock / entries hashfile '{0}'

承上，磁碟問題可能連帶lock資料異常，導致原本鎖定檔案處於鎖定又無法解鎖的窘境

目前找到的方法是把 db/locks 內的資料夾全部刪除破開鎖定

linux 下先切到 db/locks

## [**千萬記得先切到該目錄再刪除...**]

然後下刪除指令 rm -rf \*

參照：http://mahingupta.com/svn-can-not-parse-lock-entries-hashfile/

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [SVN](/jakeuj/Tags?qq=SVN)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
