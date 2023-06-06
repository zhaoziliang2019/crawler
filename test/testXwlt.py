import xlwt

wookbook=xlwt.Workbook(encoding="utf-8")#创建workbook对象
worksheet=wookbook.add_sheet('sheet1')#创建工作表
worksheet.write(0,0,'hello')#写入数据，第一行参数行，第二个参数列，第三个参数内容
wookbook.save('student.xls')#保存数据表

