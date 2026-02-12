# mount-disk

筆記下我手上的 Ubuntu 安裝碟，再 Windows 11 WSL 2 中的掛載方式。

## Windows 11 WSL 2 中掛載 Ubuntu 安裝碟

### 1. 識別磁碟

```Bash
GET-CimInstance -query "SELECT * from Win32_DiskDrive"
```

![image_1.png](image_1.png){style="block"}

下面如果有問題可以到磁碟管理將該磁碟先離線

![image_7.png](image_7.png){style="block"}

### 2. 掛載磁碟

```Bash
wsl --mount \\.\PHYSICALDRIVE1 --bare
```

![image_2.png](image_2.png){style="block"}

### 3. 進入 WSL 2

```Bash
lsblk
```

![image_3.png](image_3.png){style="block"}

### 4. 識別格式

```Bash
sudo blkid
```

![image_4.png](image_4.png){style="block"}

記錄下 ext4 的 ID = 4

### 5. 卸離磁碟

```Bash
wsl --unmount \\.\PHYSICALDRIVE1
```

![image_5.png](image_5.png){style="block"}

### 6. 重新掛載磁碟

將 ext4 的 ID = 4 帶入

```Bash
wsl --mount \\.\PHYSICALDRIVE1 --partition 4
```

![image_6.png](image_6.png){style="block"}

磁碟已成功裝載為 '/mnt/wsl/PHYSICALDRIVE1p4'。

### 7. 進入磁碟

```Bash
cd /mnt/wsl/PHYSICALDRIVE1p4
```

### 8. 離開 WSL 2

```Bash
exit
```

### 9. 卸離磁碟

```Bash
wsl --unmount \\.\PHYSICALDRIVE1
```

## REF

[在 WSL 2 中掛接 Linux 磁碟](https://learn.microsoft.com/zh-tw/windows/wsl/wsl2-mount-disk)
