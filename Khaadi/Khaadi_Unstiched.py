# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 23:57:40 2019

@author: Adil Ayub
"""

import urllib.request
from bs4 import BeautifulSoup
import os
from datetime import datetime


#used to file the number of pages
length=urllib.request.urlopen("https://www.khaadi.com/pk/unstitched11/by-fabric.html?p=1&product_list_limit=48&product_list_order=low_first")
len_soup= BeautifulSoup(length.read(),'html.parser')
length.close()
lens=len_soup.find("span",class_="total-items")
loop_index=1

print("Website: Khaadi")
print("Pages: 8")
print("Items: 340")

#csv file creation
if(os.path.exists("test.csv")):
       os.remove("test.csv")
ptr=open("test.csv","a+")
ptr.write("Name,Description,Material,Color,Current Price,Old Price,Discount,Piece,Best-seller,Link"+"\n")
index=1
total_pages=0

#time start    
start_time=datetime.now()

#loop for number of pages
while(loop_index <= int(lens.text)):
    page = urllib.request.urlopen("https://www.khaadi.com/pk/unstitched11/by-fabric.html?p="+str(loop_index)+"&product_list_limit=48&product_list_order=low_first")
    html=page.read()
    page.close()

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
        #html=urllib.request.urlopen("https://www.khaadi.com/pk/j19402-yellow-2pc.html")
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
        prices= parse.find_all("div",class_="price-box price-final_price")
        prices= prices[0].find_all("span",class_="price")
        current_price=prices[0].text
        current_price=current_price.replace(",","")
        current_price=current_price.replace("\n","")
        if(c_dis):
            
            prices=parse.find("span",class_="old-price")
            prices=prices.find("span",class_="price")
            org_price=prices.text
            org_price=org_price.replace(",","")
            org_price=org_price.replace("\n","")
            
            #discount    
            discount=""    
            if(org_price is not ""):
                num_cur=current_price.replace("PKR ","")
                num_cur=num_cur.replace(",","")
                num_org=org_price.replace("PKR ","")
                num_org=num_org.replace(",","")
                discount=(((int(num_cur)/int(num_org))*100)-100)*-1
                discount=round(discount)
                discount=str(discount)+"%"
            
        #2pc or 3pc   
        real_pc=""      
        pc= parse.find("div",itemprop="sku")
        temp_pc=pc.text
        
        if(temp_pc.find("2Pc") is not -1):
            real_pc="2Pc"
        if(temp_pc.find("3Pc") is not -1):
            real_pc="3Pc"
        
        #bestseller
        temp=parse.find("span",class_="hot-selling detail")
        if((temp is None) or (temp is [])):
            bestseller=False
        else:
            bestseller=True
        
        #write to file
        ptr.write(the_name+","+new_string+","+temp_mat+","+temp_col+","+current_price+","+org_price+","+discount+","+real_pc+","+str(bestseller)+","+str(link)+"\n")
        
        #get images
        temp=parse.find("div",class_="MagicToolboxSelectorsContainer")
        if(temp is not None):
            temp=temp.find_all("a",class_="mt-thumb-switcher")
            inner_index=0       
            for data in temp:
                 images=data['data-image']
                 urllib.request.urlretrieve(images,"Images_Temp/"+str(index)+"-"+str(inner_index)+".jpg")
                 inner_index+=1
        else:
            temp=parse.find("img",itemprop="image")
            urllib.request.urlretrieve(temp["src"],"Images_Temp/"+str(index)+"-"+"0.jpg")
         
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
print("Download Complete")
#time end
end_time=datetime.now()
print("The time difference is "+str((end_time-start_time).seconds))

