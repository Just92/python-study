# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#-----------------------------------------------------------------------------------------------
#import pydoc
#pydoc.gui()
#my_name = 'chen'
#print (" Let's talk about %s. " %my_name)

#y="hell no"
#print ("I said : %s" %y)
#print ("I said : %r" %y)

#print ("How old are you?")
#age = input()
#print (type(age))
#print ("How tall are you?")
#height = input()
#type(height)
#print ("How much do you weigh?")
#weight = input()

#print ("So, you're %r old, %r tall and %r heavy." % (age, height, weight))

#age = input("How old are you ?")

#python -m pydoc input
#----------------------------------------------------------------------------------------------------
#from sys import argv 
#从外部传入参数 空格隔开
#script,first,second,third = argv
#print ("How tall are you?" , first)
#print ("How tall are you?" , script)
#print ("How tall are you?" , third)
#print ("How tall are you?" , second)
#----------------------------------------------------------------------------------------------
#from sys import argv
#传入并接受参数
#script,user_name = argv
#prompt='>'
#print ("Hi %s , I'm the %s script." %(user_name,script))
#print ("Do you like me %s?" %user_name)
#likes=input(prompt)
#print("""
#Alright, so you said %r about liking me.
#""" %likes)

#script , file_name = argv 
#txt = open(file_name)
#print ("Here's your file %r:" %file_name)
#print (txt.read())
#txt.close()

#print("Type the file name again:")
#txt_again = open(input(prompt))
#print(txt_again.read())
#txt_again.close()
#-----------------------------------------------------------------------------------------------------
#from sys import argv
#from os.path import exists
#script,from_file,to_file = argv
#print("Copy from %r to %r" %(from_file,to_file))
#infile=open(from_file)
#indata=infile.read()
#indata = open(from_file).read()
#print("The input file is %s bytes long" %len(indata))
#print("Does the output file exists? \n%r" %exists(to_file))
#if(not exists(to_file)):
#	print("Create new file %r" %to_file)
#print("Ready, hit RETURN to continue, CRTL-C to abourt.")
#input()
#out_file=open(to_file,'w')
#out_file.write(indata)
#print("Alright,all done")
#open(from_file).close()
#out_file.close()
#～～～～
#浓缩成一行
#open(to_file,'w').write(open(from_file).read())
#----------------------------------------------------------------------------------------------------------
#administrator/business0713
#from sys import argv
#script , from_file = argv
#def print_all(f):
#	print(f.read())
#def rewind(f):
#	f.seek(0)
#def print_a_line(lineNum,f):
#	print(lineNum,f.readline())
#current_fille=open(from_file)
#print_all(current_fille)
#rewind(current_fille)
#lineNum = 1
#print_a_line(lineNum,current_fille)
#print_a_line(lineNum,current_fille)
#print_a_line(lineNum,current_fille)
#print_a_line(lineNum,current_fille)
#文件读取之前要先调用open()函数然后再调用read()或者write()等函数
#------------------------------------------------------------------------------------------------------------
#c+=a相当于c=c+a c*=a相当于c=c*a
#------------------------------------------------------------------------------------------------------------
#def break_words(stuff):
#	print ("""This function will break up words for us.""")
#	words = stuff.split(' ')
#	return words
#def sort_words(words):
#	print("""Sorts the words.""")
#	return sorted(words)
#def print_first_word(words):
#	print("""Prints the first word after popping it off.""")
#	word = words.pop(0)
#	print(word)
#def print_last_word(words):
#	print("""Prints the last word after popping it off.""")
#	word = words.pop(-1)
#	print (word)
#def sort_sentence(sentence):
#	print("""Takes in a full sentence and returns the sorted words.""")
#	words = break_words(sentence)
#	return sort_words(words)
#def print_first_and_last(sentence):
#	print("""Prints the first and last words of the sentence.""")
#	words = break_words(sentence)
#	print_first_word(words)
#	print_last_word(words)
#def print_first_and_last_sorted(sentence):
#	print("""Sorts the words then prints the first and last one.""")
#	words = sort_sentence(sentence)
#	print_first_word(words)
#	print_last_word(words)
#-------------------------------------------------------------------------------------------------------------
#a = [1,2,3]
#b = [4,5,6]
#c = [a,b]
#for i in c:
#	print(i)
#	for j in i:
#		print(j)
#a = []
#b = []
#c = []
#for i in range(1,4):
#	a.append(i)
#c.append(a)
#for i in range(4,7):
#	b.append(i)
#c.append(b)
#print(a)
#print(b)
#print(c)
#---------------------------------------------------------------------------------------------------------------
#from sys import exit
#def gold_room():
#	print ("This room is full of gold. How much do you take?")
#	next = input("> ")
#	if "0" in next or "1" in next:#判断接下来的输入中是否有1或者0  这里写入不正确，不能识别22是数字 a1不是数字
#		how_much = int(next)
#	else:
#		dead("Man, learn to type a number.")
#	if how_much < 50:
#		print ("Nice, you're not greedy, you win!")
#		exit(0)
#	else:
#		dead("You greedy bastard!")
#def bear_room():
#	print ("There is a bear here.")
#	print ("The bear has a bunch of honey.")
#	print ("The fat bear is in front of another door.")
#	print ("How are you going to move the bear?")
#	bear_moved = False
#	while True:
#		next = input("> ")
#		if next == "take honey":
#			dead("The bear looks at you then slaps your face off.")
#		elif next == "taunt bear" and not bear_moved:
#			print ("The bear has moved from the door. You can go through it now.")
#			bear_moved = True
#		elif next == "taunt bear" and bear_moved:
#			dead("The bear gets pissed off and chews your leg off.")
#		elif next == "open door" and bear_moved:
#			gold_room()
#		else:
#			print ("I got no idea what that means.")
#def cthulhu_room():
#	print ("Here you see the great evil Cthulhu.")
#	print ("He, it, whatever stares at you and you go insane.")
#	print ("Do you flee for your life or eat your head?")
#	next = input("> ")
#	if "flee" in next:
#		start()
#	elif "head" in next:
#		dead("Well that was tasty!")
#	else:
#		cthulhu_room()
#def dead(why):
#	print (why, "Good job!")
#	exit(0)
#def start():
#	print ("You are in a dark room.")
#	print ("There is a door to your right and left.")
#	print ("Which one do you take?")
#	next = input("> ")
#	if next == "left":
#		bear_room()
#	elif next == "right":
#		cthulhu_room()
#	else:
#		dead("You stumble around the room until you starve.")
#start()
#-----------------------------------------------------------------------------------------------------------
#sys.argv[0]显示的是当前python脚本的绝对路径
#import sys
#import os
#print("script path is : %s" %sys.argv[0])
#ini_file = os.path.join(sys.path[0],'temp.txt')
#print(ini_file)
#-----------------------------------------------------------------------------------------------------------
#!/usr/bin/env python
#coding: utf-8
 
#import urllib.request
##import urllib2
#import os
#import re
#import sys
# 
##显示下载进度
#def schedule(a,b,c):
#    '''
#    a:已经下载的数据块
#    b:数据块的大小
#    c:远程文件的大小
#    '''
#    per = 100.0 * a * b / c
#    if per > 100 :
#        per = 100
#    print ('%.2f%%' % per)
# 
##获取html源码
#def getHtml(url):
#    page = urllib.request.urlopen(url)
#    html = page.read()
#    return html
# 
##下载图片
#def downloadImg(html, num, foldername):
#    picpath = '%s' % (foldername)       #下载到的本地目录
#    if not os.path.exists(picpath):     #路径不存在时创建一个
#        os.makedirs(picpath)
#    target = picpath+'/%s.jpg' % num
#    myItems = re.findall('<p><a href="http:\/\/www.mzitu.com/.*?" ><img src="(.*?)" alt=".*?" /></a></p>',html,re.S)
#    print ('Downloading image to location: ' + target)
#    urllib.urlretrieve(myItems[0], target, schedule)
# 
##正则匹配分页
#def findPage(html):
#    myItems = re.findall('<span>(\d*)</span>', html, re.S)
#    return myItems.pop()
# 
##正则匹配列表
#def findList(html):
#    myItems = re.findall('<h2><a href="http://www.mzitu.com/(\d*)" title="(.*?)" target="_blank">.*?</a></h2>', html, re.S)
#    return myItems
# 
##总下载
#def totalDownload(modelUrl):
#    listHtml5 = getHtml(modelUrl)
#    listContent = findList(listHtml)
#    for list in listContent:
#        html = getHtml('http://www.mzitu.com/' + str(list[0]))
#        totalNum = findPage(html)
#        for num in range(1, int(totalNum)+1):
#            if num == 1:
#                url = 'http://www.mzitu.com/' + str(list[0])
#                html5 = getHtml(url)
#                downloadImg(html5, str(num), str(list[1]))
#            else:
#                url = 'http://www.mzitu.com/' + str(list[0]) + '/'+str(num)
#                html5 = getHtml(url)
#                downloadImg(html5, str(num), str(list[1]))
# 
#if __name__ == '__main__':
#    listHtml = getHtml('http://www.mzitu.com/model')    #这是其中一个模块的url，可以添加不同的模块url从而达到整站爬取。
#    for model in range(1, int(findPage(listHtml))+1):
#        if model == 1:
#            modelUrl = 'http://www.mzitu.com/model'
#            totalDownload(modelUrl)
#        else:
#            modelUrl = 'http://www.mzitu.com/model/page/' + str(model)
#            totalDownload(modelUrl)
#    print ("Download has finished.")
#---------------------------------------------------------------------------------------------------------------------------------
# encoding:utf-8

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 07 17:30:58 2015
 
@author: Dreace
"""
import urllib
import sys
import time
import os
import random
from multiprocessing.dummy import Pool as ThreadPool 
type_ = sys.getfilesystemencoding()
def rename():
    return time.strftime("%Y%m%d%H%M%S")
def rename_2(name):  
    if len(name) == 2:  
        name = '0' + name + '.jpg' 
    elif len(name) == 1:  
        name = '00' + name + '.jpg' 
    else:  
        name = name + '.jpg' 
    return name
def download_pic(i):
    global count
    global time_out
    if Filter(i):
        try: 
            content = urllib.urlopen(i,timeout = time_out)
            url_content = content.read()
            file_name = repr(random.randint(10000,999999999)) + "_" + rename_2(repr(count))
            f = open(file_name,"wb")
            f.write(url_content)
            f.close()
            if os.path.getsize(file_name) >= 1024*11:
                count += 1
            else:
                os.remove(file_name)
        except:
            print (1)
def Filter(content):
    for line in Filter_list:
        if content.find(line) == -1:
            return True
def get_pic(url_address):
    global pic_list
    global time_out
    global headers
    try:
        req = urllib.Request(url = url_address,headers = headers)
        str_ = urllib.urlopen(req, timeout = time_out).read()
        url_content = str_.split("\'")
        for i in url_content:
            if i.find(".jpg") != -1:
                pic_list.append(i)   
    except:
        print (2)
MAX = 100
count = 0
time_out = 60
thread_num = 50
pic_list = []
page_list = []
pic_kind = ["hot","share","mm","taiwan","japan","model"]
Filter_list = ["imgsize.ph.126.net","img.ph.126.net","img2.ph.126.net"]
dir_name = "C:\Photos\\"+rename()
os.makedirs(dir_name)
os.chdir(dir_name)
start_time = time.time()
url_address = "http://www.mzitu.com/model/page/"
headers = {"User-Agent":" Mozilla/5.0 (Windows NT 10.0; rv:39.0) Gecko/20100101 Firefox/39.0"}
for pic_i in pic_kind:     
    for i in range(1,MAX + 1):  
        page_list.append(url_address + pic_i + "/page/" + repr(i))
page_pool = ThreadPool(thread_num)
page_pool.map(get_pic,page_list)
page_pool.close()
page_pool.join()
print ("获取到".encode(type_),len(pic_list),"张图片，开始下载！".encode(type_))
pool = ThreadPool(thread_num) 
pool.map(download_pic,pic_list)
pool.close() 
pool.join()
#print (count,"张图片保存在".encode(type_) + dir_name)
#print ("共耗时".encode(type_),time.time() - start_time,"s")


















