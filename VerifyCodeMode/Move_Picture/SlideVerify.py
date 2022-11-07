import base64,random,time
from PIL import Image
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

username = "13632548845"
password = "Abc123456"

class SlideVerify:

    def __init__(self):
        self.url = "https://wallet.test.hoogeek.com/login"
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.url)
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div[1]/div[2]/form/div[1]/div/div/div[2]/input').send_keys(username)
        self.driver.find_element_by_css_selector("input[type='password']").send_keys(password)
        time.sleep(2)
        self.driver.find_element_by_css_selector("button[type='submit']").click()

    # 判断颜色是否相近
    def is_similar_color(self, x_pixel, y_pixel):  # 传入完整图片和缺口图片的像素
        for i, pixel in enumerate(x_pixel):
            if abs(y_pixel[i] - pixel) > 50:  # 如果两张图片差的绝对值大于50的话颜色不相近
                return False
        return True

    # 通过js命令返回图片
    def save_img(self, img_name, class_name):
        getImgJS = 'return document.getElementsByClassName("'+class_name+'")[0].toDataURL("image/png")'
        img = self.driver.execute_script(getImgJS)
        base64_data_img = img[img.find(',') + 1:]
        image_base = base64.b64decode(base64_data_img)
        file = open(img_name, 'wb')
        file.write(image_base)
        file.close()

    # 计算滑动距离
    def get_offset_distance(self, cut_image, full_image):
        for x in range(cut_image.width):
            for y in range(cut_image.height):
                cpx = cut_image.getpixel((x, y))
                fpx = full_image.getpixel((x, y))
                if not self.is_similar_color(cpx, fpx):
                    img = cut_image.crop((x, y, x + 50, y + 40))
                    img.save("//img/gap.png") # 保存一下计算出来位置图片，看看是不是缺口部分
                    return x
    # 开始移动
    def start_move(self, distance):
        element = self.driver.find_element_by_xpath('//div[@class="geetest_slider_button"]')
        # 这里就是根据移动进行调试，计算出来的位置不是百分百正确的，加上一点偏移
        distance -= element.size.get('width') / 2
        distance += 25
        # 按下鼠标左键,click_and_hold点击不放，move_by_offset按坐标移动，release鼠标释放
        ActionChains(self.driver).click_and_hold(element).perform()
        time.sleep(0.5)
        while distance > 0:
            if distance > 10:
                span = random.randint(5, 8) # 如果距离大于10，就让他移动快一点
            else:
                span = random.randint(2, 3) # 快到缺口了，就移动慢一点
            ActionChains(self.driver).move_by_offset(span, 0).perform()
            distance -= span
            time.sleep(random.randint(10,50)/100)
        ActionChains(self.driver).move_by_offset(distance, 1).perform()
        ActionChains(self.driver).release(element).perform()

    # 进入模拟拖动流程
    def slide_verify(self):
        # 等待验证框的出现
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//canvas[@class="geetest_canvas_slice geetest_absolute"]')))

        # 保存图片方便查看
        self.save_img('//img/full.jpg', 'geetest_canvas_fullbg')  # 输出完整图片
        self.save_img('//img/cut.jpg', 'geetest_canvas_bg')  # 输出有缺口的图片
        full_image = Image.open('full.jpg')
        cut_image = Image.open('cut.jpg')

        # 根据两个图片计算距离
        distance = self.get_offset_distance(cut_image, full_image)

        # 开始移动
        self.start_move(distance)

        # 判断是否验证成功
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_result_icon geetest_success"]')))
            print("验证成功")
        except TimeoutException:
            time.sleep(2)
            self.slide_verify()

if __name__ == '__main__':
    SlideVerify().slide_verify()