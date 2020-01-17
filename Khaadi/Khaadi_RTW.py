# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 07:10:11 2020

@author: Adil Ayub
"""

import urllib.request
from bs4 import BeautifulSoup
#from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
#import time
import os
from datetime import datetime
import requests
import json

#used to file the number of pages
#length=urllib.request.urlopen("https://www.khaadi.com/pk/unstitched11/by-fabric.html?p=1&product_list_limit=48&product_list_order=low_first")
#setup browser
#options=Options()
#options.headless=True
#browser=webdriver.Firefox(options=options,executable_path="geckodriver.exe")

#pages in the catagory
length=requests.get("https://www.khaadi.com/pk/ready-to-wear.html?p=2&product_list_limit=48").text
len_soup= BeautifulSoup(length,'html.parser')
lens=len_soup.find("span",class_="total-items")
items=len_soup.find("span",class_="toolbar-number")
loop_index=1

print("Website: Khaadi")
print("Pages: "+str(lens.text))
print("Items: "+str(items.text))

#csv file creation
if(os.path.exists("Khaadi_RTW.csv")):
       os.remove("Khaadi_RTW.csv")
ptr=open("Khaadi_RTW.csv","a+")
ptr.write("Name,Description,Material,Color,Current Price,Old Price,Discount,Best-seller,Sizes,Link"+"\n")
index=1
total_pages=0

#time start    
start_time=datetime.now()

#loop for number of pages
while(loop_index <= int(lens.text)):
    #page = urllib.request.urlopen("https://www.khaadi.com/pk/unstitched11/by-fabric.html?p="+str(loop_index)+"&product_list_limit=48&product_list_order=low_first")
    #html=page.read()
    html=requests.get("https://www.khaadi.com/pk/ready-to-wear.html?p="+str(loop_index)+"&product_list_limit=48").text
    soup = BeautifulSoup(html, 'html.parser')
    main_page=soup.find_all("div",class_="products catlog-products wrapper grid products-grid")
    pages=main_page[0].find_all("a",class_="product photo product-item-photo")
    total_pages+=len(pages)
    
    #all item loops
    for item in pages:
        c_dis=False
        
        #getting link to item
        temp_item=[]
        temp=item['href']
        link=temp
        print(str(link))
        
        
        #check if discount
        temp_dis=item.find("div",class_="stock unavailable discount-percent")
        if(temp_dis is not None):
            c_dis=True
            
        #getting page and parsing
        page = urllib.request.urlopen(temp)
        html=page.read()
        page.close()
        #html=urllib.request.urlopen("https://www.khaadi.com/pk/wbb19572-white.html")
        #html=requests.get("https://www.khaadi.com/pk/gowb19402-pink.html").text
        parse = BeautifulSoup(html, 'html.parser')
    
        #name
        name = parse.find("span",class_="base")
        temp_item.append(name.text)
        the_name=name.text
        
        #description
        descri=  parse.find("div",itemprop="description")
        temp_des=descri.get_text("\n")
        temp_des=temp_des.split("\n")
        new_string=""
        for every in temp_des:
            new_string=new_string+every+"/"
        new_string=new_string.replace(",","/")
        new_string=new_string[0:(len(new_string)-1)]        

        #details
        temp_mat=""
        temp_col=""
        mat_col=  parse.find_all("td",class_="col data")
        #print(len(mat_col))
        if(len(mat_col) == 2):
            try:
                temp_mat=mat_col[0].text
            except IndexError:
                temp_mat=""
            try:
                temp_col=mat_col[1].text
            except IndexError:
                temp_col=""
        else:
            if((mat_col[0])["data-th"] == "Color"):
                temp_col=mat_col[0].text
            if((mat_col[0])["data-th"] == "Material"):
                temp_mat=mat_col[0].text            

        #prices/bug for some price
        current_price=""
        org_price=""
        discount="" 
        #prices= parse.find_all("span",class_="special-price")
        if(c_dis is False):
            prices= parse.find_all("span",class_="price-container price-final_price tax weee")
            prices= prices[0].find_all("span",class_="price")
            current_price=prices[0].text
            current_price=current_price.replace(",","")
            current_price=current_price.replace("\n","")
        else:
            
            prices= parse.find_all("span",class_="price-container price-final_price tax weee")
            prices= prices[1].find_all("span",class_="price")
            current_price=prices[0].text
            current_price=current_price.replace(",","")
            current_price=current_price.replace("\n","")
            
            prices=parse.find("span",class_="old-price sly-old-price")
            prices=prices.find("span",class_="price")
            org_price=prices.text
            org_price=org_price.replace(",","")
            org_price=org_price.replace("\n","")
            
            #discount    
            #discount=""    
            #if(org_price is not ""):
            num_cur=current_price.replace("PKR ","")
            num_cur=num_cur.replace(",","")
            num_org=org_price.replace("PKR ","")
            num_org=num_org.replace(",","")
            discount=(((int(num_cur)/int(num_org))*100)-100)*-1
            discount=round(discount)
            discount=str(discount)+"%"
            
        #bestseller
        temp=parse.find("span",class_="hot-selling detail")
        if((temp is None) or (temp is [])):
            bestseller=False
        else:
            bestseller=True
        
         
         #print("time for images")
         #images
        '''
        temp=parse.find("div",class_="MagicToolboxSelectorsContainer")
        if(temp is not None):
            temp=temp.find_all("a",class_="mt-thumb-switcher")
            inner_index=0       
            for data in temp:
                 images=data['data-image']
                 urllib.request.urlretrieve(images,"Images_RTW/"+str(index)+"-"+str(inner_index)+".jpg")
                 inner_index+=1
        else:
            temp=parse.find("img",itemprop="image")
            urllib.request.urlretrieve(temp["src"],"Images_RTW/"+str(index)+"-"+"0.jpg")
        '''
        #get sizes
        '''
        size_str=""
        browser.get(link)
        time.sleep(3)
        temp=None
        #limit_start=datetime.now()
        #while(temp is None):
        obj=BeautifulSoup(browser.page_source,"html.parser")
        temp=obj.find("div",class_="product-options-wrapper")
        print(temp)
        #limit_end=datetime.now()
          #  if(((limit_end-limit_start).seconds) >= 5):
           #     break
        #print(temp)
        if(temp is not None):
            temp=temp.find_all("div",class_="swatch-option text")
            #print(len(temp))
            for sizes in temp:
                size_str+=sizes.text+"/"
                print(sizes.text)
            size_str=size_str[0:(len(size_str)-1)]    
        '''        
        size_str=""
        data=parse.find("div",class_="product-options-wrapper")
        if(data is not None):
            data=data.find("script")
            start=str(data).find("\"options\":")
            end=str(data).find("}]")
            json_extract=(str(data)[start:end]+"}]").replace("\"options\":","")
            loaded=json.loads(json_extract)
            for sizes in loaded:
                temp=sizes["products"]
                if(str(temp).find("[]") is -1):
                    size_str+=sizes["label"]+"/"
            size_str=size_str[0:(len(size_str)-1)]        

        #write to file
        ptr.write(the_name+","+new_string+","+temp_mat+","+temp_col+","+current_price+","+org_price+","+discount+","+str(bestseller)+","+str(size_str)+","+str(link)+"\n")
        
        
        #counter to check progress
        print(str(index)+"/"+str(total_pages))
    
        index=index+1
        
        #break
        
    print("Download Page: "+str(loop_index))
    loop_index+=1
    #if(loop_index == 4):
     #   break
    #break
    
ptr.close() 
#browser.quit()
print("Download Complete")
#time end
end_time=datetime.now()
print("The time difference is "+str((end_time-start_time).seconds))
