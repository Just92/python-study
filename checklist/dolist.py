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

	
def list_do_obj(root_dir,release,build,MYSPACE):
	nowdate = time.strftime('%Y%m%d',time.localtime(time.time()))
	build_dir = root_dir+'\\'+release+'\\'+build
	dfile = build_dir+'\\'+r'dir.list'
	#print dfile
	#获取VSS路径并执行
	lines = pfile.readtext(dfile)
	lines.sort(reverse = True)	#排序
	#print lines
	stdout_list =[]
	try:
		for line in lines:
			line = unicode(line.encode('gbk','ignore'),'gbk').strip()	#筛选异常编码并首尾去空
			rlist = line.split(',')	#以分隔符','拆分字符串为数组
			#根据文件来源(VSS/SVN/CK)处理,获取文件
			if rlist[0] == r'VSS':
				#dev_vss = rlist[4].rstrip('\\')
				dev_dir = rlist[5]
				print u"[INFO]:写入文件目录: %s" %dev_dir
				dev_file = dev_dir+'\\'+r'1.list'
				flist = pfile.readtext(dev_file)
				for file in flist:
					vss_files = file.split(' ')
					dev_vss = vss_files[0].rstrip('\\')
					vss_file =vss_files[1]
					print u"--获取VSS文件: %s/%s" %(dev_vss,vss_file.strip())
					if rlist[3] in ('sql','readme'):
						pvss.GetFile(dev_vss,dev_dir,vss_file)
					else:
						pvss.GetFile(dev_vss,dev_dir,vss_file) 
						pvss.main_vss(dev_vss,dev_dir,vss_file,release,build)	#test
			elif rlist[0] == r'SVN':
				dev_dir = rlist[5]
				print u"[INFO]:写入文件目录: %s" %dev_dir
				dev_file = dev_dir+'\\'+r'1.list'
				flist = pfile.readtext(dev_file)
				wpath_list = []
				exp_num = 0
				try:
					for file in flist:
						dev_url = file.strip()
						if any(dev_url) is False:
							continue
						print u"--获取SVN文件%s: %s" %(exp_num+1,dev_url)
						(work_path,stdout) = psvn.export_dev_file(dev_url,build_dir)	#开发分支导出文件
						m_info = release+'_'+build
						#print work_path
						wpath_list.append(work_path)
						stdout_list.append(stdout)
						#print stdout
						exp_num +=1
					print u'[INFO]:开发分支export导出文件个数 %s' %exp_num
					wpath = list(set(wpath_list))[0]
				except Exception as ex:
					print(u"[ERROR]:SVN导出失败")
					print Exception,":",ex 
					sys.exit()
				print wpath	
				if rlist[3] != r'sql':
					1==1
					psvn.src2uat_file(MYSPACE,wpath,build_dir,m_info)	#开发导出的文件同步到UAT分支 #test
			elif rlist[0] == r'CK':
				if rlist[3] == r'job':
					1 == 1	
					job_path = r'%s\%s\%s' %(root_dir,release,build)
					dojob.job_do(job_path,release,build,from_host = acrm_dev_host,to_host = acrm_uat_host)
				'''elif rlist[3] == r'dmp':
					#dmp_path = root_dir
					dmp_path = build_dir
					dodmp.dmp_exp(dmp_path, par_path= ur'.\dmp')
					#复制epsdb_lot2.dmp
					#src_path = (r'%s\epsdb_lot2.dmp' %root_dir).encode('gbk','ignore')
					#dst_path = (r'%s\epsdb_lot2.dmp' %build_dir).encode('gbk','ignore')
					#print u'[INFO]:复制DMP文件到: %s' %build_dir
					#shutil.copyfile(src_path, dst_path)
					#print u'--成功复制文件 %s\epsdb_lot2.dmp' %root_dir
				else:
					1==1
					#print u'#####需手动处理#####'
					#print u'系统%s 类型%s 目录%s' %(rlist[2],rlist[3],rlist[5])
					#print u'####################'	
					#ACRM,sql/ACRM,java/ACRM,dmp/ALL,job
					'''
		#异常抛出
		#print stdout_list
		slist = list(set(stdout_list))	#去重
		return slist
	except Exception as ex:
		print(u"[ERROR]:list文件处理失败！%s" %line)
		print Exception,":",ex	
		sys.exit()
	
#中间步骤：合并sql文件  暂未使用
def mid_do():
	build_dir = root_dir+'\\'+release+'\\'+build
	dfile = build_dir+'\\'+r'dir.list'
	#获取VSS路径并执行
	lines = pfile.readtext(dfile)
	lines.sort(reverse = True)	#排序
	sql_dlist = []
	for line in lines:	
		line = unicode(line.encode('gbk','ignore'),'gbk').strip()	#筛选异常编码并首尾去空
		rlist = line.split(',')	#以分隔符','拆分字符串为数组
		systype = rlist[2]
		dpath = rlist[5]
		if rlist[3] == r'sql':
			sql_list = [rlist[2],rlist[3],rlist[5]]
			sql_dlist.append(sql_list)
			dpath = rlist[5]
			dfile_name = u'%s_%s_%s.sql' %(systype,release,build)
			dstfile = ur'%s\%s' %(dpath,dfile_name)
			rfile = u'1.list'
			if os.path.exists(os.path.join(dpath,rfile)):
				print u'[INFO]:合并SQL文件'
				pfile.merge_file(dpath,rfile,dstfile)

#对获取的对象进行处理			
def obj_do(root_dir,release,build):
	nowdate = time.strftime('%Y%m%d',time.localtime(time.time()))
	build_dir = root_dir+'\\'+release+'\\'+build
	dfile = build_dir+'\\'+r'dir.list'
	#获取VSS路径并执行
	lines = pfile.readtext(dfile)
	lines.sort(reverse = True)	#排序
	warn_list =[]
	sql_list = []
	ssh_htsc=pssh.htsc()
	'''
	acrm_hostname = u'192.168.55.77'
	acrm_port = 22
	acrm_username = u'easyetl'
	acrm_password = u'easyetl123'
	'''
	try:
		#print lines
		for line in lines:
			#print line
			gline = unicode(line.encode('gbk','ignore'),'gbk').strip()	#筛选异常编码并首尾去空
			rlist = gline.split(',')	#以分隔符','拆分字符串为数组
			systype = rlist[2]
			dpath = rlist[5]
			filetype = '%s	%s	%s' %(rlist[0],rlist[2],rlist[1])
			warn_info = ()
			#根据文件来源(easyetl/eps/oracle/sql/job)处理文件
			if rlist[3] == r'eps': 
				print u'[INFO]:处理EPS报表文件	%s' %filetype
				src_base = ur'%s\ACRM\eps' %build_dir
				src = rlist[5]
				relpath = src.replace(src_base,'')	#获取相对路径
				dst_base = ur'\\192.168.55.51\eps_share\eps'
				#dst_base = ur'\\192.168.55.80\vss_tmp'	#test
				'''
				dst = ur'%s%s' %(dst_base,relpath)
				if not os.path.isdir(dst):
					os.makedirs(dst)
				print u'[INFO]:拷贝EPS报表文件 %s --> %s ' %(src,dst)
				eps_CopiedNum = pfile._copyFiles_(src,dst)
				print u'[INFO]:拷贝文件个数 %s' %eps_CopiedNum
				'''
				warn_info = u'eps: 请手动将目录%s 中的文件上传到服务器%s' %(src_base,dst_base)
			elif rlist[3] == r'easyetl':
				print u'[INFO]:处理EASYETL主机文件	%s' %filetype
				remotepath = r'/app11/easyetl'	#test /tmp/yhl
				localpath = ur'%s\ACRM\easyetl' %build_dir
				print u'[INFO]:上传EASYETL主机文件 "%s --> %s"' %(localpath,acrm_uat_host)
				ssh_htsc.upload_dir_win2unix_acrm(acrm_uat_host,remotepath,localpath)
			elif rlist[3] == r'sql':
				print u'[INFO]:处理SQL文件	%s' %filetype
				sql_info = u'%s,%s,%s' %(rlist[2],rlist[3],rlist[5])
				sql_list.append(sql_info)	#生成SQL信息数组
				#print sql_list
			elif u'oracle' in  rlist[3]:
				print u'[INFO]:处理ORACLE对象文件	%s' %filetype
				warn_info = u'oracle: 请手动在PL/SQL中登录数据库 %s 执行目录 %s 下的ORACLE对象文件' %(systype,dpath)
			elif rlist[3] == r'job':
				print u'[INFO]:处理JOB文件	%s' %filetype
				warn_info = u'job: 请手动在服务器 %s:/app11/easyetl 中导入JOB文件，执行命令: job_import %s.jobs %s' %(acrm_uat_host,nowdate,nowdate)
			elif rlist[3] == r'dmp':
				print u'[INFO]:处理dmp文件	%s' %filetype
				dmp_path = build_dir
				par_path = os.path.join(sys.path[0],'dmp')
				dodmp.dmp_exp(dmp_path, par_path)
				dodmp.epsdb_sel(par_path)
				dodmp.epsdb_del(par_path)	#test
				dodmp.dmp_imp(dmp_path, par_path)	#test
				warn_info = u'dmp: 请手动重启epsdb_lot2对应java前端'
			elif rlist[3] == r'java':
				print u'[INFO]:处理JAVA文件	%s' %filetype
				java_list = r'%s\%s_java.list' %(rlist[5],release)
				javawars = pfile.readtext(java_list)
				print javawars
				for war in javawars:
					warn_info = u'java: 请发布java前端包 %s' %war
			elif rlist[3] == r'readme':
				warn_info = u'readme: 请查看备注文件readme：%s' %dpath
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
				#systype = info_list[0]
				systype=info_list[0].replace('\\','_') if '\\' in info_list[0] else info_list[0]
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
					print u'[INFO]:上传GP SQL文件 "%s\%s --> %s"' %(localpath,dfile_name,acrm_uat_host)
					ssh_htsc.sftp_put_acrm(acrm_uat_host,remotepath,localpath,dfile_name)
					sql_warn = u'gp: 请手动执行服务器 %s 中GP SQL脚本，命令: gd -f %s/%s' %(acrm_uat_host,remotepath,dfile_name)
				else:
					sql_warn = u'oracle: 请手动在PL/SQL中登录数据库 %s 执行SQL脚本 %s\%s' %(systype,dpath,dfile_name)
				warn_list.append(sql_warn)
	except Exception as ex:
		print(u"[ERROR]:对象后续处理失败！%s" %line)
		print Exception,":",ex
		sys.exit()
	#返回
	return warn_list
			
#分情况单独处理 AAAAA
def sql_do(rows_list,types,dir_list,otype):
	1==1
		
def _main_(root_dir,release,build,MYSPACE):
	warnlist=list_do_obj(root_dir,release,build,MYSPACE)
	obj_do(root_dir,release,build)
	#print warnlist
	#警告信息输出
	pfile.warn_prompt(warnlist)
				
		
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
