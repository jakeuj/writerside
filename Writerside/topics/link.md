# 容器互連

Web App Container 連到 Database Container，這是一個常見的情境。

![link2.png](link2.png){style="block"}

## link

Usage:  `docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`

```Shell
docker run -d -P 
 --name testproj 
 --link some-postgres:db 
 -e "ConnectionStrings:Default=Host=db;Port=5432;Database=TestProj;User ID=root;Password=myPassword;"
 testproj:dev 
 dotnet 
 TestProj.dll
```

--link 參數的格式為：`--link name:alias`

- name 連線的容器名稱
- alias 連線的別名

### Sample

```Shell
docker run
 --name testprojps
 --link some-postgres:db
 -d
 -p 8080:8080
 -e "ConnectionStrings:Default=Host=db;Port=5432;Database=TestProj;User ID=root;Password=myPassword;"
 -e ASPNETCORE_ENVIRONMENT=Development
 -e ASPNETCORE_STATICWEBASSETS=/app/bin/Debug/net8.0/TestProj.staticwebassets.runtime.CT.json
 -e DOTNET_USE_POLLING_FILE_WATCHER=true
 -e DOTNET_RUNNING_IN_CONTAINER=true
 -v D:\jake.chu\.nuget\packages:/home/app/.nuget/packages:ro
 -v D:\repos\TestProj\TestProj:/app
 -v D:\repos\TestProj:/src
 testproj:dev
 dotnet
 /app/bin/Debug/net8.0/TestProj.dll
 ```

### 注意大小寫

Example: IMAGE=testproj:dev

寫成 testProj:dev 會報錯

## RDF

[容器互連](https://philipzheng.gitbook.io/docker_practice/network/linking)
