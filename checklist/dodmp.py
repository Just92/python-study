# -*- coding: utf-8 -*- 

import sys
import time
import os
import shutil
import chardet
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf-8')

par_path = os.path.join(sys.path[0],'dmp')

def dmp_exp(dmp_path, par_path= ur'.\dmp'):
	try:
		dmp_cmd =ur'exp epsdb_lot2/password@acrm_dev  parfile=%s\exp_acrm.par file=%s\epsdb_lot2.dmp' %(par_path,dmp_path)
		#print chardet.detect(dmp_cmd)
		print u'[INFO]开发环境 DEV 前端数据库dmp导出'
		print dmp_cmd
		dmp_cmd = dmp_cmd.encode('gbk','ignore')	#windows 命令默认只识别编码格式gbk，需格式转换
		wincmd = os.system(dmp_cmd)
		assert wincmd == 0
		print u"--成功导出前端库"		
	except Exception as ex:
		print u"[ERROR]导出有问题!!!"
		print Exception,":",ex 
		
def epsdb_del(par_path = ur'.\dmp'):
	try:
		dmp_cmd =ur'sqlplus epsdb_lot2/password@acrm_uat @%s\epsdb_del.sql' %(par_path)
		#print chardet.detect(dmp_cmd)
		print u'[INFO]测试环境 UAT 前端数据 epsdb_del 删除'
		print dmp_cmd
		dmp_cmd = dmp_cmd.encode('gbk','ignore')	#windows 命令默认只识别编码格式gbk，需格式转换
		wincmd = os.system(dmp_cmd)
		assert wincmd == 0
		print u"--成功删除数据"		
	except Exception as ex:
		print u"[ERROR]删除有问题!!!"
		print Exception,":",ex 
		
def epsdb_sel(par_path = ur'.\dmp'):
	try:
		dmp_cmd =ur'sqlplus easyetl/password@acrm_uat @%s\epsdb_sel.sql' %(par_path)
		#print chardet.detect(dmp_cmd)
		print u'[INFO]测试环境 UAT 前端数据 epsdb_sel 查询'
		print dmp_cmd
		dmp_cmd = dmp_cmd.encode('gbk','ignore')	#windows 命令默认只识别编码格式gbk，需格式转换
		wincmd = os.system(dmp_cmd)
		assert wincmd == 0
		print u"--成功查询数据"		
	except Exception as ex:
		print u"[ERROR]查询有问题!!!"
		print Exception,":",ex

def dmp_imp(dmp_path, par_path= ur'.\dmp'):
	try:
		dmp_cmd =ur'imp epsdb_lot2/password@acrm_uat parfile=%s\imp_acrm.par file=%s\epsdb_lot2.dmp' %(par_path,dmp_path)
		#print chardet.detect(dmp_cmd)
		print u'[INFO]测试环境 UAT 前端数据库dmp导入'
		print dmp_cmd
		dmp_cmd = dmp_cmd.encode('gbk','ignore')	#windows 命令默认只识别编码格式gbk，需格式转换
		wincmd = os.system(dmp_cmd)
		assert wincmd == 0
		print u"--成功导入前端库"		
	except Exception as ex:
		print u"[ERROR]导入有问题!!!"
		print Exception,":",ex 


#前端数据库导入
def dmp_do(dmp_path = ur"D:\上线\DEV"):
	try:
		dmp_dir = dmp_path+r"\clear_data.bat"
		dmp_log = dmp_path+r"\dmp.log"
		dmp_cmd = r'%s >%s 2>&1' %(dmp_dir,dmp_log)
		dmp_cmd =ur'exp epsdb_lot2/password@acrm_dev  parfile=D:\上线\DEV\exp_acrm.par file=D:\上线\DEV\epsdb_lot2.dmp'
		#print chardet.detect(dmp_cmd)
		dmp_cmd = dmp_cmd.encode('gbk','ignore')	#windows 命令默认只识别编码格式gbk，需格式转换
		print u'[INFO]前端数据库dmp导出并导入(dev2uat) 执行"%s"' %dmp_dir
		wincmd = os.system(dmp_cmd)
		assert wincmd == 0
		print u"--成功导入前端库"		
	except Exception as ex:
		print u"[ERROR]导入有问题!!!"
		f = open(dmp_log,"r")
		rows = f.readlines()
		for row in rows:
			print ''.join(row.split())
		print Exception,":",ex 
		sys.exit()
		
def test():
	release = r'8.3.1'
	build = r'build00'
	root_dir =ur'D:\上线\DEV'
	build_dir = root_dir+'\\'+release+'\\'+build
	dmp_do(root_dir)
	#src_path = (r'%s\epsdb_lot2.dmp' %root_dir).encode('gbk','ignore')
	#dst_path = (r'%s\epsdb_lot2.dmp' %build_dir).encode('gbk','ignore')
	#print u'[INFO]:复制DMP文件到: %s' %build_dir
	#shutil.copyfile(src_path, dst_path)
	#print u'--成功复制文件 %s\epsdb_lot2.dmp' %root_dir
	
if __name__=="__main__":
        ini_file = os.path.join(sys.path[0],'ck.conf')
	cf = ConfigParser.ConfigParser()
	cf.read(ini_file)
	release = unicode(cf.get("vss_ck", "release"))
	build = unicode(cf.get("release", "build"))
	root_dir = unicode(cf.get("public", "rootpath"))
	build_dir = root_dir+'\\'+release+'\\'+build
	dmp_path = build_dir
	par_path = os.path.join(sys.path[0],'dmp')
	print u'[INFO]:处理dmp文件 %s' %dmp_path
	dmp_exp(dmp_path, par_path)
	epsdb_sel(par_path)
	epsdb_del(par_path)	#test
	dmp_imp(dmp_path, par_path)	#test
	print u'dmp: 请手动重启epsdb_lot2对应java前端'
