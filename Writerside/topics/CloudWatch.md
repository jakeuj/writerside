# CloudWatch

紀錄 AWS CloudWatch 的使用方式，是說 AWS 的文件也太碎片化了，沒有一條龍的服務嗎？

目前方向上可分為：
- 使用 CloudWatch Agent (從 VM 內部安裝代理程式)
  - 需建立具備寫入 Log Group 相關權限的 IAM Role 並設定到 EC2 上
- 使用 AWS.Logger.SeriLog (從程式內部安裝 CloudWatch for SeriLog 庫)
  - 需建立具備寫入 Log Group 相關權限的 IAM Role 並設定到 User 賬號上，並且需要可以建立 Access Key 的 IAM User

## IAM role (Create)
建立具有日誌所需權限的角色

"logs:CreateLogGroup",
"logs:CreateLogStream",
"logs:PutLogEvents"

[create-iam-role](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_roles_create_for-user.html)

## EC2 (Modify IAM Role)
到 AWS 找到 EC2 右上角 Action -> Security -> Modify IAM Role 添加具有權限的角色

## SSM Agent

[install-ssm-agent-windows](https://docs.aws.amazon.com/zh_cn/systems-manager/latest/userguide/manually-install-ssm-agent-windows.html)

```shell
[System.Net.ServicePointManager]::SecurityProtocol = 'TLS12'
$progressPreference = 'silentlyContinue'
Invoke-WebRequest `
    https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/windows_amd64/AmazonSSMAgentSetup.exe `
-OutFile $env:USERPROFILE\Desktop\SSMAgent_latest.exe
```

```shell
Start-Process `
    -FilePath $env:USERPROFILE\Desktop\SSMAgent_latest.exe `
-ArgumentList "/S" `
-Wait
-OutFile $env:USERPROFILE\Desktop\SSMAgent_latest.exe
```

```shell
rm -Force $env:USERPROFILE\Desktop\SSMAgent_latest.exe
````

```shell
Restart-Service AmazonSSMAgent
```

## CloudWatch Agent

[amazon-cloudwatch-agent.msi](https://amazoncloudwatch-agent.s3.amazonaws.com/windows/amd64/latest/amazon-cloudwatch-agent.msi)

### install

```shell
msiexec.exe /i amazon-cloudwatch-agent.msi /quiet
```

### config
設定自定義 Logs 時，需要指定到檔案，例如：`"file_path": "D:\\logs\\*.log",`

```shell
cd "C:\Program Files\Amazon\AmazonCloudWatchAgent"

.\amazon-cloudwatch-agent-config-wizard.exe
```

### start

```shell
cd "C:\Program Files\Amazon\AmazonCloudWatchAgent"
& "C:\Program Files\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent-ctl.ps1" -a fetch-config -m ec2 -s -c file:config.json
```

```
****** processing amazon-cloudwatch-agent ******
I! Trying to detect region from ec2
D! [EC2] Found active network interface
I! imds retry client will retry 1 timesSuccessfully fetched the config and saved in C:\ProgramData\Amazon\AmazonCloudWatchAgent\Configs\file_config.json.tmp
Start configuration validation...
2025/04/01 15:00:29 Reading json config file path: C:\ProgramData\Amazon\AmazonCloudWatchAgent\Configs\file_config.json.tmp ...
2025/04/01 15:00:29 I! Valid Json input schema.
I! Trying to detect region from ec2
D! [EC2] Found active network interface
I! imds retry client will retry 1 times2025/04/01 15:00:30 D! ec2tagger processor required because append_dimensions is set
2025/04/01 15:00:30 D! ec2tagger processor required because append_dimensions is set
2025/04/01 15:00:30 Configuration validation first phase succeeded
Configuration validation second phase succeeded
Configuration validation succeeded
AmazonCloudWatchAgent has been stopped
AmazonCloudWatchAgent has been started
```