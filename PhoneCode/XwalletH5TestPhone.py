# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from phone_num import phone_num
import os
from time import sleep

def delete_report_file():
    if os.path.isfile('XwalletReport.txt'):
        os.remove('XwalletReport.txt')

def write_log(country='', phone='', none_country=False):
    with open('XwalletReport.txt', 'a+') as f:
        if none_country:
            f.write(f'国家：{country}电话号码为空 \n')
        else:
            f.write(f'无法正确识别，国家：{country},手机号码：{phone} \n')

if __name__ == '__main__':
    try:
        # 首先删除旧的报告文件
        delete_report_file()

        driver = webdriver.Chrome()
        driver.get(url='https://xwallettest.pundix.com/#/beforLogin')
        # 点击注册
        sleep(1)
        register = driver.find_element(By.XPATH,"//*[@id='app']/div[1]/div/div[3]/div[2]")
        register.click()
        sleep(1)
        phoneregister = driver.find_element(By.CSS_SELECTOR,'.fromLabel > a:nth-child(3)')
        phoneregister.click()
        sleep(1)
        # 点击国家下拉框
        driver.find_element_by_css_selector("label.font-Nm").click()
        sleep(1)
        # 获取国家列表
        ul_len = len(driver.find_elements(By.CSS_SELECTOR, '.naiion > ul:nth-child(1) > li'))
        for i in range(ul_len):

            # 获取国家名称
            li = driver.find_element_by_css_selector(f".naiion > ul:nth-child(1) > li:nth-child({i+1}) > h1:nth-child(1)")
            country_name = li.text

            # 如果没有该国家的记录，记录到输出报告中
            if not phone_num.get(country_name):
                write_log(country=country_name, none_country=True)
            else:
                for phone in phone_num[country_name]:

                    # 点击对应的国家
                    li = driver.find_element_by_css_selector(f".naiion > ul:nth-child(1) > li:nth-child({i+1}) > h1:nth-child(1)")
                    li.click()

                    print(f'country:{country_name}')
                    print(f'phone:{phone}')
                    a = driver.find_element_by_css_selector('input[placeholder="请输入手机号码"]')
                    # 输入电话
                    a.send_keys(phone)
                    b = driver.find_element_by_css_selector('.fromBotton')
                    Button_attribute = b.get_attribute("class")
                    sleep(1)
                    # 获取下一步按钮的class属性，fromBotton代表格式化成功
                    if Button_attribute == 'fromBotton':
                        print("格式化成功:%s"% country_name)
                    elif Button_attribute == "fromBotton nextType":
                        print("格式化失败:%s"% country_name)
                        write_log(country=country_name, phone=phone)
                    # 直接刷新页面
                    sleep(1)
                    driver.refresh()
                    sleep(2)
                    # 点击国家下拉框
                    driver.find_element_by_css_selector("label.font-Nm").click()

    finally:
        driver.quit()
