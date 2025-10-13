# SFTP to WSL on Windows 11

> **原文發布日期:** 2022-06-01
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2022/06/01/SftpWslWin11
> **標籤:** 無

---

筆記下在 Windwos 11 安裝 WSL 並設定 SSH 連到 SFTP

1. 安裝 WSL：[安裝 WSL | Microsoft Docs](https://docs.microsoft.com/zh-tw/windows/wsl/install)
   * `wsl --install -d Ubuntu-20.04`
2. 建立金鑰：[ssh启动错误：no hostkeys available— exiting](https://wangxianggit.github.io/sshd%20no%20hostkeys%20available/)
   * `sudo su`
   * `ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key`
   * `ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key`
   * `chmod 600 /etc/ssh/ssh_host_dsa_key`
   * `chmod 600 /etc/ssh/ssh_host_rsa_key`
3. 設定 SSH：[A step by step tutorial on how to automatically start ssh server on boot on the Windows Subsystem for Linux](https://gist.github.com/dentechy/de2be62b55cfd234681921d5a8b6be11)
   * sudo vi /etc/ssh/sshd\_config
     + `Port=2222`
     + `PasswordAuthentication=yes`
     + `:wq`
   * `sudo service ssh --full-restart`
4. 承第3步驟：可能重開時需要手動啟動 SSH 服務
   * `sudo service ssh start`
5. 連到 SFTP：[sftp from Windows-10-v-1803 into WSL Ubuntu-18.04 ssh-server… won't connect](https://github.com/microsoft/WSL/issues/3303)
   * `sftp -v -P 2222 jakeuj@localhost`
6. 正常應該會成功連到 SFTP
   * `sftp>`
7. 建立使用者金鑰：[[教學] 產生SSH Key並且透過KEY進行免密碼登入](https://xenby.com/b/220-%E6%95%99%E5%AD%B8-%E7%94%A2%E7%94%9Fssh-key%E4%B8%A6%E4%B8%94%E9%80%8F%E9%81%8Ekey%E9%80%B2%E8%A1%8C%E5%85%8D%E5%AF%86%E7%A2%BC%E7%99%BB%E5%85%A5)
   * `ssh-keygen`
   * `cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys`
   * `cp ~/.ssh/id_rsa /mnt/d/`
8. 使用私鑰 `D:\id_rsa` 進行 SFTP 登入：[FileZilla](https://filezilla-project.org/)
9. 或是用 Docker 架：[[Docker] 使用 Docker 建置 FTP(SFTP) 環境](https://mileslin.github.io/2020/02/%E4%BD%BF%E7%94%A8-Docker-%E5%BB%BA%E7%BD%AE-FTP-SFTP-%E7%92%B0%E5%A2%83/)
   * `docker run -p 2223:22 -d atmoz/sftp miles:123456:::upload`

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [STFP](/jakeuj/Tags?qq=STFP)
* [WSL](/jakeuj/Tags?qq=WSL)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
