from bs4 import BeautifulSoup
import bs4
import requests
import urllib.request
import os
import random
import math
from datetime import datetime
import shutil
#print(bs4.__version__)

class Base:
    def remove_image_folder(self,foldername):
        if(os.path.exists("Images_"+foldername)):
            shutil.rmtree("Images_"+foldername)
        os.mkdir("Images_"+foldername)    
    #remove old files
    def removefile(self,filename):
        if(os.path.exists(filename)):
           os.remove(filename)
    
    #wirting csv file
    def csv_write(self,the_list,filename):
        file=open(filename,"a+")
        for heading in the_list:
            heading=heading.replace("\n","")
            if(heading == the_list[(len(the_list)-1)]):
                file.write(str(heading)+"\n")
            else:    
                file.write(str(heading)+",")
        file.close()        
    
    def discount_cal(self,current_price,org_price):
        num_cur=current_price.replace("PKR","")
        num_org=org_price.replace("PKR","")
        discount=(((int(num_cur)/int(num_org))*100)-100)*-1
        discount=round(discount)
        discount=str(discount)+"%"
        return discount
        
    def insert(self,index,element,item_list):
        item_list.insert(index,element)
        item_list.pop(index+1)
        return item_list
        
    def add_images(self,links,fileindex,filename):
        print("Downloading picture num: "+str(fileindex))
        index=0
        for link in links:
            urllib.request.urlretrieve(link,"Images_"+filename+"/"+str(fileindex)+"-"+str(index)+".jpg")
            index+=1
    
    def random(self,num_item,pages):
        ran=[]
        print("Images to be taken: "+str(int(num_item)/8))
        print("Number of pages: "+str(pages))
        for i in range(round(int(num_item)/8)):
            ran.append(random.randint(0,int(num_item)))
        return ran

