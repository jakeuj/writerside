# Redis

ABP 預設使用 Redis 作為分布式快取。

## 安装
使用 Docker 安装 Redis

```bash
docker run -d --name redis -p 6379:6379 redis
```

- 注意 Docker 基本指令並不能讓人連進去，記得一定要加上 -p 之類的

![redis.png](redis.png){style="block"}

## REF
- [Redis Server 架設心得筆記](https://dotblogs.com.tw/jakeuj/2015/12/24/redis)
- [redis.yml](https://peihsinsu.gitbooks.io/docker-note-book/content/redis_user_guide.html)