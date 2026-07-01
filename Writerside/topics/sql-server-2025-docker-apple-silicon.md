# Apple Silicon Mac 用 Docker 跑 SQL Server 2025 避開 AVX crash

<web-summary>Apple Silicon Mac 使用 Docker Desktop 跑 SQL Server 2025 時，如果遇到 AVX assertion crash，優先改用固定 SQL Server 2025 CU tag、開啟 Rosetta amd64 emulation，並避免吃到舊的 2025-latest cache。</web-summary>

在 M1 到 M4 Mac 上跑 SQL Server 2025 container 時，先不要把 `2025-latest` 當作穩定答案；更穩的做法是指定已驗證的 CU tag，例如 `mcr.microsoft.com/mssql/server:2025-CU5-ubuntu-24.04`，搭配 `--platform linux/amd64`，並在 Docker Desktop 使用 Apple Virtualization framework 與 Rosetta amd64 emulation。

<tldr>
    <p>`SQL Server 2025 will run as non-root... user mssql` 是正常訊息，不是錯誤。</p>
    <p>真正要處理的是 `x86_avx_state_ptr` / `kSupportedXFeatureBits` 這類 AVX assertion crash。</p>
    <p>在 Apple Silicon 上這不是 ARM 原生 SQL Server，而是 `linux/amd64` image 透過 Docker Desktop emulation 執行。</p>
</tldr>

## 問題症狀

在 Apple Silicon Mac 使用 SQL Server 2025 Docker image 時，container 可能反覆重啟，log 會看到：

```text
SQL Server 2025 will run as non-root by default.
This container is running as user mssql.

assertion failed [x86_avx_state_ptr->xsave_header.xfeatures == kSupportedXFeatureBits]:
(ThreadContextSignals.cpp:414 rt_sigreturn)
```

第一段 `non-root` 與 `user mssql` 是 SQL Server 2025 container 的正常行為；真正讓 SQL Server 起不來的是後面的 assertion failed。

這類問題常見於：

- Apple Silicon Mac，例如 M1、M2、M3、M4。
- Docker Desktop 使用 amd64 emulation 跑 `mcr.microsoft.com/mssql/server`。
- 本機仍有舊的 `2025-latest` image cache，或使用早期 SQL Server 2025 RTM / GA tag。

## 先講結論

本機開發可先用固定 CU tag 跑 SQL Server 2025：

```bash
docker rm -f sql2025 2>/dev/null || true

docker pull --platform=linux/amd64 \
  mcr.microsoft.com/mssql/server:2025-CU5-ubuntu-24.04

docker volume create sql2025data

docker run --platform=linux/amd64 \
  --pull=always \
  --name sql2025 \
  --hostname sql2025 \
  -e ACCEPT_EULA=Y \
  -e MSSQL_SA_PASSWORD='Your_Strong_Passw0rd!' \
  -e MSSQL_PID=Developer \
  -p 1433:1433 \
  -v sql2025data:/var/opt/mssql \
  --restart unless-stopped \
  -d mcr.microsoft.com/mssql/server:2025-CU5-ubuntu-24.04
```

成功後用 log 判斷是否 ready：

```bash
docker logs -f sql2025
```

看到類似這段才算 SQL Server 可以接受 client connection：

```text
SQL Server is now ready for client connections
```

再用 `sqlcmd` 驗證版本：

```bash
docker exec -it sql2025 /opt/mssql-tools18/bin/sqlcmd \
  -S localhost \
  -U sa \
  -P 'Your_Strong_Passw0rd!' \
  -C \
  -Q "SELECT @@VERSION;"
```

本次實測成功版本為：

```text
Microsoft SQL Server 2025 (RTM-CU5) (KB5084896) - 17.0.4045.5 (X64)
```

<note>
    <p>截至 2026-07-01，Microsoft release history 已列出 SQL Server 2025 CU6。本文保留 CU5 指令，是因為這個 tag 是本次排錯時已實測可在 Apple Silicon Docker Desktop 環境啟動的固定版本。新環境可以先查 Microsoft Artifact Registry，改用更新的固定 CU tag；重點是不要只依賴本機已有的 `2025-latest` cache。</p>
</note>

## Docker Desktop 設定

在 Apple Silicon 上先確認 Docker Desktop：

1. 安裝 Rosetta。

   ```bash
   softwareupdate --install-rosetta
   ```

2. 開啟 Docker Desktop。
3. 到 <ui-path>Settings | General</ui-path>。
4. <control>Virtual Machine Manager</control> 選 <control>Apple Virtualization framework</control>。
5. 勾選 <control>Use Rosetta for x86_64/amd64 emulation on Apple Silicon</control>。
6. Apply and Restart。

Docker 文件說明，Rosetta amd64 emulation 選項只有在選 Apple Virtualization framework 時可用；Docker VMM 目前不支援 Rosetta，amd64 emulation 會比較慢。

## Docker Compose 範例

如果用 Docker Compose，重點一樣是固定 CU tag、指定 `linux/amd64`，並用 `pull_policy: always` 避免吃到舊 cache。

```yaml
services:
  sql2025:
    image: mcr.microsoft.com/mssql/server:2025-CU5-ubuntu-24.04
    pull_policy: always
    platform: linux/amd64
    container_name: sql2025
    hostname: sql2025
    environment:
      ACCEPT_EULA: "Y"
      MSSQL_SA_PASSWORD: "Your_Strong_Passw0rd!"
      MSSQL_PID: "Developer"
    ports:
      - "1433:1433"
    volumes:
      - sql2025data:/var/opt/mssql
    restart: unless-stopped

volumes:
  sql2025data:
```

啟動前先 pull：

```bash
docker compose pull sql2025
docker compose down
docker compose up -d
docker logs -f sql2025
```

## 為什麼不要只靠 2025-latest

`latest` 是會移動的 tag，但本機 Docker 可能已經有舊 digest 的 `2025-latest` image。這時 compose 或 `docker run` 看起來使用的是 `2025-latest`，實際上可能仍在跑舊 RTM / GA image。

先確認本機 image：

```bash
docker images | grep mssql
docker image inspect mcr.microsoft.com/mssql/server:2025-latest \
  --format '{{.Id}} {{.Created}} {{.RepoDigests}}'
```

如果要清掉舊 cache：

```bash
docker rm -f sql2025 2>/dev/null || true
docker image rm mcr.microsoft.com/mssql/server:2025-latest 2>/dev/null || true
docker image rm mcr.microsoft.com/mssql/server:2025-RTM-ubuntu-22.04 2>/dev/null || true
docker image rm mcr.microsoft.com/mssql/server:2025-GA-ubuntu 2>/dev/null || true
```

清完後再 pull 固定 CU tag：

```bash
docker pull --platform=linux/amd64 \
  mcr.microsoft.com/mssql/server:2025-CU5-ubuntu-24.04
```

## 官方支援邊界

Microsoft 官方文件仍說 SQL Server container image 只支援 Intel / AMD x86-64 CPU 的 Linux host；Rosetta 2、Prism、QEMU 這類 emulation 或 translation environment 不屬於已測試或支援的環境。

所以在 Apple Silicon Mac 上要把它當成本機開發 workaround，而不是正式環境架構。需要穩定測試或正式服務時，優先放到：

- x86-64 Linux VM 或實體機
- Azure VM
- Azure SQL
- 其他正式支援 SQL Server 的 x86-64 環境

## 如果 CU5 還是失敗

可以依序檢查：

1. **確認實際 image**：`docker ps -a` 和 `docker image inspect` 是否真的指到 `2025-CU5-ubuntu-24.04`。
2. **確認平台**：`docker run` 是否有 `--platform linux/amd64`，或 compose 中是否有 `platform: linux/amd64`。
3. **確認 Docker Desktop VMM**：是否使用 Apple Virtualization framework，而不是 Docker VMM。
4. **確認 Rosetta**：Docker Desktop 是否勾選 `Use Rosetta for x86_64/amd64 emulation on Apple Silicon`。
5. **換執行環境**：若 Docker Desktop 仍失敗，可測 OrbStack；若仍不穩，本機開發先退回 `mcr.microsoft.com/mssql/server:2022-latest`。

常見替代方案排序：

1. SQL Server 2025 固定 CU tag，例如 `2025-CU5-ubuntu-24.04` 或更新的固定 CU tag。
2. OrbStack 跑同一個 `linux/amd64` image。
3. 開發階段暫時使用 SQL Server 2022。
4. 正式或穩定測試環境改放 x86-64 Linux / Azure。

## 參考資料

- [Microsoft Learn: Release history for SQL Server 2025 on Linux](https://learn.microsoft.com/en-us/troubleshoot/sql/releases/linux/release-history-2025)
- [Microsoft Learn: Cumulative Update 5 for SQL Server 2025](https://learn.microsoft.com/en-us/troubleshoot/sql/releases/sqlserver-2025/cumulativeupdate5)
- [Microsoft Learn: Run SQL Server Linux container images with Docker](https://learn.microsoft.com/en-us/sql/linux/install-upgrade/quickstart-install-docker?view=sql-server-ver17)
- [Microsoft Artifact Registry: mssql/server tags](https://mcr.microsoft.com/artifact/mar/mssql/server/tags)
- [Docker Docs: Docker Desktop settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/)
- [Docker Docs: Virtual Machine Manager for Docker Desktop on Mac](https://docs.docker.com/desktop/features/vmm/)
- [GitHub: microsoft/mssql-docker issue 942](https://github.com/microsoft/mssql-docker/issues/942)
