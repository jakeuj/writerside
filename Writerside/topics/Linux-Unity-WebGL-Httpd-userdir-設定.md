# Linux Unity WebGL Httpd userdir 設定

> **原文發布日期:** 2018-01-08
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2018/01/08/LinuxWebGL
> **標籤:** 無

---

Linux Unity WebGL Httpd userdir 設定

### 更新

yum update
init 6

### 安裝Apache

yum install httpd

### 編輯設定檔
vi /etc/httpd/conf.d/userdir.conf

### 註解 UserDir disabled
#UserDir disabled

### 反註解 #UserDir public\_html
UserDir public\_html

### 設定權限 (使用者名稱=jake)

chmod 711 /home/jake

mkdir /home/jake/public\_html

chmod 755 /home/jake/public\_html

chown jake:jake /home/jake/public\_html

### 設定副檔名支援

vi /etc/httpd/conf.d/unity.conf

```

AddType application/vnd.unity unity3d
AddType application/x-javascript jsgz
AddType application/octet-stream memgz datagz unity3dgz

AddEncoding gzip .jsgz
AddEncoding gzip .datagz
AddEncoding gzip .memgz
AddEncoding gzip .unity3dgz
```

### 更改Unity WebGL生成的index.html (引用檔案後方加上gz)

```

dataUrl: "Release/Reborn.datagz",

codeUrl: "Release/Reborn.jsgz",

asmUrl: "Release/Reborn.asm.jsgz",

memUrl: "Release/Reborn.memgz",
```

### 開防火牆80
firewall-cmd --zone=public --add-port=80/tcp --permanent
systemctl restart firewalld.service

### 步驟 1: 安裝 SELINUX 政策管理
yum install policycoreutils-python

### 步驟 2: 設定 SELINUX 權限
semanage fcontext -a -t httpd\_sys\_content\_t "/home/jake/public\_html(/.\*)?"

### 或是直接關閉防火牆 (不建議)

systemctl disable firewalld.service

### 或是直接關閉 SELINUX 後重啟 (不建議)

sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

### 替代方案 3: 暫時關閉 SELINUX

sudo setenforce 0

### 將Unity建置的WebGL上傳到 /home/jake/public\_html

cp WebGL /home/jake/public\_html

### 開啟網頁

http://localhost/~jake/WebGL

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* Apache
* Httpd
* Linux
* Unity
* WebGL

* 回首頁

---

*本文章從點部落遷移至 Writerside*
