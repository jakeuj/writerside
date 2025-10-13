# Redis Server 架設心得筆記

> **原文發布日期:** 2015-12-24
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2015/12/24/Redis
> **標籤:** 無

---

Redis Server 架設心得筆記

結論

```
docker run --name some-redis -d redis
```

[redis - Official Image | Docker Hub](https://hub.docker.com/_/redis)

以下是老文章

1.事前準備

準備一台Linux系統的Server，記憶體盡可能大一點

因為作為Cache Server主要資料都是存放於Ram

OS這邊我是使用CentOS作為範例

2.Linux 系統更新

為提升系統安全性所以我這邊先把剛拿到的乾淨系統做一次升級

為了使更新下載更順利，因此我這邊先把國家參數(cc=tw)加進更新設定檔

設定檔路徑為 "/etc/yum.repos.d/CentOS-Base.repo"

使用vi開始該檔後找到前兩個 "mirrorlist"

用 i 插入文字來附加國家參數 "&cc=tw"

具體來說大概長成下面這樣

mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=os&cc=tw
mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=updates&cc=tw

更改完後開始跑更新，輸入指令 "yum update"，過程中案"y"確認執行更新作業，跑完後即完成。

3.GCC 安裝

因為Redis需要編譯後才能執行，而乾淨版本的Linux並沒有自帶C語言編譯器，所以需要自己裝GCC編譯器。

直接下指令 "yum -y install gcc" 下載安裝完成後即可。

參照：http://bbs.chinaunix.net/thread-3608283-1-1.html

4.Redis 安裝

根據官方說明，我們需要下載Redis原始檔，解壓縮，切換至該目錄，最後進行編譯。

指令如下：

wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make

參照：http://redis.io/topics/quickstart

4.快速執行

官方這邊建議將主程式複製到/usr/local/bin/

如此一來可以直接無視現在的目錄，直接執行redis的server與client

指令如下：
sudo cp src/redis-server /usr/local/bin/
sudo cp src/redis-cli /usr/local/bin/

結果是無視所在目錄，只要打"redis-server"就可以啟動server，

同上，打"redis-cli"就可以啟動客戶端來對server下指令。

5.修改連線數並接受大型記憶體需求

linux預設的連線數不到128個conn

因為redis作為cache server 需要接收大量連線要求

因此需要更改系統預設連線數設定，這邊先設為2048

設定檔路徑為 "/etc/sysctl.conf"
依樣使用vi開啟後於末端用"o"插入下面內容

vm.overcommit\_memory = 1

接續上行設定以下內容，以接受大型記憶體需求的狀況

net.core.somaxconn = 2048

然後 :wq 儲存後離開

接著於終端輸入以下指令來讓設定即刻生效

sysctl -p

sysctl vm.overcommit\_memory=1

或是重啟系統

6.背景執行

最後用預設設定檔來開啟redis

輸入以下指令即可以背景執行

redis-server /etc/redis/redis.conf &

7.前台執行

fg可以將redis拿回前端顯示

之後要切換回後台執行可以輸入以下指令

ctrl+z -> bg %1

8.測試

執行 redis-cli ping

成功好像會接收到 PONG

9.結束

以上為不熟linux也不熟redis的我做的筆記

可能有錯誤還有待改進的地方之後再補

==============================

翻譯中的Redis管理者須知

**Redis管理**

此頁包含與管理Redis執行個體相關的主題。每個主題是自我 FAQ 的形式。將在將來創建新主題。

Redis安裝提示

·        我們建議使用**Linux 作業系統**部署Redis。雖然Redis還是會在 OS X 、 FreeBSD 和 OpenBSD 系統上進行測試。然而我們壓力測試和大多數生產部署工作的地方主要還是在 Linux。

·        請務必設定 Linux 核心，將”**過量使用記憶體”(**overcommit\_memory**)設定為 1**。
添加 vm.overcommit\_memory = 1 到/etc/sysctl.conf ，然後重新開機或運行命令 sysctl vm.overcommit\_memory=1 為此立即生效。

·        一定要禁用 Linux 內核功能*透明大頁面(transparent huge pages)*，它將以消極的方式影響較大的記憶體使用方式和延遲。這通過下面的命令 ︰ echo never > /sys/kernel/mm/transparent\_hugepage/enabled.

·        確保**設定一些Swap (虛擬記憶體)**在您的系統 （我們建議將Swap設定跟記憶體大小相同）。如果 Linux 沒有Swap，你Redis的執行個體會不小心消耗太多記憶體，記憶體不足將造成Redis程序崩潰或 Linux 內核 OOM時會殺掉Redis程序。

·        明確地設置maxmemory選項限制在您的執行個體，以確保當記憶體使用量達到系統上限時，該執行個體將會報告錯誤而非直接讓程式發生錯誤。

·        如果你在非常大量寫入的應用中使用Redis，在保存RDB 檔到硬碟上或重寫 AOF 日誌的期間，**Redis可能會使用相當於一般記憶體的 2 倍使用量**。額外記憶體使用量是與儲存的過程中記憶體頁數被改寫的數量成正比，所以經常與在這段時間的鍵值 （或聚合類型專案） 的數目成正比。請確保相應大小的記憶體。

·       當運行在 daemontools(管理unix服務的工具)的時候使用daemonize no。

·        如果你使用複製(Replication)，即使你已經持久禁用，Redis將還是需要執行 RDB 保存，除非你使用的是新的目前還在實驗階段的無須磁碟的複製功能。

·        如果您在使用複製(Replication)，請確保你的master持久性啟用，或它不會在崩潰時自動重新開機︰ Slaves會儘量精確複製master，所以如果master重新開機時資料清空，Slaves也會把資料清除。

·        預設情況下Redis的不需要**任何身份驗證和監聽所有的網路介面**。這是一個大的安全問題，如果你讓Redis暴露在網際網路或其他攻擊者可以接觸到它的地方。例如，見[這種攻擊](https://ssl.translatoruser.net/bv.aspx?from=en&to=zh-CHT&a=http%3A%2F%2Fantirez.com%2Fnews%2F96)，看到它是多麼危險。請檢查我們的[安全頁面](https://ssl.translatoruser.net/bv.aspx?from=en&to=zh-CHT&a=http%3A%2F%2Fredis.io%2Ftopics%2Fsecurity)和[快速啟動](https://ssl.translatoruser.net/bv.aspx?from=en&to=zh-CHT&a=http%3A%2F%2Fredis.io%2Ftopics%2Fquickstart)有關如何確保Redis的資訊。
{ignore-vars="true"}

在 EC2 上運行Redis

·        使用不基於 PV 實例 HVM 基於實例。

·        請勿使用舊實例家庭，例如 ︰ 與 HVM 使用 m3.medium，而不是 m1.medium，光伏系統。

·        Redis的持久性與**EC2 EBS 卷**的使用需要小心處理，因為有時 EBS 卷高延遲特性。

·        你可能想要嘗試新**盤複製**（目前實驗），如果你有問題，副系統與主系統進行同步時。

升級或重新開機一個Redis的實例，而無需停機

Redis的設計是一個執行時間非常長的過程，在您的伺服器。例如可以沒有任何重啟使用[配置設置命令](https://ssl.translatoruser.net/bv.aspx?from=en&to=zh-CHT&a=http%3A%2F%2Fredis.io%2Fcommands%2Fconfig-set)修改多個配置選項.
{ignore-vars="true"}

從Redis的 2.2 開始是甚至可能從 AOF 切換到 RDB 快照持久性或Redis的無需重新開機周圍的其他方式。檢查輸出配置得到 \* 命令的詳細資訊。

然而不時重新開機是強制性的例如為了升級Redis的過程到較新的版本，或者當您需要修改一些配置參數，它目前不支援的配置命令。

以下步驟提供了非常常用的方式，以避免任何停機時間。

·        作為一個副系統為你當前的Redis的實例設置您Redis的新實例。為此，你需要一個不同的伺服器或具有足夠的 RAM 來保持的Redis的同時運行兩個實例的伺服器。

·        如果您使用一台伺服器，請確保副系統開始在不同的埠比主實例，否則副系統不能夠在所有啟動。

·        等待複製初始同步完成 （檢查副系統日誌檔）。

·        請確保使用資訊有相同數量的鑰匙在主系統和副系統。檢查與Redis的 cli 的副系統工作以及你希望對你的命令作出答覆。

·        允許寫入到副系統使用**配置設置副系統唯讀不**

·        配置您的用戶端以使用新的實例 （即，副系統）。

·        一旦你確信主系統是不再接收任何查詢 （您可以檢查這與[監視器命令](https://ssl.translatoruser.net/bv.aspx?from=en&to=zh-CHT&a=http%3A%2F%2Fredis.io%2Fcommands%2Fmonitor)），選出的副系統使用**SLAVEOF 沒有人**命令和關閉你的主系統。
{ignore-vars="true"}

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Redis
* Server

* 回首頁

---

*本文章從點部落遷移至 Writerside*
