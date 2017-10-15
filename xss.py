#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# class for check SQL injection , XSS and LFI

import requests
from bs4 import BeautifulSoup
import threading
import introduce
from colorama import init , Style, Back,Fore

from selenium import webdriver
import test



session = requests.session()
vulArray = []
_kt = True
_browser = webdriver.Firefox
_path_geck = ''
_site = ''

def login():
    dataForm = {'login': 'bee', 'password': 'bug', 'security_level': 2, 'form': 'submit'}
    session.post ('http://192.168.141.145/bWAPP/login.php', data=dataForm)
    print "login thanh cong"

def wordlistimport(file,lst):
		try:
			with open(file,'r') as f: #Importing Payloads from specified wordlist.
				print(Style.DIM+Fore.WHITE+"[+] Loading Payloads from specified wordlist..."+Style.RESET_ALL)
				for line in f:
					final = str(line.replace("\n",""))
					lst.append(final)
		except IOError:
			print(Style.BRIGHT+Fore.RED+"[!] Wordlist not found!"+Style.RESET_ALL)

# dien moi payload vao tat ca input
def getFormFrom_Url(urlInput,payload):

    # xss
    r = session.get (urlInput)

    # get all form
    parseHTML = BeautifulSoup (r.content, "lxml")

    htmlForm = parseHTML.find_all('form')

    formArr = []

    for x in htmlForm:
        formArr.append(x)

    #chen moi form mot payload va tra ve string
    payloadArr = []
    for x in formArr:
        inputs = x.find_all('input')
        # if inputs:
        #     print inputs

        # lay tat ca the input trong form
        payString = urlInput
        dem = 0
        if inputs :
            for y in inputs:
                # lay ten cua the input
                temp = ''
                if dem == 0:
                    temp = '?'
                else:
                    temp = '&'

                name = y.attrs['name']
                payString = payString + temp + name + '=' + payload
                dem = 1

            payloadArr.append (payString)

    return payloadArr


def Input():
    print "[!] URL Example: http://192.168.141.145/bWAPP/xss_get.php"
    site = raw_input ("[?] Enter URL: ")
    # site = "http://192.168.141.131/bWAPP/xss_get.php?firstname=d&lastname=d&form=submit"
    # site = "http://thegioiso.vn/search.php?kw=test"
    if 'http://' in site:
        pass
    elif 'https://' in site:
        pass
    else:
        site = "http://" + site

    return site


def brutexss():
    introduce.init()
    introduce.banner()
    global _path_geck
    global _site


    print """
         1. XSS - Reflected (GET)
         2. XSS - Reflected (POST)
         3. Cross-Site Scripting - Stored (Blog)
    """
    methodselect = eval(raw_input ("[?] Select method: "))
    _path_geck = raw_input ("input path_geck:")
    _site = Input ()

    if methodselect == 1:
        GET()
    elif methodselect == 2:
        POST()
    elif methodselect == 3:
        storeXss()
    else:
        print("[!] Incorrect method selected.")







def open_url(inj,payl):
    # print ("[!] Checking")
    # print (inj)
    global _kt
    countVul = 0;
    page = session.get(inj)
    if _kt :
        if payl in page.content:
            countVul += 1
            # print 20*"="
            # print inj
            # print 20*"="
            vulArray.append (inj)
            _kt = False



def GET():
    print 20*'-'+" DEF GET "+20*'-'
    global _site
    payloads = []
    newpayloads = []
    wordlist = 'wordlist.txt'
    wordlistimport (wordlist, payloads)

    for payTemp in payloads:
        newpayloads.append(getFormFrom_Url(_site,payTemp))

    for x,payl in zip(newpayloads,payloads):
        for y in x:
            t = threading.Thread(target=open_url,args=[y,payl])
            t.start()
            t.join()

#get data form
def getDataUrl(urlInput,payload):
    dataForm = []
    # xss
    r = session.get (urlInput)

    # get all form
    parseHTML = BeautifulSoup (r.content, "lxml")

    htmlForm = parseHTML.find_all ('form')

    formArr = []

    for x in htmlForm:
        formArr.append (x)

    payloadArr = []

    # lay tat ca cac form
    for x in formArr:
        # tim tat ca the input trong form
        inputs = x.find_all ('input')

        # payString = urlInput
        # dem = 0
        # neu tim co the input trong form
        if inputs:
            # tim tat ca cac the input lay du lieu
            dataForm = {}
            dataForm['form'] = 'submit'
            for y in inputs:
                # lay attrs name cua the input
                name = y.attrs['name']
                dataForm[name]=payload

        if dataForm:
            payloadArr.append (dataForm)
            dataForm = []


    return payloadArr

def postUrl(data,url,payl):
    global _kt
    if _kt:
        page = session.post (url, data=data[0])
        # kiem tra neu co alert
        if payl in page.content:
            vulArray.append (data)
            _kt=False



def POST():
    print 20*'-'+" DEF GET "+20*'-'
    global _site
    payloads = []
    newpayloads = []
    wordlist = 'wordlist.txt'
    wordlistimport (wordlist, payloads)

    for payTemp in payloads:
        #
        newpayloads.append(getDataUrl(_site,payTemp))

    for x,payl in zip(newpayloads,payloads):
        t = threading.Thread (target=postUrl, args=[x, _site, payl])
        t.start ()
        t.join ()

def postUrls(data,url,payl,path):
    global _kt
    if _kt:
        session.post (url, data=data[0])
        # kiem tra neu co alert
        kt = test.checkAlert(url,path)
        if kt:
            vulArray.append (data)
            _kt = False

def storeXss():
    global _path_geck
    # site = Input()
    global _site
    payloads = []
    newpayloads = []
    wordlist = 'wordlist.txt'
    wordlistimport (wordlist, payloads)
    for payTemp in payloads:
        #
        newpayloads.append(getDataUrl(_site,payTemp))

    for x,payl in zip(newpayloads,payloads):
        t = threading.Thread (target=postUrls, args=[x, _site, payl,_path_geck])
        t.start ()
        t.join ()



if __name__ == '__main__':
    # login()
    brutexss()

    stt = 0
    for x in vulArray:
        print Fore.RED + 30*'-' +" XSS Vulnerable "+30*'-'
        print Fore.RED + "[!] " + str(x)
        # print x
    print 30*"-"+" Finish "+30*"-"

    # getFormFrom_Url('http://192.168.141.144/bWAPP/xss_get.php',session,'</script>"><script>prompt(1)</script>')















