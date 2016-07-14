from lxml import  etree
import re
import json
import requests
import time
import datetime
import pymysql
from selenium import webdriver
#Da Shi Xiong
driver=webdriver.Firefox()
driver.get('https://www.ele.me/shop/361800')
item={}
item['shop_name']=driver.find_element_by_xpath("html/body/div[4]/div[1]/div/div[1]/div[1]/div/h1").text
item['score']=driver.find_element_by_xpath("//a[@class='ng-binding']").text
item['sales']=driver.find_element_by_xpath("//span[@class='ng-binding']").text
item['qisong']=driver.find_element_by_xpath("html/body/div[4]/div[1]/div/div[2]/span[1]/em[2]").text
item['peisong']=driver.find_element_by_xpath("html/body/div[4]/div[1]/div/div[2]/span[2]/em[2]").text
item['speed']=driver.find_element_by_xpath("html/body/div[4]/div[1]/div/div[2]/span[3]/em[2]").text
item['gonggao']=driver.find_element_by_xpath("html/body/div[4]/div[3]/div[2]/div/div[1]/p").text
yuansu_food=driver.find_elements_by_xpath("//div[@class='ng-scope']/div[@class='shopmenu-list clearfix ng-scope']/div/div/h3")
yuansu_miaoshu=driver.find_elements_by_xpath("//div[@class='ng-scope']/div[@class='shopmenu-list clearfix ng-scope']/div/div/p")
yuansu_price=driver.find_elements_by_xpath("//div[@class='ng-scope']/div[@class='shopmenu-list clearfix ng-scope']/div/span[@class='col-3 shopmenu-food-price color-stress ng-binding']")
yuansu_sales=driver.find_elements_by_xpath("//div[@class='ng-scope']/div[@class='shopmenu-list clearfix ng-scope']/div/div/p/span[2]")
yuansu_score=driver.find_elements_by_xpath("//div[@class='ng-scope']/div[@class='shopmenu-list clearfix ng-scope']/div/div/p/span[1]")
foodscore=[]
foodsales=[]
foodprice=[]
foodmiaoshu=[]
foodnames=[]
items=[]
for name in yuansu_food:
    foodnames.append(name.text)
for miaoshu in yuansu_miaoshu:
    foodmiaoshu.append(miaoshu.text)
for price in yuansu_price:
    foodprice.append(price.text)
for sales in yuansu_sales:
    foodsales.append(sales.text)
for score in yuansu_score:
    foodscore.append(score.text[1:-1])
item['foodname']='#'.join(foodnames)
item['foodmiaoshu']='#'.join(foodmiaoshu)
item['foodprice']='#'.join(foodprice)
item['foodsales']='#'.join(foodsales)
item['foodscore']='#'.join(foodscore)
items.append(item)

#connect the database,insert into data
conn = pymysql.connect(host='192.168.1.249', user='root', passwd='root', db='meituan_comment',charset='utf8')
cur = conn.cursor()
for it in items:
    insertsql = """INSERT INTO `dashixiong` VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    args = (it['order_id'], it['create_time'], it['city_name'], it['shop_name'], it['qishou_name'], it['qishou_phone'],
            it['distance']
            , it['user_name'], it['sex'], it['user_address'], it['user_phone'], it['total_order_count'],
            it['total_price'], it['total_price_display']
            , it['food_name'], it['food_count'], it['food_price'], it['food_origin_price'], it['food_display'],
            it['discount'], zongji
            )

    # print args
    try:
        cur.execute(insertsql, args)
        conn.commit()
    except pymysql.Error, e:
        print e.message







# url='https://www.ele.me/restapi/batch'
# cookie_txt="ubt_ssid=u6rh92168tdcz3sah678yskephj2zmid_2016-07-14;_utrace=bcb88c8d18a9757f41685e6dbc3a2052_2016-07-12; pageReferrInSession=http%3A//bzclk.baidu.com/adrc.php%3Ft%3D0fKL00c00fAcewT0hG7w0nsem00g3Cug00000cPtDW300000IKlo1x.THvvq_ZQsef0UWdBmy-bIfK15yu-PhmYnhPbnj0smvN9nj60IHd7PY7DnRczwWFjfbDvrH7APjPDf1b3fRFafHnvfWf1nsK95gTqFhdWpyfqnWTzrjDknW0dPausThqbpyfqnHmhULFG5iu1IyFEThbqFMKzpHYz0ARqpZwYTjCEQvN_ui4VufKWThnqPjmdPH0%26tpl%3Dtpl_10085_12986_1%26l%3D1041398915%26ie%3Dutf-8%26f%3D8%26tn%3Dbaidu%26wd%3D%25E9%25A5%25BF%25E4%25BA%2586%25E4%25B9%2588%26rqlang%3Dcn%26inputT%3D6717; firstEnterUrlInSession=https%3A//www.ele.me/place/ws105qj8xdf"
#
# head={
#
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
#     'Accept': 'application/json, text/plain, */*',
#     'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
#     'Accept-Encoding': 'gzip, deflate',
#     'Content-Type': 'application/json;charset=utf-8',
# }
# cookies={}
# for line in cookie_txt.split(';'):
#     name,value=line.strip().split('=',1)
#     cookies[name]=value
# postdata="""{"timeout":10000,"requests":[{"method":"GET","url":"/v1/user?extras%5B%5D=premium_vip&extras%5B%5D=is_auto_generated"
# },{"method":"GET","url":"/v4/restaurants/361800?extras%5B%5D=food_activity&extras%5B%5D=certification
# &extras%5B%5D=license&extras%5B%5D=identification&extras%5B%5D=statistics&extras%5B%5D=album&extras%5B
# %5D=flavor&geohash=ws105qj8xdf"}]}"""
#
# r=requests.post(url,data=postdata,cookies=cookies,headers=head)
# jsondata=json.loads(r.content)
# print jsondata



