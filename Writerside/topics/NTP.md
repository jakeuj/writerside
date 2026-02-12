# NTP

筆記一下 NTP (123 UDP) 不通

## 更改 NTP Server

```bash
sudo nano /etc/systemd/timesyncd.conf
```

```Ini
[Time]
NTP=ntp.myserver.intra
```

## Ref

[NTP](https://www.cnblogs.com/pipci/p/12833228.html)
