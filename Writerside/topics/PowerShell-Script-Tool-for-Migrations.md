# PowerShell Script Tool for Migrations

> **原文發布日期:** 2019-07-23
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2019/07/23/PowerShellMigrations
> **標籤:** 無

---

PowerShell 腳本用來管理 Migrations

```

<#
# 文件：migration.ps1
# 用途：用於Migration相關功能腳本
# 創建：2019-07-23
# 備註：需先設定允許腳本執行
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# 範例：
# .\migration.ps1 add init
# .\migration.ps1 update
# .\migration.ps1 script
# .\migration.ps1 remove
#>
param (
    [string]$Cmd = $(throw "Cmd parameter is required."),
    [string]$MigrationName = $null,
    [string]$DbContextName = "OBManMigrationsDbContext",
    [string]$StartupProjectPath = "src\Wow.OBMan.Web",
    [string]$MigrationProjectPath = "src\Wow.OBMan.EntityFrameworkCore.DbMigrations",
    [string]$ScriptOutputPath = "sql\$DbContextName\"
)
Write-Host "Start."
switch($Cmd)
{
    "add"
    {
        if([string]::IsNullOrEmpty($MigrationName))
        {
            throw "Add:MigrationName parameter is required."
        }
        Write-Host "dotnet ef migrations add $MigrationName -c $DbContextName -s $StartupProjectPath -p $MigrationProjectPath"
        dotnet ef migrations add $MigrationName -c $DbContextName -s $StartupProjectPath -p $MigrationProjectPath
        break
    }
    "update"
    {
        if([string]::IsNullOrEmpty($MigrationName))
        {
            Write-Host "dotnet ef database update -c $DbContextName -s $StartupProjectPath -p $MigrationProjectPath"
            dotnet ef database update -c $DbContextName -s $StartupProjectPath -p $MigrationProjectPath
        }
        else
        {
            Write-Host "dotnet ef database update $MigrationName -c $DbContextName -s $StartupProjectPath -p $MigrationProjectPath"
            dotnet ef database update $MigrationName -c $DbContextName -s $StartupProjectPath -p $MigrationProjectPath
        }
        break
    }
    "script"
    {
        if([string]::IsNullOrEmpty($MigrationName))
        {
            $ScriptName = "default.sql"
            $ScriptOutputPath += $ScriptName
            Write-Host "dotnet ef migrations script -c $DbContextName  -s $StartupProjectPath -p $MigrationProjectPath -o $ScriptOutputPath"
            dotnet ef migrations script -c $DbContextName  -s $StartupProjectPath -p $MigrationProjectPath -o $ScriptOutputPath
        }
        else
        {
            $ScriptName =  "$MigrationName.sql"
            $ScriptOutputPath += $ScriptName
            Write-Host "dotnet ef migrations script $MigrationName -c $DbContextName  -s $StartupProjectPath -p $MigrationProjectPath -o $ScriptOutputPath"
            dotnet ef migrations script $MigrationName -c $DbContextName  -s $StartupProjectPath -p $MigrationProjectPath -o $ScriptOutputPath
        }
        break
    }
    "remove"
    {
        Write-Host "dotnet ef migrations remove -c $DbContextName  -s $StartupProjectPath -p $MigrationProjectPath"
        dotnet ef migrations remove -c $DbContextName  -s $StartupProjectPath -p $MigrationProjectPath
        break
    }
}
Write-Host "End."
```

延伸閱讀：[Entity Framework Core Migrations 注意事項](https://dotblogs.com.tw/jakeuj/2019/07/23/efcoremigrations)

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Entity Framework
{ignore-vars="true"}
* PowerShell
* Migration

* 回首頁

---

*本文章從點部落遷移至 Writerside*
