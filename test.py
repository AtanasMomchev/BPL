import requests
from bs4 import BeautifulSoup


res = requests.get("https://tablegames.bg/search.html?phrase=fuse")
soup = BeautifulSoup(res.text, 'html.parser')
title = soup.select('.product-title.ellipsis a')
price = soup.select('.price-withtax')
url = soup.select('.product-image-bg')

print(price[0].getText())


# from selenium import webdriver
#
# u = 'https://www.ozone.bg/instantsearchplus/result/?q=razer%20-%20deathadder%20'
# driver = webdriver.Chrome(executable_path='D:\\Projects\\chromedriver')
# driver.get(u)
# title = driver.find_element_by_class_name('isp_product_info')
# for i in title:
#     print(i)