import re

from bs4 import BeautifulSoup

file = open("./douban.html", "rb")
html = file.read()
bs = BeautifulSoup(html, "html.parser")
print(bs.title.string)
print(bs.a.contents)
print(bs.head.contents[1])

# 文档的搜索
# 字符串过滤：会查找与字符串完全匹配的内容
# t_list=bs.findAll("a")
# print(t_list)

# 正则表达式搜索：使用search（）方法匹配内容
# t_list = bs.findAll(re.compile("a"))
# print(t_list)


# 方法：传入一个函数（方法），根据函数要求来搜索
# def name_is_exists(tag):
#     return tag.has_attr("name")
#
#
# t_list = bs.findAll(name_is_exists)
# print(t_list)

# kwargs 参数
# t_list = bs.findAll(class_=True)
#
# for item in t_list:
#     print(item)

# t_list = bs.findAll(href="https://beian.miit.gov.cn/")
#
# for item in t_list:
#     print(item)

# t_list = bs.findAll(text=re.compile("\d"))
#
# for item in t_list:
#     print(item)

# t_list = bs.findAll("a",limit=3)
#
# for item in t_list:
#     print(item)

# css选择器
print(bs.select('title'))
print(bs.select(".mnav"))
t_list=bs.select("a[class]")
for item in t_list:
    print(item)
