# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep


def login_xiaoe(url='https://admin.xiaoe-tech.com/login_page#/account'):
    '''用cookie登录准线网账号'''
    driver = webdriver.Chrome()
    driver.get(url)
    # driver.maximize_window()
    driver.implicitly_wait(10)
    sleep(1)
    login = {'name': 'laravel_session',
             'value': 'eyJpdiI6Ik84K0wyVXFpWUVLa2s0QTZXVVAraXc9PSIsInZhbHVlIjoic1AzZ0d6ZTFWVjU5eEhjZGl0V0taaGpFSjI5MzBYblJTaDZ3WG5YVWM5NkdtN0ZNRkNtR'
                      'FM5cHA0SE9ZU2lTZmY1R0FCMDlNWVhSU2lzb1lJXC9xdEFBPT0iLCJtYWMiOiI1MzYxMzE5Y2U2MDQ5MDljNGQxYmY3NWQ3ODg5NThiMDEyYmFmNjUxOTJiYzBhZWY5MWIwNjAzYzMwZjFlM2IzIn0%3D'}
    driver.add_cookie(login)  # 输入cookies
    sleep(1)
    driver.refresh()



if __name__ == '__main__':
    login_xiaoe()