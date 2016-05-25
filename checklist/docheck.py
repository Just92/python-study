# -*- coding: utf-8 -*- 

import sys
import pvss
import psvn
import pfile
import pssh
import dojob
import dodmp
import time
import shutil
import os
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf-8')

#for line in open(r'D:\SVN\tmp\DEV\8.1.1\build04\dir.list'):
	
'''
根据dir.list文件内容进行处理
'''
ini_file = os.path.join(sys.path[0],'ck.conf')
cf = ConfigParser.ConfigParser()
cf.read(ini_file)
acrm_uat_host = unicode(cf.get("ssh_acrm_uat", "hostname"))
acrm_dev_host = unicode(cf.get("ssh_acrm_dev", "hostname"))

	
def list_check(root_dir,release,build,MYSPACE):
	nowdate = time.strftime('%Y%m%d',time.localtime(time.time()))
	build_dir = root_dir+'\\'+release+'\\'+build
	dfile = build_dir+'\\'+r'dir.list'
	#print dfile
	#获取VSS路径并执行
	lines = pfile.readtext(dfile)
	lines.sort(reverse = True)	#排序
	#print lines
	warn_list =[]
	try:
		print u"[INFO]:检测文件准确性"
		for line in lines:
			line = unicode(line.encode('gbk','ignore'),'gbk').strip()	#筛选异常编码并首尾去空
			rlist = line.split(',')	#以分隔符','拆分字符串为数组
			#根据文件来源(VSS/SVN/CK)处理,获取文件
			if rlist[0] == r'SVN':
				dev_dir = rlist[5]
				dev_file = dev_dir+'\\'+r'1.list'
				flist = pfile.readtext(dev_file)
				#wpath_list = []
				exp_num = 0
				print u"--检测SVN文件: %s" %(dev_dir)
				for file in flist:
					dev_url = file.strip()
					warn = psvn.check_exist(dev_url)	#开发分支导出文件
					warn_list.append(warn)
					#print stdout
					exp_num +=1
				print u'[INFO]:SVN文件检查个数 %s' %exp_num
				warn_list = list(set(warn_list))
				if any(warn_list):
					warn_list.sort(reverse = True)	#排序
					for warnvalue in warn_list:
						if warnvalue == None:
							continue
						print u'--%s' %warnvalue
					sys.exit()
			'''elif rlist[0] == r'CK':
				if rlist[3] == r'job':
					1 == 1	
					job_path = r'%s\%s\%s' %(root_dir,release,build)
					dojob.job_do(job_path,release,build,from_host = acrm_dev_host,to_host = acrm_uat_host)
				
				else:
					1==1
					#print u'#####需手动处理#####'
					#print u'系统%s 类型%s 目录%s' %(rlist[2],rlist[3],rlist[5])
					#print u'####################'	
					#ACRM,sql/ACRM,java/ACRM,dmp/ALL,job
					'''
		#异常抛出
		#print stdout_list
	except Exception as ex:
		print(u"[ERROR]:list文件检查文件有问题！%s" %line)
		print Exception,":",ex	
		sys.exit()	
		
if __name__=="__main__":
	release = r'8.3.1'
	build = r'build03'
	root_dir = ur'D:\上线\DEV'
	MYSPACE = r'a.backend'
	start = time.time()		
	#_main_(root_dir,release,build)
	obj_do(root_dir,release,build)
	c = time.time() - start
	print(u'[INFO]:程序运行耗时:%0.2f'%(c))