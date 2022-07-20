# plex_notify
* 当有新文件/文件夹添加到库目录下时，通知plex进行更新
  

## 安装
1. 安装依赖库
```sh
pip install plexapi
```
2. 下载代码
```sh 
git clone https://github.com/ccf-2012/plex_notify.git
```


## 取得Plex的auth token
* https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/


## 使用说明
```sh
python3 plex_notify.py -h
usage: plex_notify.py [-h] -l LIBRARY -f FILEPATH -s PLEX -t TOKEN

notify plex server to add a file/folder.

optional arguments:
  -h, --help            show this help message and exit
  -l LIBRARY, --library LIBRARY
                        the plex library index.
  -f FILEPATH, --filepath FILEPATH
                        the file/foler path to add.
  -s PLEX, --plex PLEX  the plex server url, ex: http://plex.server.ip:32400
  -t TOKEN, --token TOKEN
                        the plex auth token, ref: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-
                        plex-token/
```

## 示例
```sh
python3 plex_notify.py -l 2 -f '/gd124/media/148/emby/TV/cn/庭外 (2022)' -s http://plex.server.ip:32400 -t plex-token
```
* 以上代码表示，在 `http://plex.server.ip:32400` 库中的第 `2` 个库中，添加 `/gd124/media/148/emby/TV/cn/庭外 (2022)` 文件夹中的内容
* 其中的 `2` 为 Plex 媒体库中的称作 `资料库` 的条目序号，在Plex网页端后台，查看媒体库，按顺序从 `0` 开始编号 
* 脚本运行后， 在Plex网页端可以看到刷新标志开始旋转，旋转停止后，媒体库第 `2` 目录中会出现此新增条目


媒体库中的资料库可以使用名称，如
```sh
python3 plex_notify.py -l 电影 -f '/gd124/media/148/emby/TV/cn/庭外 (2022)' -s http://plex.server.ip:32400 -t plex-token
```

## 需要注意
1. 以 `-f` 所指向的路径，应在相应媒体库资料库已有目录之下，需使用者自行保证，否则无法添加成功
2. 代码新鲜出来，未经充分测试
