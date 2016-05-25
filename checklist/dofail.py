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
reload(sys)
sys.setdefaultencoding('utf-8')

#for line in open(r'D:\SVN\tmp\DEV\8.1.1\build04\dir.list'):
	
'''
根据dir.list文件内容进行处理
oracle sql job
'''
#对获取的对象进行处理			
def oracle_do(root_dir,release,build):
	nowdate = time.strftime('%Y%m%d',time.localtime(time.time()))
	build_dir = root_dir+'\\'+release+'\\'+build
	dfile = build_dir+'\\'+r'dir.list'
	#获取VSS路径并执行
	lines = pfile.readtext(dfile)
	lines.sort(reverse = True)	#排序
	warn_list =[]
	sql_list = []
	acrm_hostname = u'192.168.55.77'
	acrm_port = 22
	acrm_username = u'easyetl'
	acrm_password = u'easyetl123'
	try:
		#print lines
		for line in lines:
			#print line
			gline = unicode(line.encode('gbk','ignore'),'gbk').strip()	#筛选异常编码并首尾去空
			rlist = gline.split(',')	#以分隔符','拆分字符串为数组
			systype = rlist[2]
			dpath = rlist[5]
			warn_info = ()
			#根据文件来源(easyetl/eps/oracle/sql/job)处理文件
			if rlist[3] == r'eps': 
				print u'[INFO]:处理EPS报表文件' 
				src_base = ur'%s\ACRM\eps' %build_dir
				src = rlist[5]
				relpath = src.replace(src_base,'')	#获取相对路径
				#dst_base = ur'\\192.168.55.51\eps_share\eps'
				dst_base = ur'\\192.168.55.80\vss_tmp'	#test
				dst = ur'%s%s' %(dst_base,relpath)
				if not os.path.isdir(dst):
					os.makedirs(dst)
				print u'[INFO]:拷贝EPS报表文件 "%s"' %src
				pfile._copyFiles_(src,dst)
			elif rlist[3] == r'easyetl':
				print u'[INFO]:处理EASYETL主机文件' 
				remotepath = r'/app11/easyetl/tmp/yhl'	#test /tmp/yhl
				localpath = ur'%s\ACRM\easyetl' %build_dir
				print u'[INFO]:上传EASYETL主机文件 "%s --> %s"' %(localpath,acrm_hostname)
				pssh.upload_dir_win2unix(acrm_hostname,acrm_port,acrm_username,acrm_password,remotepath,localpath)
			elif rlist[3] == r'sql':
				print u'[INFO]:处理SQL文件' 
				sql_info = u'%s,%s,%s' %(rlist[2],rlist[3],rlist[5])
				sql_list.append(sql_info)	#生成SQL信息数组
				#print sql_list
			elif u'oracle' in  rlist[3]:
				print u'[INFO]:处理ORACLE对象文件' 
				warn_info = u'oracle: 请手动在PL/SQL中登录数据库 %s 执行目录 %s 下的ORACLE对象文件' %(systype,dpath)
			elif rlist[3] == r'job':
				print u'[INFO]:处理JOB文件' 
				warn_info = u'job: 请手动在服务器 %s:/app11/easyetl 中导入JOB文件，执行命令: job_import %s.job' %(acrm_hostname,nowdate)
			elif rlist[3] == r'dmp':
				print u'[INFO]:处理dmp文件' 
				dmp_path = build_dir
				dodmp.dmp_exp(dmp_path, par_path= ur'.\dmp')
				dodmp.epsdb_sel(par_path = ur'.\dmp')
				#dodmp.epsdb_del(par_path = ur'.\dmp')	#test
				#dodmp.dmp_imp(dmp_path, par_path= ur'.\dmp')	#test
				warn_info = u'dmp: 请手动重启epsdb_lot2对应java前端'
			elif rlist[3] == r'java':
				print u'[INFO]:处理JAVA文件' 
				java_list = r'%s\%s_java.list' %(rlist[5],release)
				javawars = pfile.readtext(java_list)
				print javawars
				for war in javawars:
					warn_info = u'java: 请发布java前端包 %s' %war
			#提示信息返回
			if any(warn_info):
				warn_list.append(warn_info) 
	except Exception as ex:
		print(u"[ERROR]:对象处理失败！%s" %line)
		print Exception,":",ex
	#执行后续步骤
	try:
		if sql_list is not None:	#若存在SQL脚本
			sql_list = list(set(sql_list))	#去重
			#print sql_list
			for sql_info in sql_list:
				info_list = sql_info.split(',')
				systype = info_list[0]
				dpath = info_list[2]
				dfile_name = u'%s_%s_%s.sql' %(systype,release,build)
				dstfile = ur'%s\%s' %(dpath,dfile_name)
				rfile = u'1.list'
				if os.path.exists(os.path.join(dpath,rfile)):
					print u'[INFO]:合并SQL文件'
					pfile.merge_file(dpath,rfile,dstfile)
				#按系统类型处理SQL
				if systype == u'GP':
					1==1
					remotepath = r'/app11/easyetl/tmp'
					localpath = dpath
					print u'[INFO]:上传GP SQL文件 "%s\%s --> %s"' %(localpath,dfile_name,acrm_hostname)
					pssh.sftp_put(acrm_hostname,acrm_port,acrm_username,acrm_password,remotepath,localpath,dfile_name)
					sql_warn = u'gp: 请手动执行服务器 %s:%s 中GP SQL脚本，命令: gd -f %s' %(acrm_hostname,remotepath,dfile_name)
				else:
					sql_warn = u'oracle: 请手动在PL/SQL中登录数据库 %s 执行SQL脚本 %s\%s' %(systype,dpath,dfile_name)
				warn_list.append(sql_warn)
	except Exception as ex:
		print(u"[ERROR]:对象后续处理失败！%s" %line)
		print Exception,":",ex
	#返回
	return warn_list
			

def _main_(root_dir,release,build,MYSPACE):
	warnlist=list_do_obj(root_dir,release,build,MYSPACE)
	obj_do(root_dir,release,build)
	#print warnlist
	#警告信息输出
	pfile.warn_prompt(warnlist)
				
		
if __name__=="__main__":
	#设置传递参数
	print sys.argv
	if sys.argv[1] is None:
		print u"[WARN]:命令执行示例：%s %s %s" %(sys.argv[0],sys.argv[1],sys.argv[2])
	release = sys.argv[1]
	build= sys.argv[2] #build= u'build01'
	root_dir = ur'D:\上线\DEV'
	MYSPACE = r'a.backend'
	start = time.time()		
	#_main_(root_dir,release,build)
	obj_do(root_dir,release,build)
	c = time.time() - start
	print(u'[INFO]:程序运行耗时:%0.2f'%(c))