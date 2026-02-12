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

預設只會記錄事件 system，如果要記錄登入事件，則需要在 `config.json` 中加入 `"event_name": "Security"` 區段：

`C:\ProgramData\Amazon\AmazonCloudWatchAgent\Configs\file_config.json`

```json
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "D:\\logs\\*.json",
            "log_group_class": "STANDARD",
            "log_group_name": "logs",
            "log_stream_name": "{instance_id}",
            "retention_in_days": 180
          }
        ]
      },
      "windows_events": {
        "collect_list": [
          {
            "event_format": "xml",
            "event_levels": [
              "VERBOSE",
              "INFORMATION",
              "WARNING",
              "ERROR",
              "CRITICAL"
            ],
            "event_name": "System",
            "log_group_class": "STANDARD",
            "log_group_name": "System",
            "log_stream_name": "{instance_id}",
            "retention_in_days": 180
          },
          {
            "event_format": "xml",
            "event_levels": [
              "INFORMATION",
              "WARNING",
              "ERROR",
              "CRITICAL"
            ],
            "event_name": "Security",
            "log_group_class": "STANDARD",
            "log_group_name": "Security",
            "log_stream_name": "{instance_id}",
            "retention_in_days": 180
          }
        ]
      }
    }
  },
  "metrics": {
    "aggregation_dimensions": [
      [
        "InstanceId"
      ]
    ],
    "append_dimensions": {
      "AutoScalingGroupName": "${aws:AutoScalingGroupName}",
      "ImageId": "${aws:ImageId}",
      "InstanceId": "${aws:InstanceId}",
      "InstanceType": "${aws:InstanceType}"
    },
    "metrics_collected": {
      "LogicalDisk": {
        "measurement": [
          "% Free Space"
        ],
        "metrics_collection_interval": 60,
        "resources": [
          "*"
        ]
      },
      "Memory": {
        "measurement": [
          "% Committed Bytes In Use"
        ],
        "metrics_collection_interval": 60
      },
      "statsd": {
        "metrics_aggregation_interval": 60,
        "metrics_collection_interval": 10,
        "service_address": ":8125"
      }
    }
  }
}
```

改完記得重啟服務

```powershell
& "C:\Program Files\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent-ctl.ps1" -a stop
& "C:\Program Files\Amazon\AmazonCloudWatchAgent\amazon-cloudwatch-agent-ctl.ps1" -a start
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

## Query

- 登入成功 4624
- 登入失敗 4625

Windows Events Log 會有兩個 log group，分別是 `System` 和 `Security`，登入事件會在 `Security` 裡面。

```
filter @logStream = 'i-0416c1dd94d16227f'
| fields @timestamp, @message
| parse @message "<EventID>*</EventID>" as EventID
| filter EventID = "4624"
| parse @message "<Data Name='TargetUserName'>*</Data>" as TargetUserName
| parse @message "<Data Name='TargetDomainName'>*</Data>" as TargetDomainName
| parse @message "<Data Name='IpAddress'>*</Data>" as IpAddress
| parse @message "<Data Name='LogonType'>*</Data>" as LogonType
| parse @message "<Data Name='ProcessName'>*</Data>" as ProcessName
| display @timestamp, TargetUserName, TargetDomainName, IpAddress, LogonType, ProcessName
| sort @timestamp desc
| limit 20
```

自己的 json log

```
fields @timestamp, MessageTemplate,Properties.IP,Properties.Uri,Properties.UserID,Timestamp
| filter Properties.Uri like /Login/
| sort @timestamp desc
| limit 10000
```
