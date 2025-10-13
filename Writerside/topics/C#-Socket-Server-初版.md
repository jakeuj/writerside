# C# Socket Server 初版

> **原文發布日期:** 2012-04-11
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2012/04/11/71413
> **標籤:** 無

---

C# Socket Server 初版

因緣際會需要學習一下，這是至少可以跑的版本，還在想怎麼改比較好，請不吝賜教，感謝！

Server端

```

   1:  using System;
```

```

   2:  using System.Collections.Generic;
```

```

   3:  using System.ComponentModel;
```

```

   4:  using System.Net;
```

```

   5:  using System.Net.Sockets;
```

```

   6:  using System.Text;
```

```

   7:
```

```

   8:  namespace MyServer
```

```

   9:  {
```

```

  10:      class Program
```

```

  11:      {
```

```

  12:          // 宣告客戶端清單
```

```

  13:          public static List<Client> ClientList;
```

```

  14:
```

```

  15:          public static void Main(string[] args)
```

```

  16:          {
```

```

  17:              //產生 BackgroundWorker 負責處理每一個 socket client 的 reuqest
```

```

  18:              BackgroundWorker bgwSocket = new BackgroundWorker();
```

```

  19:              bgwSocket.DoWork += new DoWorkEventHandler(bgwSocket_DoWork);
```

```

  20:              bgwSocket.RunWorkerAsync();
```

```

  21:              while (true)
```

```

  22:              {
```

```

  23:                  BoardCast("伺服器端：" + Console.ReadLine());
```

```

  24:              }
```

```

  25:          }
```

```

  26:
```

```

  27:          private static void bgwSocket_DoWork(object sender, DoWorkEventArgs e)
```

```

  28:          {
```

```

  29:              // 設定連線接聽阜值
```

```

  30:              const int ServerPort = 80;
```

```

  31:
```

```

  32:              // 設定半開連接數
```

```

  33:              const int BackLog = 10;
```

```

  34:
```

```

  35:              // 初始化客戶端清單
```

```

  36:              ClientList = new List<Client>();
```

```

  37:
```

```

  38:              // 初始化客戶端序列號
```

```

  39:              int PlayerNum = 0;
```

```

  40:
```

```

  41:              // 建立接聽Socket
```

```

  42:              Socket ListenSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
```

```

  43:
```

```

  44:              // 綁定接聽Socket的IP與Port
```

```

  45:              ListenSocket.Bind(new IPEndPoint(IPAddress.Any, ServerPort));
```

```

  46:
```

```

  47:              // 開始接聽
```

```

  48:              ListenSocket.Listen(BackLog);
```

```

  49:
```

```

  50:              // 輸出伺服器端起始訊息
```

```

  51:              Console.WriteLine("開始接聽客戶端連線...");
```

```

  52:
```

```

  53:              // 持續等待客戶端接入
```

```

  54:              while (true)
```

```

  55:              {
```

```

  56:                  ClientList.Add(new Client(PlayerNum, ListenSocket.Accept()));
```

```

  57:                  PlayerNum++;
```

```

  58:              }
```

```

  59:          }
```

```

  60:
```

```

  61:          public static void BoardCast(string serverResponse)
```

```

  62:          {
```

```

  63:              foreach (Client myClient in Program.ClientList)
```

```

  64:              {
```

```

  65:                  myClient.SendToPlayer(serverResponse);
```

```

  66:                  Console.WriteLine("廣播訊息：{0}", serverResponse);
```

```

  67:              }
```

```

  68:          }
```

```

  69:
```

```

  70:          public static void RemoveClient(int PlayerNum)
```

```

  71:          {
```

```

  72:              foreach (Client myClient in Program.ClientList)
```

```

  73:              {
```

```

  74:                  if (myClient.CurrentPlayerNum.Equals(PlayerNum))
```

```

  75:                  {
```

```

  76:                      Program.ClientList.Remove(myClient);
```

```

  77:                      break;
```

```

  78:                  }
```

```

  79:              }
```

```

  80:          }
```

```

  81:      }
```

```

  82:
```

```

  83:      class Client
```

```

  84:      {
```

```

  85:          public int CurrentPlayerNum { get; set; }
```

```

  86:          public Socket PlayerSocket { get; set; }
```

```

  87:          public int CurrentStatus { get; set; }
```

```

  88:          public Client(int PlayerNum, Socket mySocket)
```

```

  89:          {
```

```

  90:              this.CurrentPlayerNum = PlayerNum;
```

```

  91:              this.PlayerSocket = mySocket;
```

```

  92:              this.CurrentStatus = 1;
```

```

  93:              DoCommunicate();
```

```

  94:          }
```

```

  95:
```

```

  96:          public void DoCommunicate()
```

```

  97:          {
```

```

  98:              //產生 BackgroundWorker 負責處理每一個 socket client 的 reuqest
```

```

  99:              BackgroundWorker bgwSocket = new BackgroundWorker();
```

```

 100:              bgwSocket.DoWork += new DoWorkEventHandler(bgwSocket_DoWork);
```

```

 101:              bgwSocket.RunWorkerAsync();
```

```

 102:          }
```

```

 103:
```

```

 104:          private void bgwSocket_DoWork(object sender, DoWorkEventArgs e)
```

```

 105:          {
```

```

 106:              try
```

```

 107:              {
```

```

 108:                  //server & client 已經連線完成
```

```

 109:                  Console.WriteLine("客戶端No.{0}已連結.", CurrentPlayerNum.ToString());
```

```

 110:                  Program.BoardCast("客戶端No." + CurrentPlayerNum.ToString() + "已連結.");
```

```

 111:                  while (PlayerSocket.Connected)
```

```

 112:                  {
```

```

 113:                      byte[] readBuffer = new byte[PlayerSocket.ReceiveBufferSize];
```

```

 114:                      int count = 0;
```

```

 115:
```

```

 116:                      if ((count = PlayerSocket.Receive(readBuffer)) > 0)
```

```

 117:                      {
```

```

 118:                          string clientRequest = Encoding.UTF8.GetString(readBuffer, 0, count);
```

```

 119:                          Program.BoardCast("客戶端No." + CurrentPlayerNum.ToString() + "：" + clientRequest);
```

```

 120:                          Console.WriteLine("客戶端No.{0}：{1}", CurrentPlayerNum.ToString(), clientRequest);
```

```

 121:                      }
```

```

 122:                  }
```

```

 123:              }
```

```

 124:              catch
```

```

 125:              {
```

```

 126:                  Program.BoardCast("客戶端No." + CurrentPlayerNum.ToString() + "已斷開連結.");
```

```

 127:                  Console.WriteLine("客戶端No.{0}已斷開連結.", CurrentPlayerNum.ToString());
```

```

 128:              }
```

```

 129:              finally
```

```

 130:              {
```

```

 131:                  PlayerSocket.Close();
```

```

 132:                  this.CurrentStatus = 0;
```

```

 133:                  Program.RemoveClient(this.CurrentPlayerNum);
```

```

 134:              }
```

```

 135:          }
```

```

 136:
```

```

 137:          public int SendToPlayer(string serverResponse)
```

```

 138:          {
```

```

 139:              if (this.CurrentStatus.Equals(1))
```

```

 140:              {
```

```

 141:                  try
```

```

 142:                  {
```

```

 143:                      byte[] sendBytes = Encoding.UTF8.GetBytes(serverResponse);
```

```

 144:                      return PlayerSocket.Send(sendBytes);
```

```

 145:                  }
```

```

 146:                  catch
```

```

 147:                  {
```

```

 148:                      return 0;
```

```

 149:                  }
```

```

 150:              }
```

```

 151:              else
```

```

 152:                  return 0;
```

```

 153:          }
```

```

 154:      }
```

```

 155:  }
```

Client端

```

   1:  using System;
```

```

   2:  using System.ComponentModel;
```

```

   3:  using System.Net;
```

```

   4:  using System.Net.Sockets;
```

```

   5:  using System.Text;
```

```

   6:
```

```

   7:  namespace MyClient
```

```

   8:  {
```

```

   9:      class Program
```

```

  10:      {
```

```

  11:          static void Main(string[] args)
```

```

  12:          {
```

```

  13:              string host = "127.0.0.1";
```

```

  14:              int port = 80;
```

```

  15:
```

```

  16:              Console.WriteLine("開始連接.");
```

```

  17:              IPAddress[] IPs = Dns.GetHostAddresses(host);
```

```

  18:
```

```

  19:              Socket mySocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
```

```

  20:
```

```

  21:              Console.WriteLine("正在連接至 {0}:{1} ...", host, port);
```

```

  22:              try
```

```

  23:              {
```

```

  24:                  mySocket.Connect(IPs[0], port);
```

```

  25:                  Console.WriteLine("已完成連接.");
```

```

  26:
```

```

  27:                  Client CC = new Client(mySocket);
```

```

  28:                  CC.DoCommunicate();
```

```

  29:
```

```

  30:                  while (true)
```

```

  31:                  {
```

```

  32:                      try
```

```

  33:                      {
```

```

  34:                          int i = mySocket.Send(Encoding.UTF8.GetBytes(Console.ReadLine()));
```

```

  35:                      }
```

```

  36:                      catch (Exception ex)
```

```

  37:                      {
```

```

  38:                          Console.WriteLine("與伺服器斷開連接.");
```

```

  39:                          Console.WriteLine(ex.Message);
```

```

  40:                          Console.WriteLine("按下任意鍵結束...");
```

```

  41:                          Console.ReadLine();
```

```

  42:                          break;
```

```

  43:                      }
```

```

  44:                  }
```

```

  45:              }
```

```

  46:              catch(Exception ex)
```

```

  47:              {
```

```

  48:                  Console.WriteLine("連接失敗.");
```

```

  49:                  Console.WriteLine(ex.Message);
```

```

  50:                  Console.WriteLine("按下任意鍵結束...");
```

```

  51:                  Console.ReadLine();
```

```

  52:              }
```

```

  53:          }
```

```

  54:      }
```

```

  55:      class Client
```

```

  56:      {
```

```

  57:          Socket mySocket;
```

```

  58:          public Client(Socket mySocket)
```

```

  59:          {
```

```

  60:              this.mySocket = mySocket;
```

```

  61:          }
```

```

  62:
```

```

  63:          public void DoCommunicate()
```

```

  64:          {
```

```

  65:              //產生 BackgroundWorker 負責處理每一個 socket client 的 reuqest
```

```

  66:              BackgroundWorker bgwSocket = new BackgroundWorker();
```

```

  67:              bgwSocket.DoWork += new DoWorkEventHandler(bgwSocket_DoWork);
```

```

  68:              bgwSocket.RunWorkerAsync();
```

```

  69:
```

```

  70:          }
```

```

  71:
```

```

  72:          private void bgwSocket_DoWork(object sender, DoWorkEventArgs e)
```

```

  73:          {
```

```

  74:              //server & client 已經連線完成
```

```

  75:              while (mySocket.Connected)
```

```

  76:              {
```

```

  77:                  byte[] readBuffer = new byte[mySocket.ReceiveBufferSize];
```

```

  78:                  int count = 0;
```

```

  79:                  if ((count = mySocket.Receive(readBuffer)) != 0)
```

```

  80:                  {
```

```

  81:                      string clientRequest = Encoding.UTF8.GetString(readBuffer, 0, count);
```

```

  82:                      Console.WriteLine(clientRequest);
```

```

  83:                  }
```

```

  84:              }
```

```

  85:          }
```

```

  86:      }
```

```

  87:  }
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* [C#](/jakeuj/Tags?qq=C%23)
* [Socket](/jakeuj/Tags?qq=Socket)

* [回首頁](/jakeuj)

---

*本文章從點部落遷移至 Writerside*
