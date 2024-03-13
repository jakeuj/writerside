# Docker

筆記下 Docker 的使用方式。

![docker.png](docker.png)

## Dockerfile

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

### Rider
如果發現沒吃到 `command: ["--migrate-database"]` 參數

可以在 Rider 的 Docker Compose 設定裡面加上 Don't use Docker fast mode。

如下圖所示

![compose-config.png](compose-config.png)

## TODO
depends_on 似乎沒有等到 Migration 完成就開始執行 Web App。

## 參照
GitHub: [Docker](https://github.com/jakeuj/TestDocker/blob/master/docker-compose.yml)