# bot_service
a tg bot with fastapi service




#### 走 HTTP 代理
```
git config --global http.proxy "http://127.0.0.1:8080"
git config --global https.proxy "http://127.0.0.1:8080"

```

#### 走 socks5 代理（如 小飞机 or V2xxxx）
```
git config --global http.proxy "socks5://127.0.0.1:1080"
git config --global https.proxy "socks5://127.0.0.1:1080"
```
#### 取消设置
```
git config --global --unset http.proxy
git config --global --unset https.proxy
```