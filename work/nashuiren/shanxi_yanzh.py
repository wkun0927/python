# 请求服务器上的蓝图进行测试
import requests


def send_post_image_nsfw(img1_path, url):
    """
    :param img1:
    :return:
    """
    files = {
        'img1_path': open(img1_path, 'rb').read()
    }
    html = requests.post(url, files=files).text
    return html


def get():
    url = 'http://192.168.3.236:5001/tax/shanxi'
    path = './0.jpg'
    html = send_post_image_nsfw(path, url)
    return html


if __name__ == '__main__':
    a = get()
    a = eval(a)
    print(a, type(a))
