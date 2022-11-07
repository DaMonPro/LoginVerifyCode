# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from phone_num import phone_num
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def delete_report_file():
    if os.path.isfile('MetchantReport.txt'):
        os.remove('MetchantReport.txt')

def write_log(country='', phone='', none_country=False):
    with open('MetchantReport.txt', 'a+') as f:
        if none_country:
            f.write(f'国家：{country}电话号码为空 \n')
        else:
            f.write(f'无法正确识别，国家：{country},手机号码：{phone} \n')

def click_country_select():
    # 点击国家下拉框，弹出下拉框
    country_select = driver.find_element_by_css_selector("input[placeholder='Country']")
    # 判断国家下拉框是否可见
    country_display = driver.find_element_by_css_selector("ul.el-scrollbar__view")
    if not country_display.is_displayed():
        # 如果该div不可见，就点击国家下拉框弹出国家下拉框
        country_select.click()
    # 页面显示等待下拉框弹出
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul.el-scrollbar__view')))


if __name__ == '__main__':
    try:
        # 首先删除旧的报告文件
        delete_report_file()

        driver = webdriver.Chrome()
        driver.get(url='http://buy.testonline.pundix.com/#/?path=test')
        # 点击国家下拉框
        click_country_select()
        # 获取国家列表
        ul_len = len(driver.find_elements(By.CSS_SELECTOR, 'li.el-select-dropdown__item'))
        for i in range(ul_len):
            # 点击国家下拉框
            click_country_select()

            # 获取国家名称
            li = driver.find_element_by_css_selector(f"ul.el-scrollbar__view li:nth-child({i+2})")
            country_name = li.text

            # 如果没有该国家的记录，记录到输出报告中
            if not phone_num.get(country_name):
                write_log(country=country_name, none_country=True)
            else:
                for phone in phone_num[country_name]:
                    # 弹出国家下拉框
                    click_country_select()
                    # 选择国家
                    li = driver.find_element_by_css_selector(f"ul.el-scrollbar__view li:nth-child({i+2})")
                    li.click()

                    print(f'country:{country_name}')
                    print(f'phone:{phone}')
                    a = driver.find_element_by_css_selector('input[placeholder="Phone number"]')
                    # 输入电话
                    a.send_keys(phone)
                    # 点击发送短信按钮
                    driver.find_element_by_xpath('//*[@id="pane-phone"]/div/form/div[3]/button').click()
                    # 根据页面是否出现电话号码格式不正确提示，判断有没有正确该国家又没正确格式化电话,True为页面存在该元素
                    element_exist = True
                    try:
                        driver.find_element_by_css_selector('div.el-form-item__error')
                    except NoSuchElementException:
                        element_exist = False
                    # element_exist = False,说明页面元素不存在，该电话号码通过测试
                    # element_exist = True,说明页面元素存在，该电话号码不通过测试
                    if element_exist:
                        write_log(country=country_name, phone=phone)

                    # 直接刷新页面，避免等待60秒才能点击发送短信按钮
                    driver.refresh()

    finally:
        driver.quit()
