# Docker

筆記下 Docker 的使用方式。

![docker.png](docker.png){style="block"}

## Dockerfile

Rider 自動產生的 Dockerfile，稍微修改一下

```Docker
#See https://aka.ms/customizecontainer to learn how to customize your debug container 
# and how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER app
WORKDIR /app
EXPOSE 8080
EXPOSE 8081

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["NuGet.Config", "."]
COPY ["TestProj/TestProj.csproj", "TestProj/"]
RUN dotnet restore "./TestProj/./TestProj.csproj"
COPY . .
WORKDIR "/src/TestProj"
RUN dotnet build "./TestProj.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./TestProj.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "TestProj.dll"]
```

### VS 產生的 比 Rider 多了以下設定。

```Docker
COPY ["NuGet.Config", "."]
```

## .dockerignore
將 VS 與 Rider 自動產生的 dockerignore 合併。

```Docker
**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/.idea
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/azds.yaml
**/bin
**/charts
**/docker-compose*
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
LICENSE
README.md
!**/.gitignore
!.git/HEAD
!.git/config
!.git/packed-refs
!.git/refs/heads/**
```

### VS 產生的 dockerignore 比 Rider 多了以下設定。

```Docker
**/.classpath
!**/.gitignore
!.git/HEAD
!.git/config
!.git/packed-refs
!.git/refs/heads/**
```

## Migration

ABP 單層架構的專案，使用以下邏輯來判斷是否執行資料庫遷移：
    
```C#
args.Any(x => x.Contains("--migrate-database"))
```

所以在執行容器時，要加上 `--migrate-database` 參數。

```Shell
 docker run
 --name db-migration
 --link some-postgres:db
 -d
 -e "ConnectionStrings:Default=Host=db;Port=5432;Database=TestProj;User ID=root;Password=myPassword;"
 -e ASPNETCORE_ENVIRONMENT=Development
 -e ASPNETCORE_STATICWEBASSETS=/app/bin/Debug/net8.0/TestProj.staticwebassets.runtime.CT.json
 -e DOTNET_USE_POLLING_FILE_WATCHER=true
 -e DOTNET_RUNNING_IN_CONTAINER=true
 -v D:\jake.chu\.nuget\packages:/home/app/.nuget/packages:ro
 -v D:\repos\TestProj\TestProj:/app
 -v D:\repos\TestProj:/src
 db-migration:dev
 dotnet
 /app/bin/Debug/net8.0/TestProj.dll
 --migrate-database
```
## docker-compose.yml
可以用 docker-compose up 建立 DB 、 Migration 、最後執行 Web App。

```yaml
services:
  kanban-postgres:
    image: postgres
    container_name: kanban-postgres
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: myPassword
    ports:
      - "5432:5432"
    volumes:
      - kanban-data:/var/lib/postgresql/data
  migration:
    image: testproj
    build:
      context: .
      dockerfile: TestProj/Dockerfile
    depends_on:
      - kanban-postgres
    container_name: migration
    environment:
      - DB_SERVER=kanban-postgres
      - ConnectionStrings:Default=Host=kanban-postgres;Port=5432;Database=TestProj;User ID=root;Password=myPassword;
    links:
      - kanban-postgres
    command: ["--migrate-database"]
  testproj:
    image: testproj
    build:
      context: .
      dockerfile: TestProj/Dockerfile
    depends_on:
      - migration
    container_name: test-proj
    environment:
      - DB_SERVER=kanban-postgres
      - ConnectionStrings:Default=Host=kanban-postgres;Port=5432;Database=TestProj;User ID=root;Password=myPassword;
    ports:
      - 8080:8080
    links:
      - kanban-postgres
    restart: on-failure
volumes:
  kanban-data:
```

## Rider
如果發現沒吃到 `command: ["--migrate-database"]` 參數

可以在 Rider 的 Docker Compose 設定裡面加上 Don't use Docker fast mode。

如下圖所示

![compose-config.png](compose-config.png){style="block"}

實測成功後再次移除 `Don't use Docker fast mode`，一樣會導致讀不到 `--migrate-database`。

### Docker Fast Mode

JetBrains Rider 的 Docker Fast Mode 是一種特殊的模式，用於加速 Docker 容器的啟動和停止。這種模式主要通過以下方式實現：  
- 快速啟動：在 Fast Mode 中，Rider 不會每次都重新構建 Docker 映像。相反，它會檢查映像是否已經存在，如果存在，則直接啟動該映像的容器。這大大減少了啟動時間。  
- 快速停止：在 Fast Mode 中，當你停止 Docker 容器時，Rider 不會真正地停止容器，而是將其暫停。這意味著下次啟動時，容器可以立即恢復運行，而不需要重新啟動。  
- 快速更新：在 Fast Mode 中，當你修改了 Dockerfile 或相關的配置文件時，Rider 只會重新構建那些被修改的部分，而不是整個映像。這也大大加快了更新速度。  
請注意，Fast Mode 可能不適合所有情況。例如，如果你的應用依賴於容器的啟動狀態，或者你需要每次都從一個乾淨的環境開始，那麼你可能需要關閉 Fast Mode。

## TODO
depends_on 似乎沒有等到 Migration 完成就開始執行 Web App。

## 參照
GitHub: [Docker](https://github.com/jakeuj/TestDocker/blob/master/docker-compose.yml)