import re
import string
from time import sleep
from xmlrpc.client import Boolean
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from loguru import logger
# 全局wait time 根据个人需求修改
second = 5


class CommonUtils:

  # 执行点击操作
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver
  @classmethod
  def AutoClick(self, method: By, param: string, driver:webdriver):  # 自动点击
    button = self.tryGetElemetTwice(method, param, driver)
    # 弃用下面被注释的代码,因为有时候会出现元素找到了但是无法点击的情况,所以改为使用js点击
    # button = WebDriverWait(driver, second, 1).until(EC.presence_of_element_located((method, param)))
    driver.execute_script("arguments[0].click();", button)

  # 执行点击操作,如果未找到元素则刷新页面
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver
  @classmethod
  def AutoClickWithRefresh(self, method: By, param: string, driver):  # 自动点击
    button = self.tryGetElemetTwiceWithRefresh(method, param, driver)
    if(button is None):
      logger.debug("获取元素失败："+param)
    driver.execute_script("arguments[0].click();", button)

  # 验证元素是否存在,不存在则抛出异常
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver
  @classmethod
  def validElementContains(self, method: By, param: string, driver):

    temp = True
    a = 0
    while (a < 2) & temp:
       try:
         #todo 未捕获到就刷新，后面可以改
         WebDriverWait(driver, second, 0.5).until(
             EC.presence_of_element_located((method, param))
         )
         temp = False
         a = a+2
       except Exception:
         a = a+1

  # 获取对应元素(单个,如有多个返回第一个),未获取到则进行第二次尝试,最终未获取到则返回None
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver 
  # return: element or None
  @classmethod
  def AutoGetElement(self, method: By, param: string, driver):
    element = self.tryGetElemetTwice(method, param, driver)

    return element
  
  # 获取对应元素(多个),未获取到则进行第二次尝试,最终未获取到则返回None
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver
  # return: elements or None
  @classmethod
  def AutoGetElements(self, method: By, param: string, driver):
    elements = self.tryGetElemetsTwice(method, param, driver)
    return elements


  # 获取对应元素,未获取到则刷新页面后进行第二次尝试,最终未获取到则返回None
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver
  # return: element or None
  @classmethod
  def AutoGetElementWithRefresh(self, method: By, param: string, driver):
    element = self.tryGetElemetTwiceWithRefresh(method, param, driver)
    return element
  
  # 填充内容到对应元素中,填充前会清空元素内容
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # content: string  examp: "content"
  # driver: WebDriver examp: driver
  @classmethod
  def AutoInput(self, method: By, param: string, content, driver):
     element = self.tryGetElemetTwice(method, param, driver)
     element.clear()
     element.send_keys(content)

  # 获取对应元素(单个,如果有多个返回第一个),返回element,如果未获取到则进行重试.最终未获取到则返回None
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver
  # num: int  examp: 5 重试次数
  # waitTimes: int  examp: 1 重试间隔时间
  # return: element or None
  @classmethod
  def tryGetElemetTwice(self, method: By, param: string, driver ,num=5,waitTimes=1):
    temp = True
    a = 0
    element = None
    while (a < num) & temp:
       try:
         #todo 未捕获到就刷新，后面可以改
         element = WebDriverWait(driver, second, waitTimes).until(
             EC.presence_of_element_located((method, param))
         )
         temp = False
         a = a+num
       except Exception:
         a = a+num
    return element
  

  # 获取对应元素(单个,如果有多个返回第一个),返回element,如果未获取到则先刷新页面然后再次尝试获取.最终未获取到则返回None
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver
  # num: int  examp: 5 重试次数
  # waitTimes: int  examp: 1 重试间隔时间
  # return: element or None
  @classmethod
  def tryGetElemetTwiceWithRefresh(self, method: By, param: string, driver,num=5,waitTimes=1):
    temp = False
    a = 0
    element = None
    while (a < num):
       if(temp == True):
         a = a+num
       try:
         element = WebDriverWait(driver, second, waitTimes).until(
             EC.presence_of_element_located((method, param))
         )
         if(element is not None):
          temp = True
          a = a+num
       except Exception:
         logger.debug("未找到元素:{}，执行刷新后重试".format(param))
         driver.refresh()
         a = a+1
    return element
  
  # 获取对应元素(多个),如果未获取到则进行重试.返回elements list,最终未获取到则返回None
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver
  # return: elements list or None
  @classmethod
  def tryGetElemetsTwice(self, method: By, className: string, driver):
    temp = True
    a = 0
    elements = None
    while (a < 2) & temp:

       try:
         #todo 未捕获到就刷新，后面可以改
         logger.debug("check:"+className)
         elements = WebDriverWait(driver, second,1).until(
             EC.presence_of_all_elements_located((method, className))
         )
         temp = False
         a = a+2
       except Exception:
         a = a+1
    return elements

  # 检查元素是否存在(进行多次尝试,每次尝试获取前刷新页面),存在返回element list,不存在返回None   
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver
  # num: int  examp: 5 重试次数
  # waitTimes: int  examp: 1 重试间隔时间
  # return: bool
  @classmethod
  def check_element_exists(self, method: By, param: string, driver,num=5,waitTimes=1):
    var = self.tryGetElemetTwiceWithRefresh(method, param, driver,num,waitTimes)
    if(var is None):
      return False
    else:
      return True

  # 检查元素是否存在(进行多次尝试),存在返回True,不存在返回False
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver
  # num: int  examp: 5 重试次数
  # waitTimes: int  examp: 1 重试间隔时间
  # return: bool
  @classmethod
  def check_element_existsNoRefresh(self, method: By, param: string, driver,num=5,waitTimes=1):
    var = self.tryGetElemetTwice(method, param, driver,num,waitTimes)
    if(var is None):
      return False
    else:
      return True

  # 检查元素是否存在(进行2次尝试,每次尝试获取前刷新页面),2次尝试未检查到元素则抛出异常
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver
  
  @classmethod
  def checkAndExceptein(self, method: By, param: string,  driver):
    var = self.tryGetElemetTwiceWithRefresh(method, param, driver)
    logger.debug("check:"+param)
    if(var is None):
       logger.debug("check False:"+param)
       raise Exception('未找到元素：{}'.format(param))
     
     
  # 检查元素是否存在(进行2次尝试,每次尝试获取前刷新页面),获取到则返回True,2次尝试未检查到元素返回False
  # method: By  examp: By.ID
  # param: string  examp: "id"
  # driver: WebDriver examp: driver
  # return: bool
  @classmethod
  def checkAndRefresh(self, method: By, param: string, driver):
     var = self.tryGetElemetTwiceWithRefresh(method, param, driver)
     logger.debug("check:"+param)
     if(var is None):
       logger.debug("check False:"+param)
       return False
     else:
       logger.debug("check True:"+param)
       return True


