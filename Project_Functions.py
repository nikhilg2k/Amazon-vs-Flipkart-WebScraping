# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 08:56:54 2019

@author: SCL1
"""
import pymysql as sql
import prettytable
from textwrap import fill
mycon=sql.connect(host='localhost',user='root',password='',database='Project')
cursor=mycon.cursor()

class Functions():
    def string_to_int(self,price):
        new_int=''
        nums='0123456789'
        for i in price:
            if i in nums:
                new_int+=i
        return int(new_int)
    
    def add_new(self,fliplist,amzlist):
        addlist=[fliplist[0],self.string_to_int(fliplist[1]),amzlist[0],self.string_to_int(amzlist[1])]
        insert_string='insert into newtable values("{}",{},"{}",{})'.format(addlist[0],addlist[1],addlist[2],addlist[3])
        cursor.execute(insert_string)
        mycon.commit()
        
    def get_best_site(self,price_flip,price_amz):
        if price_flip==0 and price_amz !=0:
            return "Amazon"
        elif price_amz==0 and price_flip!=0:
            return "Flipkart"
        elif price_flip>price_amz:
            return "Amazon"
        elif price_flip<price_amz:
            return "Flipkart"
        else:
            return "Either"
    def get_best_price(self,price_flip,price_amz):
        if price_flip==0:
            return str(price_amz)
        elif price_amz==0:
            return str(price_flip)
        elif price_flip>price_amz:
            return str(price_amz)
        else:
            return str(price_flip)
        
        
    def view(self):
        cursor.execute("select * from newtable")
        data=cursor.fetchall()
        hdr=["S.No",'Flipkart_Name',"Flipkart_Price",'Amazon_Name',"Amazon_Price"]
        table=prettytable.PrettyTable(hdr)
        count=0
        for i in data:
            count+=1
            table.add_row([count,fill(i[0],width=20),chr(8377)+str(i[1]),fill(i[2],width=20),chr(8377)+str(i[3])])
            table.add_row(['','','','',''])
        return table.get_string()
