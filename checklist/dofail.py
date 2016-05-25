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
����dir.list�ļ����ݽ��д���
oracle sql job
'''
#�Ի�ȡ�Ķ�����д���			
def oracle_do(root_dir,release,build):
	nowdate = time.strftime('%Y%m%d',time.localtime(time.time()))
	build_dir = root_dir+'\\'+release+'\\'+build
	dfile = build_dir+'\\'+r'dir.list'
	#��ȡVSS·����ִ��
	lines = pfile.readtext(dfile)
	lines.sort(reverse = True)	#����
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
			gline = unicode(line.encode('gbk','ignore'),'gbk').strip()	#ɸѡ�쳣���벢��βȥ��
			rlist = gline.split(',')	#�Էָ���','����ַ���Ϊ����
			systype = rlist[2]
			dpath = rlist[5]
			warn_info = ()
			#�����ļ���Դ(easyetl/eps/oracle/sql/job)�����ļ�
			if rlist[3] == r'eps': 
				print u'[INFO]:����EPS�����ļ�' 
				src_base = ur'%s\ACRM\eps' %build_dir
				src = rlist[5]
				relpath = src.replace(src_base,'')	#��ȡ���·��
				#dst_base = ur'\\192.168.55.51\eps_share\eps'
				dst_base = ur'\\192.168.55.80\vss_tmp'	#test
				dst = ur'%s%s' %(dst_base,relpath)
				if not os.path.isdir(dst):
					os.makedirs(dst)
				print u'[INFO]:����EPS�����ļ� "%s"' %src
				pfile._copyFiles_(src,dst)
			elif rlist[3] == r'easyetl':
				print u'[INFO]:����EASYETL�����ļ�' 
				remotepath = r'/app11/easyetl/tmp/yhl'	#test /tmp/yhl
				localpath = ur'%s\ACRM\easyetl' %build_dir
				print u'[INFO]:�ϴ�EASYETL�����ļ� "%s --> %s"' %(localpath,acrm_hostname)
				pssh.upload_dir_win2unix(acrm_hostname,acrm_port,acrm_username,acrm_password,remotepath,localpath)
			elif rlist[3] == r'sql':
				print u'[INFO]:����SQL�ļ�' 
				sql_info = u'%s,%s,%s' %(rlist[2],rlist[3],rlist[5])
				sql_list.append(sql_info)	#����SQL��Ϣ����
				#print sql_list
			elif u'oracle' in  rlist[3]:
				print u'[INFO]:����ORACLE�����ļ�' 
				warn_info = u'oracle: ���ֶ���PL/SQL�е�¼���ݿ� %s ִ��Ŀ¼ %s �µ�ORACLE�����ļ�' %(systype,dpath)
			elif rlist[3] == r'job':
				print u'[INFO]:����JOB�ļ�' 
				warn_info = u'job: ���ֶ��ڷ����� %s:/app11/easyetl �е���JOB�ļ���ִ������: job_import %s.job' %(acrm_hostname,nowdate)
			elif rlist[3] == r'dmp':
				print u'[INFO]:����dmp�ļ�' 
				dmp_path = build_dir
				dodmp.dmp_exp(dmp_path, par_path= ur'.\dmp')
				dodmp.epsdb_sel(par_path = ur'.\dmp')
				#dodmp.epsdb_del(par_path = ur'.\dmp')	#test
				#dodmp.dmp_imp(dmp_path, par_path= ur'.\dmp')	#test
				warn_info = u'dmp: ���ֶ�����epsdb_lot2��Ӧjavaǰ��'
			elif rlist[3] == r'java':
				print u'[INFO]:����JAVA�ļ�' 
				java_list = r'%s\%s_java.list' %(rlist[5],release)
				javawars = pfile.readtext(java_list)
				print javawars
				for war in javawars:
					warn_info = u'java: �뷢��javaǰ�˰� %s' %war
			#��ʾ��Ϣ����
			if any(warn_info):
				warn_list.append(warn_info) 
	except Exception as ex:
		print(u"[ERROR]:������ʧ�ܣ�%s" %line)
		print Exception,":",ex
	#ִ�к�������
	try:
		if sql_list is not None:	#������SQL�ű�
			sql_list = list(set(sql_list))	#ȥ��
			#print sql_list
			for sql_info in sql_list:
				info_list = sql_info.split(',')
				systype = info_list[0]
				dpath = info_list[2]
				dfile_name = u'%s_%s_%s.sql' %(systype,release,build)
				dstfile = ur'%s\%s' %(dpath,dfile_name)
				rfile = u'1.list'
				if os.path.exists(os.path.join(dpath,rfile)):
					print u'[INFO]:�ϲ�SQL�ļ�'
					pfile.merge_file(dpath,rfile,dstfile)
				#��ϵͳ���ʹ���SQL
				if systype == u'GP':
					1==1
					remotepath = r'/app11/easyetl/tmp'
					localpath = dpath
					print u'[INFO]:�ϴ�GP SQL�ļ� "%s\%s --> %s"' %(localpath,dfile_name,acrm_hostname)
					pssh.sftp_put(acrm_hostname,acrm_port,acrm_username,acrm_password,remotepath,localpath,dfile_name)
					sql_warn = u'gp: ���ֶ�ִ�з����� %s:%s ��GP SQL�ű�������: gd -f %s' %(acrm_hostname,remotepath,dfile_name)
				else:
					sql_warn = u'oracle: ���ֶ���PL/SQL�е�¼���ݿ� %s ִ��SQL�ű� %s\%s' %(systype,dpath,dfile_name)
				warn_list.append(sql_warn)
	except Exception as ex:
		print(u"[ERROR]:�����������ʧ�ܣ�%s" %line)
		print Exception,":",ex
	#����
	return warn_list
			

def _main_(root_dir,release,build,MYSPACE):
	warnlist=list_do_obj(root_dir,release,build,MYSPACE)
	obj_do(root_dir,release,build)
	#print warnlist
	#������Ϣ���
	pfile.warn_prompt(warnlist)
				
		
if __name__=="__main__":
	#���ô��ݲ���
	print sys.argv
	if sys.argv[1] is None:
		print u"[WARN]:����ִ��ʾ����%s %s %s" %(sys.argv[0],sys.argv[1],sys.argv[2])
	release = sys.argv[1]
	build= sys.argv[2] #build= u'build01'
	root_dir = ur'D:\����\DEV'
	MYSPACE = r'a.backend'
	start = time.time()		
	#_main_(root_dir,release,build)
	obj_do(root_dir,release,build)
	c = time.time() - start
	print(u'[INFO]:�������к�ʱ:%0.2f'%(c))