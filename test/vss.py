#/usr/bin/python
# -*- coding: utf-8 -*- 
#sys模块 sys模块包含了与Python解释器和它的环境有关的函数
import sys
#subprocess模块 subprocess包中定义有数个创建子进程的函数，这些函数分别以不同的方式创建子进程，所以我们可以根据需要来从中选取一个使用
import subprocess  
#os模块，用来执行cmd/shell/linux等命令
import os  
#读取配置文件的模块
import configparser

"""
1)基本的读取配置文件
    -read(filename) 直接读取ini文件内容
    -sections() 得到所有的section，并以列表的形式返回
    -options(section) 得到该section的所有option
    -items(section) 得到该section的所有键值对
    -get(section,option) 得到section中option的值，返回为string类型
    -getint(section,option) 得到section中option的值，返回为int类型，还有相应的getboolean()和getfloat() 函数。
 
2)基本的写入配置文件
    -add_section(section) 添加一个新的section
    -set( section, option, value) 对section中的option进行设置，需要调用write将内容写入配置文件。
"""
#reload(sys)
#sys.setdefaultencoding('utf-8')
#python 3 默认utf-8编码
#print(sys.getdefaultencoding())
#vsscmd = r'SAWVcmd GetFile -server 192.168.55.61 -port 8877 -username huzhonghai -pwd 7216797 -alias htsc_vss -workdir D:\SVN\tmp\DEV\8.1.1\build04\ACRM\pkg -prj $/源码管理/DEV/ACRM/后端/PACKAGE -file ZS.pck -tempdir c:\\temp'
cf=configparser.ConfigParser()
cf.read('ck.conf',encoding='utf-8')
cntPara = cf.get('vss','arvg')
prj = cf.get('vss_ck','project')
#release = cf.get('vss_ck','release')
fileName = cf.get('vss_ck','file')
print('cntpara is %r,' %cntPara)
print('prj is %r,' %prj)
#print('release is %r,' %release)
print('fileName is %r,' %fileName)

def exCmd(cmd):
	child = subprocess.Popen(cmd,shell = True)
	child.wait()
def getfile(build_num,localdir):
		Vss_dir = r''