# selenium_util
a common util repo for selenium 


Selenium 工具类
这是一个针对selenium的python工具类，旨在帮助新手入门时使用。它封装了常见的selenium方法，处理了一些常见的异常情况及返回值。
如果自身有其他需求,可以根据里面的方法进行二次包装后使用


CommonUtils
这是一个通用的Selenium工具类，用于对一些常用的操作进行包装。以下是此工具类中包含的方法：

AutoClick
执行点击操作。


AutoClick(method: By, param: string, driver:webdriver)
参数：

method：元素的定位方式，如By.ID。
param：元素的参数，如"id"。
driver：webdriver对象，即浏览器对象。
AutoClickWithRefresh
执行点击操作，如果未找到元素则刷新页面。

AutoClickWithRefresh(method: By, param: string, driver)
参数：

method：元素的定位方式，如By.ID。
param：元素的参数，如"id"。
driver：webdriver对象，即浏览器对象。

validElementContains
验证元素是否存在，不存在则抛出异常
validElementContains(method: By, param: string, driver)

参数：

method：元素的定位方式，如By.ID。
param：元素的参数，如"id"。
driver：webdriver对象，即浏览器对象。
AutoGetElement
获取对应元素（单个，如有多个返回第一个），未获取到则进行第二次尝试，最终未获取到则返回None。


AutoGetElement(method: By, param: string, driver)
参数：
method：元素的定位方式，如By.ID。
param：元素的参数，如"id"。
driver：webdriver对象，即浏览器对象。
返回值：
element：获取到的元素，如果未获取到则返回None。

AutoGetElements
获取对应元素（多个），未获取到则进行第二次尝试，最终未获取到则返回None。
AutoGetElements(method: By, param: string, driver)
参数：

method：元素的定位方式，如By.ID。
param：元素的参数，如"id"。
driver：webdriver对象，即浏览器对象。
返回值：
elements：获取到的元素列表，如果未获取到则返回None。

更多的方法 查看注释

如果有用 希望fork && star,thx

