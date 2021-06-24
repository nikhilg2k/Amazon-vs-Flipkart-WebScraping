# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 16:45:28 2019

@author: Administrator
"""

import bs4 as bs
import urllib.request as urlr

class WebScraper():
    alink='https://www.amazon.in/s?k='
    flink='https://www.flipkart.com/search?q='

    def __init__(self):
        pass
        
    def inputtoqry(self,exp):
        srchqry=''
        wordlist=exp.split()
        for word in wordlist:
            srchqry+=str(word)+'+'
        return srchqry
    
    def search(self,qstr,found,prodnames,prodprices):
        
       def wordtosrch(wrdlist):
            
           def strtolower(st1):
                resultstr=''
                for char in st1:
                    if char.isalnum():
                        resultstr+=char.lower()
                    else:
                        continue

                return resultstr
        
           wrdlist2=[]
           for i in range(len(wrdlist)):
               wrdlist2.append(strtolower(wrdlist[i]))
           return wrdlist2
        
        
       if found==0:
            return ['Not Available',0]
            
       elif found==1:
            wordlist=qstr.split()
            wdlst= wordtosrch(wordlist)

            matchlist=[]
            matchplist=[]
            matchind=[]
            numberofmatch=[]
            cnt=0
            
            for name in prodnames:

                nmchk=name.split()
                nmlst=wordtosrch(nmchk)
                nmstr=''

                for elem in nmlst:
                    nmstr+=elem

                for word in wdlst:

                    if word in nmstr:

                        cnt+=1
                        nameind=prodnames.index(name)
                        
                    if wdlst.index(word)==len(wdlst)-1:

                        
                        if cnt==len(wdlst):
                            matchind.append(nameind)
                            numberofmatch.append(cnt)
                            for i in range (len(numberofmatch)):
                                if numberofmatch[i]==len(wdlst):
                                    reqind=matchind[i]
                                    price=prodprices[reqind]

                                    matchlist.append(prodnames[reqind])
                                    matchplist.append(price)
                                    nmstr=''
                                    cnt=0
                        else:
                            cnt=0
                            nmstr=''
                                                

            if matchlist == [] or matchplist== []:
                return [qstr+' is Not Available','0']
            else:
                resultset=[matchlist[0],matchplist[0]] 
                return resultset
                print()

    
    def flipkart_search(self,query):
        srchurl=self.flink+self.inputtoqry(query)
        hdr = { 'User-Agent' : 'Chrome (Windows NT 6.1; Win64; x64)' }
        req=urlr.Request(srchurl,headers=hdr)
        sauce=urlr.urlopen(req).read()
        soup=bs.BeautifulSoup(sauce,'lxml')
        
        body=soup.body
        fnamelist=[]
        fpricelist=[]
        
        for para in body.find_all('div', class_ = "_3O0U0u"):
    
            if para is None:
                fmatch=0
                continue
            
            elif para.find_all('div', style = 'width:25%'):
                
                reslt=para.find_all('div', style ='width:25%')
                for child in reslt:
                    
                    d=child.find('a', class_ = "_2cLu-l")
                    product_name=(d.contents)[0]
                    fnamelist.append(product_name)
                    
                    e=child.find('div', class_ = "_1vC4OE")
                    product_price=(e.contents)[0]
                    fpricelist.append(product_price)
                    fmatch=1
                    
            else:
                b=para.find('div', class_ = "_3wU53n")
                name=list(b.contents)[0]
                fnamelist.append(name)
                i=0
                
                for parent in para.parents:
                    if i==0:
                        if parent is None:
                            print(parent)
                        elif parent.find('div', class_ ="col col-5-12 _2o7WAb"):
                            f=parent.find('div', class_ = "_1vC4OE _2rQ-NK")
                            price=list(f.contents)[0]
                            fpricelist.append(price)
                            i=1
                            fmatch=1
                            

        return(self.search(query,fmatch,fnamelist,fpricelist))

    def amazon_search(self,query):
        srchurl=self.alink+self.inputtoqry(query)
        hdr = { 'User-Agent' : 'Chrome (Windows NT 6.1; Win64; x64)' }
        req=urlr.Request(srchurl,headers=hdr)
        sauce=urlr.urlopen(req).read()
        soup=bs.BeautifulSoup(sauce,'lxml')
        
        body=soup.body
        anamelist=[]
        apricelist=[]
        match=0
        for para in body.find_all('span', class_ ="a-size-medium a-color-base a-text-normal"):
            if para is None:
                match=0
            else:
                name=list(para.contents)[0]
                anamelist.append(name)
                i=0
                
                for parent in para.parents:
                    if i==0:
                        if parent is None:
                            print(parent)
                        elif parent.find('span', class_ ='a-price-whole'):
                            b=parent.find('span', class_ ='a-price-whole')
                            price=list(b.contents)[0]
                            apricelist.append(price)
                            i=1
                            match=1
        
        return(self.search(query,match,anamelist,apricelist))

