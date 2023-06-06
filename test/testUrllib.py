# -*- codeing = uft-8 -*-

import urllib.request, urllib.parse, urllib.error

# response=urllib.request.urlopen("http://www.baidu.com")
# print(response.read().decode('utf-8'))#对获取到的网页源码进行utf-8解码

# 获取一个post请求httpbin.org
# try:
#     data = bytes(urllib.parse.urlencode({"hello": "world"}), encoding="utf-8")
#     response = urllib.request.urlopen("http://httpbin.org/post", data=data, timeout=5)
#     print(response.read())
# except urllib.error.URLError as e:
#     print("time out !")

url = "https://www.douban.com"
# url="http://httpbin.org/post"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}
data = urllib.parse.urlencode({'name': 'douban'})
req = urllib.request.Request(url=url, headers=headers, method="POST", data=bytes(data, encoding="utf-8"))
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))
