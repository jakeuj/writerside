# PostgreSQL

Start typing here...

![postgresql.png](postgresql.png){style="block"}

## PostgreSQL

- 建立一個名為 `some-postgres` 的容器，並且將容器的 5432 port 對應到本機的 5432 port。

```Shell
docker run --name some-postgres 
    -e POSTGRES_PASSWORD=myPassword 
    -p 5432:5432 
    -d postgres
```

- 設定 root 使用者和密碼。

```Shell
docker run --name some-postgres 
    -e POSTGRES_USER=root 
    -e POSTGRES_PASSWORD=myPassword 
    -p 5432:5432 
    -d postgres
```

- 將資料庫儲存到本機的 C:\Postgres 資料夾。

```Shell
docker run --name some-postgres 
    -e POSTGRES_USER=root
    -e POSTGRES_PASSWORD=myPassword 
    -e PGDATA=/var/lib/postgresql/data/pgdata 
    -v C:\Postgres:/var/lib/postgresql/data 
    -p 5432:5432 
    -d postgres
```

目前測試如果將資料庫儲存到本機，重建 Container 時會遇到 SHA 加密問題。

開發階段可以先不將資料掛出來，已掛可以先把裡面資料砍掉

最終應該是有個加密憑證也要一起掛出來，保留當初憑證去解密？

![postgresql-rider.png](postgresql-rider.png){style="block"}

![rider-ps.png](rider-ps.png){style="block"}

![migration.png](migration.png){style="block"}

## ReFS

如果你將掛載本機路徑指定到 ReFS 格式的磁碟，可能會遇到以下錯誤：

    chmod: changing permissions of '/var/lib/postgresql/data/pgdata': Operation not permitted
    initdb: error: could not change permissions of directory "/var/lib/postgresql/data/pgdata": Operation not permitted
    fixing permissions on existing directory /var/lib/postgresql/data/pgdata ...

將掛載路徑設定回一般 NTFS 格式的磁碟，就可以正常運作了。

### 參照
[DockerHub](https://hub.docker.com/_/postgres)
[initdb: could not change permissions of directory on Postgresql container](https://stackoverflow.com/questions/44878062/initdb-could-not-change-permissions-of-directory-on-postgresql-container)

