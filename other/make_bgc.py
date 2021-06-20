#! /usr/bin/python3
# 定时更新登录页背景图

import os
import os.path
import os.path
import time
import urllib.request
import click
import tinify
import requests


# 请求网页，跳转到最终 img 地址
def get_img_url(raw_img_url="https://area.sinaapp.com/bingImg/"):
    r = requests.get(raw_img_url)
    img_url = r.url  # 得到图片文件的网址
    print('图片下载地址：', img_url)
    return img_url


# 保存图片到磁盘文件夹dirname中
def save_img(img_url, dirname):
    try:
        if not os.path.exists(dirname):
            print('文件夹', dirname, '不存在，重新建立')
            # os.mkdir(dirname)
            os.makedirs(dirname)
        # 获得图片文件名，包括后缀
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        filename = date + '.jpg'
        # 拼接目录与文件名，得到图片路径
        filepath = os.path.join(dirname, filename)
        # 下载图片，并保存到文件夹中
        print("保存地址:", filepath)
        urllib.request.urlretrieve(img_url, filepath)
    except IOError as e:
        print('文件操作失败', e)
    except Exception as e:
        print('错误 ：', e)
    print(filepath, "保存成功!")
    return filepath


# 压缩图片
def zip_img(in_file, out_file):
    tinify.key = "sX1FG8BMyWSlxBx5bKGHyZ8XBdqYTBTs"
    source = tinify.from_file(in_file)  # 压缩指定文件
    resized = source.resize(
        method="fit",
        width=1024,
        height=768
    )
    resized.to_file(out_file)
    print(out_file, "压缩完成！")


def main():
    # 下载保存图片
    dirname = "/opt/bgc"
    img_url = get_img_url()
    file_path = save_img(img_url, dirname)

    # 压缩图片

    img_dir = "/opt/myblog/static/images"  # 输出目录
    img_name = 'bg-img.jpg'
    img_path = img_dir+"/"+img_name
    zip_img(file_path, img_path)


if __name__ == '__main__':
    main()
