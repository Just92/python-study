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
import sys
import os
print("script path is : %s" %sys.argv[0])
ini_file = os.path.join(sys.path[0],'temp.txt')
print(ini_file)
#-----------------------------------------------------------------------------------------------------------






















