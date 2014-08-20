## 模拟登录百度账号，批量下载百度音乐。 ##

> 本工具采用python 2.7.3,需要pyqt、BeautifulSoup的支持。

本工具首先模拟登录百度，登录成功后，会解析百度新歌榜或者百度热歌榜，之后形成歌曲列表，以界面的形式展现处理。 可以下载单个歌曲、选择下载多个歌曲，或者复制所有歌曲链接，到迅雷中新建下载组打包下载歌曲。

> 使用步骤：

 

 1. 首先找到settings.py文件，在文件开始位置，配置你的账号、密码及新歌榜或热歌榜的地址 username = "your baidu acount" #配置你的百度账号 password = "your baidu password" #配置你的百度密码
musiclistUrl = "http://music.baidu.com/top/dayhot" #热歌 或者http://music.baidu.com/top/new #新歌
 2. 直接运行spiderMan.py即可，采用多线程，网速不给力的情况下最多8、9秒即可爬完新歌榜前100首，当然有些歌曲是不可以免费下载的。
