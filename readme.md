# 项目简介

## 一、网站技术

网站前端使用到了layui、jQuery、Bootstrap框架，以及echaets实现数据可视化。

文章编辑器使用markdown，评论留言使用layui富文本实现。

后端使用python语言，django框架开发。

数据库主要使用MySQL，缓存使用Redis。

网站部署在阿里云服务器，使用docker部署，通过nginx反向代理，实现动静分离，css、js、字体、图片等静态资源使用七牛OSS对象存储，并通过华为CDN提供加速服务，动态资源由Django解析并处理。

整个站点流量通过调用百度统计的api接口实现流量统计分析。

## 二、网站架构

![](https://oss.cuiliangblog.cn/markdown/2020_10_28_12_42_03_182074.png)

## 三、功能模块

>博客网站按照用户身份权限共划分为网站前台、用户管理后台、管理员后台三部分，总共二十八个模块。

### 1. 前台模块

所有用户都可以通过网站前台浏览到博文、轮播广告、最新博文、热点博文、文章点赞等功能。

- 首页

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-14-42.png)

- 文章分类

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-15-21.png)

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-15-41.png)

- 笔记目录

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-16-03.png)

- 时间轴

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-16-18.png)

- 留言板

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-16-35.png)

- 关于页

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-16-52.png)

- 文章正文

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-17-40.png)

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-18-06.png)

- 笔记正文

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-19-08.png)

- 用户登录

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-33-47.png)

- 用户注册

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-34-03.png)

- 忘记密码

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-34-19.png)

- 注销登录

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-33-27.png)

### 2. 用户管理模块

用户注册后，通过登陆的用户可以进行发表文章评论、收藏文章、发表留言以及回复留言评论操作，在个人中心可以查看自己的浏览记录，收藏记录，点赞记录，还可以修改个人信息、修改密码、修改邮箱等功能。

- 个人中心首页

![](https://oss.cuiliangblog.cn/markdown/2020_12_26_23_45_50_607355.jpg)

- 修改信息

![](https://oss.cuiliangblog.cn/markdown/2020_12_09_10_08_57_273306.png)

- 修改密码

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-37-52.png)

- 修改邮箱

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-38-06.png)

- 浏览记录

![](https://oss.cuiliangblog.cn/markdown/2020_12_09_10_12_21_292661.png)

- 收藏记录

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-39-09.png)

- 评论记录

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-39-23.png)

- 留言记录

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-39-47.png)

### 3. 后台模块

后台博客管理系统是为管理员管理博客而设置的，管理员可以查看网站流量数据，查看注册用户信息，可以对文章进行发布、修改、删除操作。以及对文章分类，标签管理。还有设置博客网站的轮播图、友情链接等内容。

- 流量统计

![](https://oss.cuiliangblog.cn/markdown/2020_12_26_23_52_32_791830.jpg)

- 文章发布

![](https://oss.cuiliangblog.cn/markdown/2020_12_09_12_21_06_545641.png)

- 文章列表

![](https://oss.cuiliangblog.cn/markdown/2020_12_09_12_21_55_166338.png)

- 文章分类

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-45-12.png)

- 文章标签

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-45-50.png)

- 文章评论

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-46-25.png)

- 笔记发布

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-48-44.png)

- 笔记列表

![](https://oss.cuiliangblog.cn/markdown/2020_12_09_12_22_36_497601.png)

- 笔记名称

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-48-54.png)

- 目录编排

![](https://oss.cuiliangblog.cn/markdown/2020_12_09_12_22_59_876194.png)

- 笔记评论

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-49-18.png)

- 网站配置

![](https://oss.cuiliangblog.cn/markdown/2020_12_09_12_23_22_812681.png)

- 博主信息

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-53-01.png)

- 关于页面

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-53-13.png)

- 轮播管理

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-53-42.png)

- 友链管理

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-53-58.png)

- 留言管理

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-54-11.png)

- 用户管理

![](https://oss.cuiliangblog.cn/markdown/Snipaste_2021-06-19_23-54-24.png)

## 四、部署流程

### 1. 代码目录准备

```bash
[root@aliyun root]# cd /opt
# git记住密码
[root@aliyun opt]# vim ~/.git-credentials
https://cuiliang0302:cl147963@gitee.com
[root@aliyun opt]# git config --global credential.helper store
# 拉取项目代码
[root@aliyun opt]# git clone https://gitee.com/cuiliang0302/myblog.git
# 初始化项目
[root@aliyun opt]# pip3 install click tinify
[root@aliyun opt]# chmod u+x /opt/myblog/other/update.sh 
[root@aliyun opt]# sh /opt/myblog/other/update.sh
```

### 2. MySQL部署

```bash
[root@aliyun opt]# mkdir -p /opt/docker/mysql
[root@aliyun opt]# cd /opt/docker/mysql/
[root@aliyun mysql]# docker run -p 3306:3306 --name mysql -v $PWD/conf:/etc/mysql/conf.d -v $PWD/logs:/logs -v $PWD/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=password -d --restart=always mysql
```

### 3. MySQL导入数据

```bash
# 拷贝数据库文件
[root@aliyun mysql]# docker cp myblog/other/myblog.sql mysql:/root
[root@aliyun mysql]# docker exec -it mysql bash
root@3bd762759930:/# mysql -u root -p

# 设置远程连接数据库权限(按需)
mysql> use mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> grant all privileges on *.* to 'root'@'%';
Query OK, 0 rows affected (0.00 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.01 sec)

# 创建数据库
mysql> CREATE DATABASE myblog DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
Query OK, 1 row affected, 2 warnings (0.01 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| myblog             |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)

# 导入数据
mysql> use myblog;
Database changed
mysql> source /root/myblog.sql;
mysql> show tables;
```

### 4. redis部署

```bash
[root@aliyun docker]# docker run --name redis -p 6379:6379 -d --restart=always redis --requirepass password
fe24cb38242ed2f1c8c7340fa1ce05f39c8fc351a7a96506c43dff41ca0774bb
[root@aliyun docker]# docker exec -it redis redis-cli
127.0.0.1:6379> auth CuiLiang@0302
OK
```

### 5. django部署

> 运行前记得将setting.py密码密钥等信息填写自己的内容。

```bash
[root@aliyun docker]# cd /opt/myblog/
# 构建镜像并运行
[root@aliyun myblog]# docker build -t myblog:v1 .
# 测试开发环境
[root@aliyun myblog]# docker run --name myblog -p 8000:8000 -v /opt/myblog:/opt/myblog -d --restart=always --link mysql --link redis myblog:v1
[root@aliyun myblog]# curl 127.0.0.1:8000
# 线上环境
[root@aliyun myblog]# docker run -d --name myblog -p 8997:8997 -v /opt/myblog:/opt/myblog -d --restart=always --link mysql --link redis myblog:v1
```

### 6. nginx部署

```bash
# 将项目下的other/nginx移动至/opt/docker下
[root@aliyun myblog]# cp -R other/nginx/ /opt/docker/
[root@aliyun myblog]# cd /opt/docker/
[root@aliyun docker]# tree nginx/
nginx/
├── conf
│   └── nginx.conf
└── ssl
    ├── cdn.cuiliangblog.cn_chain.crt
    ├── cdn.cuiliangblog.cn_key.key
    ├── www.cuiliangblog.cn_chain.crt
    └── www.cuiliangblog.cn_key.key
[root@aliyun docker]# docker run --name nginx -p 80:80 -p 443:443 -v /opt/docker/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v /opt/docker/nginx/ssl:/etc/ssl -v /opt/myblog:/opt/myblog -v /opt/docker/nginx/log:/var/log/nginx -d --link myblog --restart=always nginx
```

* 修改hosts文件，分别访问测试

  https://www.cuiliangblog.cn/

  https://cdn.cuiliangblog.cn/media/

  https://cdn.cuiliangblog.cn/static/



## 五、运维

### 1. 壁纸定时更换

```bash
[root@aliyun ~]# chmod u+x /opt/myblog/other/make_bgc.py 
[root@aliyun ~]# crontab -e
* 3 * * * /usr/bin/python3 /opt/myblog/other/make_bgc.py >/dev/null
```

### 2. 数据库定时备份

```bash
[root@aliyun ~]# chmod u+x /opt/myblog/other/db_backup.sh
[root@aliyun ~]# crontab -e
* 4 * * * /usr/bash /opt/myblog/other/db_backup.sh >/dev/null
```
