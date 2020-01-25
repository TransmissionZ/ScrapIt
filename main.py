from bs4 import BeautifulSoup
import requests
from Base_Class import Base
import json
import math
from datetime import datetime
import random
import sys
starttime=datetime.now()

obj=Base() 

def page(temp):
    splits=temp.split(" ")
    dash_index=splits.index("-")
    items_on_page=splits[(dash_index)+1]
    #print(items_on_page)
    dash_index=splits.index("of")
    total_items=splits[(dash_index)+2]
    #print(total_items)
    temp=(float(int(total_items)/int(items_on_page)))
    temp=math.ceil(temp)
    return temp,total_items

filename=sys.argv[1]
print("Sys arg 1: "+str(sys.argv[1]))
csv_file=filename+".csv"

obj.remove_image_folder(filename)
obj.removefile(csv_file)

#master_link="https://www.junaidjamshed.com/womens.html"
master_link=sys.argv[2]
print("Sys arg 2: "+str(sys.argv[2]))
html=requests.get(master_link).text
soup=BeautifulSoup(html,"html.parser")
#calculate pages
pages,ti=page(str((soup.find("p",class_="toolbar-amount")).get_text(" ")))
#print(pages)
Master_list=["Name","Description","Material","Color","Current Price","Original Price","Discount","Piece","Availability","Category","Size","Link"]
obj.csv_write(Master_list,csv_file)

#random images cause of file size
ran=obj.random(ti,pages)

curr_page=1
index=1
while(curr_page <= pages):

    link=master_link+"#?p="+str(curr_page)
    html=requests.get(link).text
    soup=BeautifulSoup(html,"html.parser")

    all_items=soup.find_all("li",class_="item product product-item")
    for item in all_items:
        item_list=[]
        item_list.extend([""]*(len(Master_list)))

        temp=item.find("a")
        link=(temp['href'])
        #link="https://www.junaidjamshed.com/jtp-303-s19-jj6634.html"
        print(link)
        html=requests.get(link).text
        soup=BeautifulSoup(html,"html.parser")

        #print(item_list)
        #name
        name=(soup.find("div",class_="page-title-wrapper product")).text
        item_list=obj.insert(Master_list.index("Name"),(name.replace("\n","")),item_list)
        #print(item_list)
        #price
        price=(soup.find("span",class_="price-wrapper")).text
        item_list=obj.insert(Master_list.index("Current Price"),((price.replace(",",""))).replace("PKR","PKR "),item_list)
        price=price.replace(",","")
        price=price.replace(".","")
        #org price
        second_price=soup.find("div",class_="product-info-price")
        second_price=second_price.find_all("span",class_="price-wrapper")
        if(len(second_price) == 2):
            second_price=second_price[1].text
            item_list=obj.insert(Master_list.index("Original Price"),((second_price.replace(",",""))).replace("PKR","PKR "),item_list)
            second_price=second_price.replace(",","")
            second_price=second_price.replace(".","")
            #calculate discount
            discount=obj.discount_cal(price,second_price)
            item_list=obj.insert(Master_list.index("Discount"),discount,item_list)
        #print(price)
        #description
        des=""
        des=(soup.find("div",{"itemprop":"description"}))
        if(des is not None):
            des=des.get_text("\n","/")
            des=des.replace(",","|")
            item_list=obj.insert(Master_list.index("Description"),des,item_list)
        #print(des)
        #table
        info_table=(soup.find("tbody"))
        #get row and data
        rows=info_table.find_all("tr")
        #color,cate,piece,fabric
        #print(rows)
        for row in rows:
            temp=row.find("td").text
            test=row.find("th")
            if(test is not None):
                if((row.find("th").text) == "Color"):
                    #print(row.find("td").text)
                    item_list=obj.insert(Master_list.index("Color"),temp,item_list)
                if((row.find("th").text) == "Product Category"):
                    #print(row.find("td").text)
                    item_list=obj.insert(Master_list.index("Category"),temp,item_list)
                if((row.find("th").text) == "Pieces "):
                    #print("Hey")
                    #print(row.find("td").text)
                    item_list=obj.insert(Master_list.index("Piece"),temp,item_list)
                if((row.find("th").text) == "Fabric"):
                    #print(row.find("td").text)
                    item_list=obj.insert(Master_list.index("Material"),temp,item_list)
        #available
        ava=(soup.find("div",class_="stock available")).text
        #print(ava)
        item_list=obj.insert(Master_list.index("Availability"),(ava.replace("\n","")),item_list)
        #adding link
        item_list=obj.insert(Master_list.index("Link"),link,item_list)
        #getting sizes
        sizes_str=""
        data=soup.find("div",class_="product-options-wrapper")
        if(data is not None):
            data=data.find("script")
            start=str(data).find("\"options\":")
            end=str(data).find("}]")
            json_extract=(str(data)[start:end]+"}]").replace("\"options\":","")
            loaded=json.loads(json_extract)
            for sizes in loaded:
                temp=sizes["products"]
                if(str(temp).find("[]") is -1):
                    temp=(sizes["label"]).replace("X","Extra")
                    sizes_str+=temp+"|"
            sizes_str=sizes_str[0:(len(sizes_str))-1]        
            item_list=obj.insert(Master_list.index("Size"),sizes_str,item_list)        
        #print(item_list)
        #getting pictures
        if(ran.count(index) is not 0):
            pic_link=[]
            pic=soup.find("div",class_="MagicToolboxSelectorsContainer")
            pic=pic.find_all("a")
            for pics in pic:
                pic_link.append(pics['href'])
            obj.add_images(pic_link,index,filename)

        obj.csv_write(item_list,csv_file)
        
        print(str(index)+"/"+str(ti)+" completed")
        index=index+1
        #if(index == 3):
        #break
    print(str(curr_page)+" page completed")    
    curr_page+=1
    #break
endtime=datetime.now() 
print("Download Completed")
print("Total time is "+str(endtime-starttime))    
