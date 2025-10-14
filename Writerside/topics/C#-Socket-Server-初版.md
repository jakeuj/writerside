# C# Socket Server 初版

> **原文發布日期:** 2012-04-11
> **原文連結:** https://www.dotblogs.com.tw/jakeuj/2012/04/11/71413
> **標籤:** 無

---

C# Socket Server 初版

因緣際會需要學習一下，這是至少可以跑的版本，還在想怎麼改比較好，請不吝賜教，感謝！

## Server 端

```csharp
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace MyServer
{
    class Program
    {
        // 宣告客戶端清單
        public static List<Client> ClientList;

        public static void Main(string[] args)
        {
            //產生 BackgroundWorker 負責處理每一個 socket client 的 reuqest
            BackgroundWorker bgwSocket = new BackgroundWorker();
            bgwSocket.DoWork += new DoWorkEventHandler(bgwSocket_DoWork);
            bgwSocket.RunWorkerAsync();
            while (true)
            {
                BoardCast("伺服器端：" + Console.ReadLine());
            }
        }

        private static void bgwSocket_DoWork(object sender, DoWorkEventArgs e)
        {
            // 設定連線接聽阜值
            const int ServerPort = 80;

            // 設定半開連接數
            const int BackLog = 10;

            // 初始化客戶端清單
            ClientList = new List<Client>();

            // 初始化客戶端序列號
            int PlayerNum = 0;

            // 建立接聽Socket
            Socket ListenSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            // 綁定接聽Socket的IP與Port
            ListenSocket.Bind(new IPEndPoint(IPAddress.Any, ServerPort));

            // 開始接聽
            ListenSocket.Listen(BackLog);

            // 輸出伺服器端起始訊息
            Console.WriteLine("開始接聽客戶端連線...");

            // 持續等待客戶端接入
            while (true)
            {
                ClientList.Add(new Client(PlayerNum, ListenSocket.Accept()));
                PlayerNum++;
            }
        }

        public static void BoardCast(string serverResponse)
        {
            foreach (Client myClient in Program.ClientList)
            {
                myClient.SendToPlayer(serverResponse);
                Console.WriteLine("廣播訊息：{0}", serverResponse);
            }
        }

        public static void RemoveClient(int PlayerNum)
        {
            foreach (Client myClient in Program.ClientList)
            {
                if (myClient.CurrentPlayerNum.Equals(PlayerNum))
                {
                    Program.ClientList.Remove(myClient);
                    break;
                }
            }
        }
    }

    class Client
    {
        public int CurrentPlayerNum { get; set; }
        public Socket PlayerSocket { get; set; }
        public int CurrentStatus { get; set; }

        public Client(int PlayerNum, Socket mySocket)
        {
            this.CurrentPlayerNum = PlayerNum;
            this.PlayerSocket = mySocket;
            this.CurrentStatus = 1;
            DoCommunicate();
        }

        public void DoCommunicate()
        {
            //產生 BackgroundWorker 負責處理每一個 socket client 的 reuqest
            BackgroundWorker bgwSocket = new BackgroundWorker();
            bgwSocket.DoWork += new DoWorkEventHandler(bgwSocket_DoWork);
            bgwSocket.RunWorkerAsync();
        }

        private void bgwSocket_DoWork(object sender, DoWorkEventArgs e)
        {
            try
            {
                //server & client 已經連線完成
                Console.WriteLine("客戶端No.{0}已連結.", CurrentPlayerNum.ToString());
                Program.BoardCast("客戶端No." + CurrentPlayerNum.ToString() + "已連結.");
                while (PlayerSocket.Connected)
                {
                    byte[] readBuffer = new byte[PlayerSocket.ReceiveBufferSize];
                    int count = 0;

                    if ((count = PlayerSocket.Receive(readBuffer)) > 0)
                    {
                        string clientRequest = Encoding.UTF8.GetString(readBuffer, 0, count);
                        Program.BoardCast("客戶端No." + CurrentPlayerNum.ToString() + "：" + clientRequest);
                        Console.WriteLine("客戶端No.{0}：{1}", CurrentPlayerNum.ToString(), clientRequest);
                    }
                }
            }
            catch
            {
                Program.BoardCast("客戶端No." + CurrentPlayerNum.ToString() + "已斷開連結.");
                Console.WriteLine("客戶端No.{0}已斷開連結.", CurrentPlayerNum.ToString());
            }
            finally
            {
                PlayerSocket.Close();
                this.CurrentStatus = 0;
                Program.RemoveClient(this.CurrentPlayerNum);
            }
        }

        public int SendToPlayer(string serverResponse)
        {
            if (this.CurrentStatus.Equals(1))
            {
                try
                {
                    byte[] sendBytes = Encoding.UTF8.GetBytes(serverResponse);
                    return PlayerSocket.Send(sendBytes);
                }
                catch
                {
                    return 0;
                }
            }

            else
                return 0;
        }
    }
}
```

## Client 端

```csharp
using System;
using System.ComponentModel;
using System.Net;
using System.Net.Sockets;
using System.Text;

namespace MyClient
{
    class Program
    {
        static void Main(string[] args)
        {
            string host = "127.0.0.1";
            int port = 80;

            Console.WriteLine("開始連接.");
            IPAddress[] IPs = Dns.GetHostAddresses(host);

            Socket mySocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            Console.WriteLine("正在連接至 {0}:{1} ...", host, port);
            try
            {
                mySocket.Connect(IPs[0], port);
                Console.WriteLine("已完成連接.");

                Client CC = new Client(mySocket);
                CC.DoCommunicate();

                while (true)
                {
                    try
                    {
                        int i = mySocket.Send(Encoding.UTF8.GetBytes(Console.ReadLine()));
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine("與伺服器斷開連接.");
                        Console.WriteLine(ex.Message);
                        Console.WriteLine("按下任意鍵結束...");
                        Console.ReadLine();
                        break;
                    }
                }
            }
            catch(Exception ex)
            {
                Console.WriteLine("連接失敗.");
                Console.WriteLine(ex.Message);
                Console.WriteLine("按下任意鍵結束...");
                Console.ReadLine();
            }
        }
    }

    class Client
    {
        Socket mySocket;

        public Client(Socket mySocket)
        {
            this.mySocket = mySocket;
        }

        public void DoCommunicate()
        {
            //產生 BackgroundWorker 負責處理每一個 socket client 的 reuqest
            BackgroundWorker bgwSocket = new BackgroundWorker();
            bgwSocket.DoWork += new DoWorkEventHandler(bgwSocket_DoWork);
            bgwSocket.RunWorkerAsync();
        }

        private void bgwSocket_DoWork(object sender, DoWorkEventArgs e)
        {
            //server & client 已經連線完成
            while (mySocket.Connected)
            {
                byte[] readBuffer = new byte[mySocket.ReceiveBufferSize];
                int count = 0;
                if ((count = mySocket.Receive(readBuffer)) != 0)
                {
                    string clientRequest = Encoding.UTF8.GetString(readBuffer, 0, count);
                    Console.WriteLine(clientRequest);
                }
            }
        }
    }
}
```

![](https://card.psnprofiles.com/1/jakeuj.png)

PS5

* C#
{ignore-vars="true"}
* Socket

* 回首頁

---

*本文章從點部落遷移至 Writerside*
