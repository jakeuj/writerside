# Share Wifi

Windows 11 筆記型電腦可以通過 LAN 取得 IP 地址後，再使用 Wi-Fi 網卡作為 AP（接入點）來分享網絡給手機。

![wifi.png](wifi.png){style="block"}

## 行動熱點

以下是具體步驟：

1. **確保網絡連接正常**：
    - 使用網路線將筆記型電腦連接到路由器，確保已經成功取得 LAN IP 並且能正常上網。

2. **設置行動熱點**：
    - 打開 `設定`（Settings）。
    - 選擇 `網路與網際網路`（Network & Internet）。
    - 點擊 `行動熱點`（Mobile hotspot）。
    - 在 `共用我的網際網路連線`（Share my Internet connection from）下拉選單中，選擇 `乙太網路`（Ethernet）。
    - 開啟 `共用我的網際網路連線與其他裝置`（Share my Internet connection with other devices）開關。
    - 在 `行動熱點` 設定中，可以設定網絡名稱（Network name）和密碼（Network password）。

3. **配置 Wi-Fi 網卡**：
    - 在 `行動熱點`（Mobile hotspot）設置頁面下，點擊 `編輯`（Edit），可以自定義 SSID（網絡名稱）和密碼，這些資訊需要在手機連接 Wi-Fi 時使用。

4. **連接手機**：
    - 開啟手機的 Wi-Fi 設定，搜尋並連接剛剛設置的行動熱點，輸入設定好的密碼即可。

通過這些步驟，您就可以將筆記型電腦上的網絡通過 Wi-Fi 共享給手機使用。如有任何問題，請隨時告知。

## 防火牆

需要設定防火牆，在公開網路中允許服務使用的 port 連入方向的流量。

![fwc.png](fwc.png){style="block"}

初步測試階段可以考慮先關閉公用網路的防火牆，以確保手機能夠正常連接。

![firewall.png](firewall.png){style="block"}

測試可連線後記得回頭設定防火牆，並重新啟用公開網路的防火牆，以免被左右鄰兵攻擊！

## 連線

主機 IP 預設為 192.168.137.1，手機連接後可以在手機瀏覽器中輸入這個 IP 來訪問主機。

請確保服務有 Listen 192.168.137.1 的設定，以便手機能夠正常訪問。

## Vue

```Shell
yarn dev --host
yarn run v1.22.22
$ vite --host

  VITE v5.3.3  ready in 1201 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.137.1:5173/
  ➜  press h + enter to show help
```

## 結論

祝大家與 IT 同仁更緊密連接，共同進步！
