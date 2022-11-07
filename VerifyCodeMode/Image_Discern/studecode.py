
from selenium import webdriver
import pytesseract.pytesseract
from PIL import Image

Url = "http://www.stegd.edu.cn/selfec/login/login.jsp"

wb = webdriver.Chrome()
wb.get(Url)
wb.set_window_size(2200,2200)

elem_user = wb.find_element_by_name('account')
elem_psw = wb.find_element_by_name('password')
elem_code = wb.find_element_by_name('addcode')

elem_user.send_keys('030419303525')
elem_psw.send_keys('xgq123456')
elem_code.click()

path1 = "./Image/code1/image.png" #用于存放验证码的页面图片
path2 ='./Image/code2/image.png' #用于存放截取后的图
wb.save_screenshot(path1)
imgelement = wb.find_element_by_name('randomImage')
locations = imgelement.location #获取坐标
sizes = imgelement.size  #获取长度、宽度
print(locations,sizes)

#计算出需要截图的长宽、高度
rangle = (int(locations['x']),int(locations['y']),int(locations['x'] + sizes['width']),int(locations['y'] + sizes['height']))
img = Image.open(str(path1))
jpg = img.crop(rangle) #进行截取验证码位置图片
print(jpg.size)
jpg.save(path2) #保存截取后的图片

image = Image.open(str(path2))
image.load()
image.show()
code = pytesseract.image_to_string(image)
print("图片内容识别为:%s"%code)
elem_code.send_keys(code)

wb.quit()
