# Azure App Service CI/CD 部署檔案鎖定問題

## 問題描述

在使用 GitHub Actions 進行 CI/CD 部署到 Azure App Service 時，可能會遇到以下情況：

- GitHub Actions 顯示部署成功
- Azure Portal 顯示部署完成
- **但實際應用程式並未更新**

### 錯誤原因

查看部署日誌會發現類似以下錯誤：

```
Failed to delete log files: The process cannot access the file because it is being used by another process.
```

**根本原因**：應用程式在運行時持續寫入 log 檔案，導致部署腳本在清理舊檔案時遇到檔案鎖定 (file lock)，最終導致部署失敗。

## 解決方案

### 方案一：停止站台後部署 (推薦)

在 CI/CD workflow 中，於部署前後加入停止/啟動站台的步驟：

```yaml
  - name: Stop Azure Web App Slot (避免 log 檔案鎖定)
    run: |
        Write-Host "停止 App Service Slot 以避免檔案鎖定問題..."
        az webapp stop --name your-app-name --resource-group your-rg --slot your-slot
        Start-Sleep -Seconds 10

  - name: Deploy to Azure Web App
    id: deploy-to-webapp
    uses: azure/webapps-deploy@v3
    with:
      app-name: 'your-app-name'
      slot-name: 'your-slot'
      package: .

  - name: Start Azure Web App Slot
    if: always()  # 確保即使部署失敗也會重新啟動
    run: |
        Write-Host "啟動 App Service Slot..."
        az webapp start --name your-app-name --resource-group your-rg --slot your-slot
```

#### 重點說明

- **`Start-Sleep -Seconds 10`**：等待 10 秒確保站台完全停止，釋放所有檔案鎖定
- **`if: always()`**：確保無論部署成功或失敗，都會重新啟動站台，避免服務長時間中斷
- **使用 Slot**：建議使用部署槽位 (deployment slot) 進行部署，可以搭配 slot swap 實現零停機部署

### 方案二：使用 Slot Swap (零停機部署)

更好的做法是使用 Azure App Service 的 Slot Swap 功能：

```yaml
  - name: Deploy to Staging Slot
    uses: azure/webapps-deploy@v3
    with:
      app-name: 'your-app-name'
      slot-name: 'staging'
      package: .

  - name: Swap Staging to Production
    run: |
        Write-Host "執行 Slot Swap..."
        az webapp deployment slot swap \
          --name your-app-name \
          --resource-group your-rg \
          --slot staging \
          --target-slot production
```

**優點**：
- 零停機時間
- 可以在 staging slot 驗證部署結果
- 出問題時可以快速 swap 回去

### 方案三：調整應用程式日誌設定

從根本解決問題，調整應用程式的日誌寫入方式：

#### .NET 應用程式

在 `appsettings.json` 中設定日誌：

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information"
    },
    "ApplicationInsights": {
      "LogLevel": {
        "Default": "Information"
      }
    }
  }
}
```

使用 Azure Application Insights 取代檔案日誌，或使用支援檔案輪替的日誌框架 (如 Serilog)。

#### Serilog 設定範例

```csharp
Log.Logger = new LoggerConfiguration()
    .WriteTo.File(
        path: "logs/app-.txt",
        rollingInterval: RollingInterval.Day,
        shared: true,  // 允許多個程序共享日誌檔案
        retainedFileCountLimit: 7
    )
    .CreateLogger();
```

## 最佳實踐建議

1. **使用 Deployment Slots**：利用 staging/production slots 實現藍綠部署
2. **啟用 Application Insights**：使用雲端日誌服務取代本地檔案日誌
3. **設定健康檢查**：在 swap 前確認新版本正常運作
4. **監控部署狀態**：設定 GitHub Actions 通知，及時發現部署問題
5. **保留部署歷史**：設定適當的 `retainedFileCountLimit` 避免磁碟空間不足

## 相關資源

- [Azure App Service Deployment Slots](https://learn.microsoft.com/azure/app-service/deploy-staging-slots)
- [GitHub Actions for Azure Web Apps](https://github.com/Azure/webapps-deploy)
- [Azure Application Insights](https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview)