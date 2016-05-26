# -*- coding: utf-8 -*- 

'''
前提：设置SAWVcmd的PATH环境变量
popen的参数，第一个为字符串（或者也可以为多个非命名的参数），表示你要执行的命令和命令的参数；后面的均为命名参数；
shell=True,表示你前面的传入的命令将在shell下执行，如果你的命令是个可执行文件或bat，不需要指定此参数；
stdout=subprocess.PIPE用来将新进程的输出重定向，
stderr=subprocess.STDOUT将新进程的错误输出重定向到stdout，
stdin=subprocess.PIPE用来将新进程的输入重定向；
universal_newlines=True表示以text的方式打开stdout和stderr。
'''

import sys
import subprocess
import os
#import unicodedata
import chardet
import time
import pfile
import stat
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

#设置VSS默认访问方式
#vss_arvg = r'-server 192.168.55.61 -port 8877 -username yuanhuangliang -pwd 123456 -alias htsc_vss'
#vss_tmpdir = r'-tempdir c:\temp'
ini_file = os.path.join(sys.path[0],'ck.conf')
cf = ConfigParser.ConfigParser()
cf.read(ini_file)
vss_arvg = unicode(cf.get("vss", "arvg"))
vss_tmpdir = unicode(cf.get("vss", "tmpdir"))
ISOTIMEFORMAT = u'%Y-%m-%d %X'
nowtime = time.strftime( ISOTIMEFORMAT,time.localtime())

	
def _excmd_(vcmd):
	vcmd = vcmd.encode('gbk','ignore')	#windows 命令默认只识别编码格式gbk，需格式转换
	#print nowtime
	pfile.write_list('vss.log',[0,nowtime,vcmd+'\n'])
	#print vcmd
	#print type(vcmd)
	#print chardet.detect(vcmd)
	#os.system(vcmd)
	child=subprocess.Popen(vcmd,shell = True)
	#shell设置为true 表示命令将通过shell执行 默认为false
	#child=subprocess.check_call(vcmd,shell = True)
	#print child
	child.wait()
	'''
	subprocess.call('脚本/shell', shell=True)
	效果等同于
	s = subprocess.Popen('脚本/shell', shell=True)
	s.wait()
	区别是 前者无阻塞和主程序同步执行 后者需要等命令执行完毕
	'''
	#child.communicate()
	#print child.stderr
	#print child.returncode
	
def GetFile(vss_prj,work_dir,vss_file):
	file_path = ur'%s\%s' %(work_dir,vss_file)
	pfile.rm_file(file_path)
	prj = '-prj '+vss_prj
	workdir = '-workdir '+work_dir
	file = '-file '+vss_file
	vsscmd ='SAWVcmd GetFile %s %s %s %s %s' %(vss_arvg,workdir,prj,file,vss_tmpdir)
	#print vsscmd
	#vsscmd = unicodedata.normalize('NFD',vsscmd)
	#vsscmd = r'SAWVcmd GetFile -server 192.168.55.61 -port 8877 -username huzhonghai -pwd 7216797 -alias htsc_vss -workdir D:\SVN\tmp\DEV\8.1.1\build04\ACRM\pkg -prj $/源码管理/DEV/ACRM/后端/PACKAGE -file ZS.pck -tempdir c:\\temp'
	_excmd_(vsscmd)
	
def AddFile(vss_prj,work_dir,vss_file):
	prj = r'-prj '+vss_prj
	workdir = r'-workdir '+work_dir
	file = r'-file '+vss_file
	vsscmd ='SAWVcmd AddFile %s %s %s %s %s' %(vss_arvg,workdir,prj,file,vss_tmpdir)
	_excmd_(vsscmd)
	
def CheckOutFile(vss_prj,work_dir,vss_file):
	prj = r'-prj '+vss_prj
	workdir = r'-workdir '+work_dir
	file = r'-file '+vss_file
	vsscmd ='SAWVcmd CheckOutFile %s %s %s %s %s' %(vss_arvg,workdir,prj,file,vss_tmpdir)
	_excmd_(vsscmd)
	
def undoCheckOutFile(vss_prj,work_dir,vss_file):
	prj = r'-prj '+vss_prj
	workdir = r'-workdir '+work_dir
	file = r'-file '+vss_file
	vsscmd ='SAWVcmd undoCheckOutFile %s %s %s %s %s' %(vss_arvg,workdir,prj,file,vss_tmpdir)
	_excmd_(vsscmd)
	
def CheckInFile(vss_prj,work_dir,vss_file,vss_comment):
	prj = r'-prj '+vss_prj
	workdir = r'-workdir '+work_dir
	file = r'-file '+vss_file
	comment = r'-comment '+vss_comment
	vsscmd ='SAWVcmd CheckInFile %s %s %s %s %s %s' %(vss_arvg,workdir,prj,file,vss_tmpdir,comment)
	_excmd_(vsscmd)
	
'''
常用vss步骤：
1. get files from dev environment;
2. add the files into uat environment;
3. checkout files from uat environment; 
4. checkin files into uat environment
'''
def main_vss(dev_vss,dev_dir,vss_file,release,build):
	uat_vss = dev_vss.replace('/DEV','/UAT')
	uat_dir = dev_dir.replace(r'\DEV',r'\UAT')
	vss_comment = release+'_'+build
	#dev->local->uat
	GetFile(dev_vss,dev_dir,vss_file)
	AddFile(uat_vss,dev_dir,vss_file)
	CheckOutFile(uat_vss,uat_dir,vss_file)
	CheckInFile(uat_vss,dev_dir,vss_file,vss_comment)
	


#GetFile(dev_vss,dev_dir,vss_file)
#main_vss(dev_vss,dev_dir,vss_file,release,build)
		
