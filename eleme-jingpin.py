# -*- coding: utf8 -*-
import json
import requests
import pymysql
import sys
import datetime
import time
import sys
import re
import multiprocessing
from selenium import webdriver

kd=sys.argv[1].decode('gbk').encode('utf-8')

print kd

conn = pymysql.connect(host='192.168.1.249', user='root', passwd='root', db='meituan_comment',charset='utf8')
cur = conn.cursor()

def requests_urls(urls,location):

    print 'location is %s' % location

    shop_numbers=re.findall("-?[1-9]\d*",urls)
    for s in shop_numbers:
        shop_numbers=int(s)

    #print int(shop_numbers)
    #伪装用户代理
    head={
      "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    cookies_text = """ubt_ssid=pc85a36u1jhpqv5yd5q6l4ltqkyf0pw3_2016-06-20; _utrace=4da32a1a6b3f80bdae8c945c33e23b0f_2016-06-20"""

    cookies={}

    #cookies 处理
    for line in cookies_text.split(';'):
        name,value=line.strip().split('=',1)
        cookies[name]=value

    post_data ='{"timeout":10000,"requests":[{"method":"GET","url":"/v1/user?extras%%5B%%5D=premium_vip&extras%%5B%%5D=is_auto_generated"\
},{"method":"GET","url":"/v4/restaurants/%d?extras%%5B%%5D=food_activity&extras%%5B%%5D=certification\
&extras%%5B%%5D=license&extras%%5B%%5D=identification&extras%%5B%%5D=statistics&extras%%5B%%5D=album&extras%%5B\
%%5D=flavor&geohash=ws100mszxpr"}]}' % int(shop_numbers)

    url='https://www.ele.me/restapi/batch'


    #获取总数的请求
    check=requests.post(url,data=post_data,headers=head,cookies=cookies)
    checkcontent=check.content
    checkdata=json.loads(checkcontent)
    #Get data
    try:
        all_data=checkdata[1]['body']
        true_data=json.loads(all_data)
        shopname=true_data['name']
        address=true_data['address']
        phone=true_data['phone']
        sales_people=true_data['recent_order_num']
        score=true_data['rating']
    except Exception as e:
        print e.message

    #Again requests
    post_data2='{"timeout":10000,"requests":[{"method":"GET","url":"/shopping/v1/menu?restaurant_id=%d"},' \
               '{"method":"GET","url":"/v1/users/15462046/messages/count"},{"method":"GET",' \
               '"url":"/ugc/v1/restaurants/464498/rating_scores?latitude=22.54412&longitude=113.9466"},' \
               '{"method":"GET","url":"/v1/users/15462046/favor/restaurants/464498"}]}' % shop_numbers

    cookies2_txt="ubt_ssid=xg0gh4k0ud3gig0ivmtfjfkh7q7dxy6n_2016-05-04; " \
                 "_utrace=bec7ca9501c95aa532b60704ed0914ee_2016-05-04;" \
                 " track_id=1462348258%7Ca019611db23803d4762eb9ffcc751bc58b720435aa81e88f93%7C68edbbba3e2d930f2b02e8ba7d11d51a;" \
                 " SID=YGfRlNCDuv8xYIVelQ9qk5jiH5N6ftO7ZDFw; USERID=15462046; " \
                 "eleme__ele_me=04c1f502f4713ae2755e8b636d4436eb%3A58f0216ab82449a9f12e14abb92c0c33d48379b9;" \
                 " firstEnterUrlInSession=https%3A//www.ele.me/place/ws102bj3h0x; " \
                 "pageReferrInSession=https%3A//www.ele.me/place/ws102bj3h0x"
    cookies2={}
    #cookies 处理
    for line in cookies2_txt.split(';'):
        name,value=line.strip().split('=',1)
        cookies2[name]=value

    food_data=requests.post(url,headers=head,cookies=cookies2,data=post_data2)
    result=food_data.content
    result=json.loads(result)
    try:
    # print result[0]['body'][1:-1]
        foodnames_arr=[]
        foodprices_arr=[]
        foodsales_arr=[]
        foodorginprices_arr=[]
        true_result=json.loads((result[0]['body']))
        for i in true_result:
            for m in i['foods']:
                for n in m['specfoods']:
                    foodprices_arr.append(str(n['price']))
                    foodnames_arr.append((n['name']))
                    foodorginprices_arr.append(str(n['original_price']))
                    foodsales_arr.append(str(n['recent_popularity']))

        foodname='#'.join(foodnames_arr)
        foodprice='#'.join(foodprices_arr)
        foodsales='#'.join(foodsales_arr)
        foodorgprice='#'.join(foodorginprices_arr)

        #print foodname,foodprice,foodorgprice,foodsales
        theTime= time.strftime('%Y-%m-%d',time.localtime(time.time()))
    except Exception as e:
        print e.message

    try:
        insert_sql="""
                    replace into `comshop_all_data` (updateTime,category,platfrom,shopname,address,phone,score,food_name,price,orgin_price,food_sales,url,sales_people)
                    VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   """
        args=(theTime,location,'饿了么',shopname,address,phone,score,foodname,foodprice,foodorgprice,foodsales,urls,sales_people)
        #print args
        cur.execute(insert_sql, args)
        conn.commit()
    except Exception as e:
        print e.message

get_shop_session='https://www.ele.me/restapi/v2/pois?extras[]=count&geohash=ws105rz9smwm&keyword=%s&limit=20&type=nearby' % kd
content=requests.get(get_shop_session)
checkcontent=content.content
checkdata=json.loads(checkcontent)
shopAndGeo=[]
for ad in checkdata:
    item={}
    item['name']=ad['name']
    item['geohash']=ad['geohash']
    shopAndGeo.append(item)


def extra_urls(geo):

    print geo['geohash']
    print geo['name']

    location=geo['name']

    true_url='https://www.ele.me/place/%s' % geo['geohash']
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.maximize_window()
    driver.get(true_url)

    xiala_button=driver.find_element_by_xpath("//div[@id='fetchMoreRst']")
    #click the button load ajax page
    try:
        while xiala_button:
            xiala_button.click()
            xiala_button = driver.find_element_by_xpath("//div[@id='fetchMoreRst']")
    except Exception as e:
        print e.message
    finally:
        urls_=driver.find_elements_by_xpath("//a[@class='rstblock']")
        urls=[]

        for url in urls_:
            all_href=url.get_attribute('href')
            urls.append(all_href)

        #print urls
        #print 'urls length is %d' % len(urls)
    #print 'here is %s' % urls
    driver.quit()
    for url in urls:
        requests_urls(url,location)

#----------------------------------------------Get GeoHash-----------------------------------------
geo_urls=[]
geo_names=[]
for geo in shopAndGeo:
    geo_urls.append(geo['geohash'])
    geo_names.append(geo['name'])


if __name__=='__main__':
    # print geo_urls
    # print len(geo_urls)
    pool=multiprocessing.Pool(multiprocessing.cpu_count(),maxtasksperchild=10)
    pool.map(extra_urls,shopAndGeo)
    #print 'Im urls of pool is %s' %
    # print type(pool_get_urls)
    pool.close()
    pool.join()
