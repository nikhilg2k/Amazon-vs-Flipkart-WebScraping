# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 21:56:43 2020

@author: Administrator
"""

#New Attempt at GUI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image
import Project_Functions as funcs
import Project_WebScraper_search as flip
import webbrowser as browser

web=funcs.Functions()
scraper=flip.WebScraper()

font1=("Helvetica",36)                   
font2=("Helvetica",12)
font3=("Helvetica",18)
font4=("Helvetica",26)

class Parent_Project(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container=tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        self.title("Amazon Vs Flipkart Wishlist: Project")
        self.frames={}
        for f in [Welcome_Page,Search_Page,Wishlist_Page]:
            frame=f(container,self)
            self.frames[f]=frame
            frame.grid(row=0,column=0,sticky="nsew")
        self.show_frame(Welcome_Page)
             
    def show_frame(self,cont):
        frame=self.frames[cont]            
        frame.tkraise()
        
class Welcome_Page(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.grid_columnconfigure(0)
        self.grid_rowconfigure(0)
        #Background Color
        self.configure(background="#ede59a")
        
        #Title
        title=tk.Label(self,text="Amazon Vs Flipkart: Wishlist",font=font1,bg="#fddb3a")
        title.pack(pady=8)
        
        #Instructions
        instructions_0=tk.Label(self,text='Welcome To The Wishlist:',font=font3,bg="#ede59a")
        instructions_0.pack(side='top',padx=10,anchor='nw')
        
        instructions_1=tk.Label(self,text="Instructions:",font=font3,bg="#ede59a")
        instructions_1.pack(side='top',padx=10,anchor='nw')
        
        instructions_2=tk.Label(self,text='1.You can compare prices of your desired products on Flipkart and Amazon',font=font3,bg="#ede59a")
        instructions_2.pack(side='top',padx=100,anchor='nw')
        
        #Instruction to search
        instructions_3=tk.Label(self,text='2.Click search to go to Search Page',font=font3,bg="#ede59a")
        instructions_3.pack(side='top',padx=100,anchor='nw')

        #Instruction to view
        instructions_3=tk.Label(self,text='3.Click view to see current wishlist',font=font3,bg="#ede59a")
        instructions_3.pack(side='top',padx=100,anchor='nw')
        
        #Image
        img_avf=ImageTk.PhotoImage(Image.open('amazon_vs_flipkart.png'))
        imglbl=tk.Label(self,image=img_avf)
        imglbl.image=img_avf
        imglbl.pack(side='top',anchor='center',pady=20)

        test=tk.Frame(self,bg='#ede59a')
        test.pack(side="bottom",fill='none')
        
        #Button to search page
        img_search=ImageTk.PhotoImage(Image.open(r'search.png'))
        def gotosearch():
            global b1
            global b2
            b1=tk.Button()
            b2=tk.Button()
            controller.show_frame(Search_Page)
        button1=tk.Button(test,text='Search',image=img_search,command=lambda: gotosearch())
        button1.image=img_search
        button1.pack(side="right",anchor="se",padx=10,pady=10)
        
        #Button to view page
        img_view=ImageTk.PhotoImage(Image.open(r'view.jpg'))
        button2=tk.Button(test,text='View',image=img_view,command=lambda: controller.show_frame(Wishlist_Page))
        button2.image=img_view
        button2.pack(side="left",anchor="sw",padx=10,pady=10)

class Search_Page(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.grid_columnconfigure(0)
        self.grid_rowconfigure(0)
        #Background Color
        self.configure(background="#ede59a")
        
        #Title
        title=tk.Label(self,text="Amazon Vs Flipkart: Wishlist",font=font1,bg="#fddb3a")
        title.pack(pady=8)
        
        title1=tk.Label(self,text="Search",font=font4,bg="#AEE100")
        title1.pack(pady=8)
        
        #Frame to contain content
        f2=tk.Frame(self,bg='#ede59a')
        f2.pack(side='top')
        
        #Name of product input
        name_label=tk.Label(f2,text='Enter the name of the product: ',font=font3,bg='#ede59a')
        name_label.grid(row=0,column=0,sticky='w')
        input_box1=tk.Entry(f2, width=30,bg='#fddb3a',font=font3)
        input_box1.grid(row=0,column=1,padx=3)
        
        #Specification input
        spec_label=tk.Label(f2,text="Enter the specification: ",font=font3,bg='#ede59a')
        spec_label.grid(row=1,column=0,sticky='w')
        input_box2=tk.Entry(f2, width=30,bg='#fddb3a',font=font3)
        input_box2.grid(row=1,column=1,padx=3,pady=5)
        
        #Search Button
        img_search=ImageTk.PhotoImage(Image.open(r'search.png'))
        button1=tk.Button(f2,text='Search',image=img_search,command=lambda: execute_all())
        button1.image=img_search
        button1.grid(row=2,column=1,pady=10)
        
        #Spacing
        l1=tk.Label(f2,text='',bg="#ede59a",height=2)
        l1.grid(row=3,columnspan=2)
        l2=tk.Label(f2,text='',bg="#ede59a",height=2)
        l2.grid(row=4,columnspan=2)
        
        #Functionality
        '''Variables'''
        best_site=''
        best_price=''
        def execute_all():
            global best_site
            global best_price
            result_flip=scraper.flipkart_search(input_box1.get()+' '+input_box2.get())
            result_amz=scraper.amazon_search(input_box1.get()+' '+input_box2.get())
            best_site=web.get_best_site(web.string_to_int(result_flip[1]),web.string_to_int(result_amz[1]))
            best_price=web.get_best_price(web.string_to_int(result_flip[1]),web.string_to_int(result_amz[1]))
            best_price=chr(8377)+best_price
            web.add_new(result_flip,result_amz)
            messagebox.showinfo('Result','Added to the database:\nFlipkart\nName "{}" | Price: "{}"\nAmazon\nName "{}" | Price: "{}"'.format(result_flip[0],result_flip[1],result_amz[0],result_amz[1]))
            post_site()
            post_price()
            link()

        #Output Frame
        f3=tk.Frame(self,bg='#ede59a')
        f3.pack(side='top')

        #Outputs
        img_site=ImageTk.PhotoImage(Image.open(r'site.png'))
        deal_label=tk.Label(f3,text="You will get better deal on: ",image=img_site,compound='right',bg='#ede59a',font=font3)
        deal_label.image=img_site
        deal_label.grid(row=0,column=0,pady=10)
        img_price=ImageTk.PhotoImage(Image.open(r'price.png'))
        price_label=tk.Label(f3,text="Price : ",image=img_price,compound='right',bg='#ede59a',font=font3)
        price_label.image=img_price
        price_label.grid(row=0,column=2,padx=5,pady=10,sticky='w')
        outsite=tk.Text(f3,bg='#fddb3a',width=20,height=1,font=font2)
        outsite.grid(row=0,column=1,padx=5,pady=10,sticky='w')
        outprice=tk.Text(f3,bg='#fddb3a',width=20,height=1,font=font2)
        outprice.grid(row=0,column=3,padx=5,pady=10)
        
        def post_site():
            global best_site
            outsite.delete(0.0,'end')
            outsite.insert(0.0,best_site)
        def post_price():
            global best_price
            outprice.delete(0.0,'end')
            outprice.insert(0.0,best_price)
            
        #Link
        def link():
            global best_site
            global b1
            global b2
            global best_price

            if best_site=='Flipkart':
                bestsite_link=scraper.inputtoqry(scraper.flink+input_box1.get()+' '+input_box2.get())
                b1=tk.Button(f3,bg="#ede59a",text="Click to visit Flipkart link",font=font2,command=lambda: browser.open(bestsite_link),cursor='hand2') 
                b1.grid(row=2,column=1,sticky='w',pady=5)
                
            elif best_site=="Amazon":
                bestsite_link=scraper.inputtoqry(scraper.alink+input_box1.get()+' '+input_box2.get())
                b2=tk.Button(f3,bg="#ede59a",text='Click to visit Amazon link',font=font2,command=lambda: browser.open(bestsite_link),cursor='hand2')  
                b2.grid(row=2,column=1,sticky='w',pady=5)
                
            elif best_site=='Either':
                if web.string_to_int(best_price) != 0:
                    bestsite_link_a=scraper.inputtoqry(scraper.alink+input_box1.get()+' '+input_box2.get())
                    bestsite_link_f=scraper.inputtoqry(scraper.flink+input_box1.get()+' '+input_box2.get())
                    b1=tk.Button(f3,bg="#ede59a",text='Click to visit Amazon link',font=font2,command=lambda: browser.open(bestsite_link_a),cursor='hand2')  
                    b1.grid(row=2,column=1,sticky='w',pady=5)
                    b2=tk.Button(f3,bg="#ede59a",text='Click to visit Flipkart link',font=font2,command=lambda: browser.open(bestsite_link_f),cursor='hand2')  
                    b2.grid(row=3,column=1,sticky='w',pady=5)
                    
                else:
                    pass
 
        #Back Button
        test=tk.Frame(self,bg='#ede59a')
        test.pack(side="bottom",fill='none')
        def back():
            global best_site
            global best_price
            global b1
            global b2
            outsite.delete(0.0,'end')
            outprice.delete(0.0,'end')
            input_box1.delete(0,'end')
            input_box2.delete(0,'end')
            best_site=''
            best_price=''
            b1.destroy()
            b2.destroy()
            controller.show_frame(Welcome_Page)
            
        img_back=ImageTk.PhotoImage(Image.open(r'back.jpg'))
        button2=tk.Button(test,text='Back',image=img_back,command=lambda: back())
        button2.image=img_back
        button2.pack(side="right",anchor="se",padx=10,pady=10)
        
class Wishlist_Page(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.grid_columnconfigure(0)
        self.grid_rowconfigure(0)
        #Background Color
        self.configure(background="#ede59a")
        
        #Title
        title=tk.Label(self,text="Amazon Vs Flipkart: Wishlist",font=font1,bg="#fddb3a")
        title.pack(pady=8)
        title1=tk.Label(self,text="Wishlist",font=font4,bg="#AEE100")
        title1.pack(pady=8)
        
        #Frame to contain output
        f1=tk.Frame(self,bg='#ede59a')
        f1.pack(side='top')
        
        #Output Box
        output_box=tk.Text(f1,bg="#d5c455",width=86)
        output_box.grid(row=0,column=0)
        def post_output():
            output_box.delete(0.0,'end')
            output_box.insert(0.0,web.view())
        post_output()
        #Scrollbar
        sc=tk.Scrollbar(f1)
        sc.grid(row=0,column=1,sticky='ns')
        output_box.config(yscrollcommand=sc.set)
        sc.config(command=output_box.yview)
        
        #Back Button
        test=tk.Frame(self,bg='#ede59a')
        test.pack(side="bottom",fill='none',anchor='e')
        img=ImageTk.PhotoImage(Image.open(r'back.jpg'))
        button1=tk.Button(test,text='Back',image=img,command=lambda: controller.show_frame(Welcome_Page))
        button1.image=img
        button1.pack(side="right",anchor="se",padx=10,pady=10)
            
        #Update Button
        img_update=ImageTk.PhotoImage(Image.open(r'up.png'))
        button2=ttk.Button(test,text='Update List',image=img_update,command=lambda: post_output())
        button2.image=img_update
        button2.pack(side='left',anchor='sw',padx=10,pady=10)

gui=Parent_Project()
gui.mainloop()        

