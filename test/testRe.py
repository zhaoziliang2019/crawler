# 正则表达式：字符串模式（判断字符串是否符合一定的标准）
import re

pat = re.compile("AA")  # 此处的AA是正则表达式，用来去验证其他的字符串
# m = pat.search("AACBAA")  # search 字符串被校验的内容
# print(m)

m = re.search("asd", "Aasd")
print(m)

m = re.findall("a", "ASDaDFGAa")
print(m)

print(re.findall("[A-Z]+", "ASDaDFGAa"))

# sub
print(re.sub("a", "A", "abcdcasd"))  # 找到a用A替换
