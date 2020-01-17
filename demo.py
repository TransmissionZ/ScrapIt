# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 18:32:26 2020

@author: Adil Ayub
"""
#libraries
from bs4 import BeautifulSoup
import bs4
import requests
import urllib.request
import os
import random
import math
from datetime import datetime
import shutil
print(bs4.__version__)
'''
add link to csv file
'''
def remove_image_folder(foldername):
    if(os.path.exists("Images_"+foldername)):
        shutil.rmtree("Images_"+foldername)
    os.mkdir("Images_"+foldername)    
#remove old files
def removefile(filename):
    if(os.path.exists(filename)):
       os.remove(filename)

#wirting csv file
def csv_write(the_list,filename):
    file=open(filename,"a+")
    for heading in the_list:
        heading=heading.replace("\n","")
        if(heading == the_list[(len(the_list)-1)]):
            file.write(str(heading)+"\n")
        else:    
            file.write(str(heading)+",")
    file.close()        

def discount_cal(current_price,org_price):
    num_cur=current_price.replace("PKR ","")
    num_org=org_price.replace("PKR ","")
    discount=(((int(num_cur)/int(num_org))*100)-100)*-1
    discount=round(discount)
    discount=str(discount)+"%"
    return discount
    
def insert(index,element):
    item_list.insert(index,element)
    item_list.pop(index+1)
    
def add_images(links,fileindex,filename):
    index=0
    for link in links:
        urllib.request.urlretrieve(link,"Images_"+filename+"/"+str(fileindex)+"-"+str(index)+".jpg")
        index+=1

def get_pages(string):
    temp=string.split(" ")
    print(temp)
    to=temp.index("to")
    of=temp.index("of")
    return (int(temp[(int(of)+1)])/ int(temp[(int(to)+1)])), int(temp[(int(of)+1)]) 

title_list=["Name","Description","Material","Color","Current Price","Old Price","Discount","Piece","Availability","Category","Gender","Size","Design","Link"]
global item_list
item_list=[]
item_list.extend([""]*(len(title_list)))
data_ele=[]
ran=[]

#number of pages
#master_link="https://www.alkaramstudio.com/unstitched?dir=asc&limit=36"
master_link="https://www.alkaramstudio.com/pret?limit=36&p=1"
html=requests.get(master_link).text
soup=BeautifulSoup(html,"html.parser")
num=soup.find("div",class_="col-lg-4 col-md-4 col-sm-4 col-xs-12 mob-btm-hide")
num=(num.find("div",class_="amount")).text
pages_html,items=get_pages(num)

#random images cause of file size
print("Images to be taken: "+str(int(items)/5))
print("Number of pages: "+str(pages_html))
for i in range(round(int(items)/5)):
    ran.append(random.randint(0,items))

image_folder="pret"
csv_filename=image_folder+".csv"
remove_image_folder(image_folder)
#old file removal
removefile(csv_filename)
               
#file creation
csv_write(title_list,csv_filename)               

index=1
pages=1
start_time=datetime.now()
while(pages <= math.ceil(pages_html)):
       #master_link="https://www.alkaramstudio.com/unstitched?dir=asc&limit=36&p="+str(pages)
       master_link="https://www.alkaramstudio.com/pret?limit=36&p="+str(pages)
       html=requests.get(master_link).text
       soup=BeautifulSoup(html,"html.parser")
       #print(soup.prettify())
       item=soup.find_all("li",class_="item col-lg-4 col-md-4 col-sm-6 col-xs-6")
       #print(item)
       item.insert(0,soup.find("li",class_="item col-lg-4 col-md-4 col-sm-6 col-xs-6 first"))
       #print(len(item))
       #break
       if(item == []):
           print("Page Error: "+str(pages))
           break
       else:
           for product in item:
               item_list=[]
               item_list.extend([""]*(len(title_list)))
               pro_img_link=product.find("a",class_="product-image")
               link=pro_img_link['href']

               #making soup
               #link="https://www.alkaramstudio.com/2-piece-embroidered-suit-with-satin-silk-dupatta-22631"
               #link="https://www.alkaramstudio.com/2-piece-embroidered-chicken-suit"
               #link="https://www.alkaramstudio.com/kids-printed-bed-sheet-set-t-185"
               #link="https://www.alkaramstudio.com/catalog/product/view/id/23533/s/emroidered-cotton-ribbed-kurti"
               #link="https://www.alkaramstudio.com/1-piece-mak-embroidered-21625"
               print(link)
               html=requests.get(link).text
               soup=BeautifulSoup(html,"html.parser")
               
               #name
               insert(0,(soup.find("div",class_="product-name").text).replace("\n",""))
               #Description
               insert(1,((soup.find("div",class_="std").get_text("|")).replace("\n","|")).replace(",","|").replace("\n","|"))
                #user input size
               sizes=soup.find("div",class_="input-box")
               if(sizes is not None):
                   sizes=sizes.find_all("span",class_="swatch-label swatch-label_hover")
                   if(len(sizes) is not 0):
                       temp_str=""
                       for t in sizes:
                           temp_str+=t.text+"|"
                       temp_str=(temp_str[0:(len(temp_str))-1]).replace(" ","")  
                       insert(title_list.index("Size"),temp_str)
               #table of info
               table=soup.find("table",class_="data-table")
               #print(table)
               if(table is not None):
                   data_ele=table.find_all("tr")
                   #print(data_ele)
                   if(not(data_ele == [])):
                       for data in data_ele:
                           if(data.th.text == "Fabric"):
                               #material
                               insert(title_list.index("Material"),data.td.text)
                           if(data.th.text == "Color"):
                               #Color
                               insert(title_list.index("Color"),data.td.text)
                           if(data.th.text == "Concept"):
                               #cate
                               insert(title_list.index("Category"),data.td.text)
                           if(data.th.text == "Product Category"):
                               #gender
                               insert(title_list.index("Gender"),data.td.text)
                           if((data.th.text == "Size") and(item_list[title_list.index("Size")] is "")):
                               #size
                               insert(title_list.index("Size"),data.td.text)
                           if(data.th.text == "Piece"):
                               #piece
                               insert(title_list.index("Piece"),data.td.text)
                           if(data.th.text == "Design"):
                               #Design
                               insert(title_list.index("Design"),(data.td.text).replace(","," "))
               #print(item_list[title_list.index("Size")])                
               #price
               price=soup.find("div",class_="price-box")
               if(price is not None):
                       price_2=price.find("p",class_="old-price")
                       if(price_2 is None):
                           temp_str=price.text
                           temp_str=temp_str.replace(",","")
                           insert(title_list.index("Current Price"),temp_str)
                           #old price
                           insert(title_list.index("Old Price"),"-")
                       else:
                           temp_str=price_2.find("span",class_="price")
                           temp_str=temp_str.text
                           temp_str=temp_str.replace(",","")
                           insert(title_list.index("Old Price"),temp_str)
                           #old price
                           price_2=price.find("p",class_="special-price")
                           temp_str=price_2.find("span",class_="price")
                           temp_str=temp_str.text
                           temp_str=temp_str.replace(",","")
                           insert(title_list.index("Current Price"),temp_str)
                #discount
               if(item_list[5] is not "-"):
                   insert(title_list.index("Discount"),discount_cal(item_list[4],item_list[5]))
               else:
                   insert(title_list.index("Discount"),"-")    
               #Availability
               ava=soup.find("p",class_="availability in-stock")
               if(ava is not None):
                   stock=ava.find("span")
                   if(stock is not None):
                       insert(title_list.index("Availability"),stock.text)
               #images
               data_ele=[]
               if(ran.count(index) is not 0):
                   print("Getting Images....\n Please Wait")
                   images=soup.find("div",class_="more-views")
                   images=images.find_all("a")
                   for image in images:
                       data_ele.append(image['href'])
                   add_images(data_ele,index,image_folder)   
                   print("Image of "+str(index)+" downloaded")
               #print(item_list)        
               #adding link to csv
               insert(title_list.index("Link"),str(link))
               #write item to file
               csv_write(item_list,csv_filename)
               print(str(index)+"/"+str(items)+" items downloaded")
               index+=1
               #break
               
       print("Page Number "+str(pages)+" downloaded")
       pages+=1
       #break
           
end_time=datetime.now()
print("Download Complete")
print("The time difference is "+str((end_time-start_time).seconds))