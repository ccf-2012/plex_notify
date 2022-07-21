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


## 配合torcp使用
* torcp 2022.7.21 版本加入 `--after-copy-script` 参数，可在完成一个媒体项目的 link/move 之后，对目标文件夹执行一个脚本。
* torcp传出的是一个在 Plex/Emby 根目录下面的相对目录
### 如果直接在本地硬盘上运行torcp，或在GD上使用`--move-run`运行torcp，方法如下：
1. 编辑一个 `plex_notify.sh`，在torcp中有示例，内容如下，修改其中除 `-f "$1"` 之外的参数：
```sh
#!/bin/bash#
PLEX_ROOT_DIR=/gd1/emby/
echo PLEX_ROOT_DIR"$1"
python3 /home/ccf2012/plex_notify/plex_notify.py -l 2 -f PLEX_ROOT_DIR"$1" -s http://plex.server.ip:32400 -t plex-token
```
2. 在原 `rcp.sh` 中调用 torcp 的地方，加入新参数 `--after-copy-script /home/ccf2012/torcp/plex_notify.sh`

* 如此，在torcp完成改名硬链/移动后，将调用plex_notify通知plex对指定的新加项目进行处理
* 注1：torcp应以源码方式添加，即以 `python3 tp.py` 方式调用


### 如果torcp在本地完成改名硬链后，再上传gd的，则：
1. 编辑一个 `exp.sh`，在其中将 torcp 输出的目标文件夹内容保存到一个shell变量中，`exp.sh` 内容如下：
```sh
#!/bin/bash

# 此处应为运行Plex Server的那台机器所识别的Plex媒体库路径，在TV/Movie之上的那一层目录，结尾应有'/'
PLEX_ROOT_DIR=/gd1/emby/
export CURRENT_PLEX_ITEM="PLEX_ROOT_DIR$1"
```
2. 在原 `rcp.sh` 中，对torcp命令加入`--after-copy-script`，并在上传完成后，运行 `plex_notify.py`, 例如：
```sh
# example 2: rclone copy to gd drive
python /home/ccf2012/torcp/tp.py "$1" -d "/home/ccf2012/emby/$2/" -s --tmdb-api-key <tmdb api key> --lang cn,jp
rclone copy "/home/ccf2012/emby/$2/"  gd:/media/148/emby/
rm -rf "/home/ccf2012/emby/$2/"

echo $CURRENT_PLEX_ITEM
sleep 30
python3 /home/ccf2012/plex_notify/plex_notify.py -l 2 -f "$CURRENT_PLEX_ITEM" -s http://plex.server.ip:32400 -t plex-token
```

* 一个位置上传gd后，各地rclone mount的盘，不会及时更新响应，脚本中加了 `sleep 30` 也并不能保证，各位使用时斟酌修改

