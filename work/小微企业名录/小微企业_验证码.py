# 请求服务器上的蓝图进行测试
import requests
import time


def send_post_image_nsfw(img1_path, img_path2, url):
    """
    :param img1:
    :return:
    """
    files = {
        'img1_path': open(img1_path, 'rb').read(),
        'img2_path': open(img_path2, 'rb').read()
    }
    html = requests.post(url, files=files).text
    return html


def get():
    url = 'http://192.168.3.236:5001/xiaowei/slider'
    img_path1 = './0.webp'
    img_path2 = './1.webp'
    html = send_post_image_nsfw(img_path1, img_path2, url)
    return html


if __name__ == '__main__':
    a = get()
    print(a)
