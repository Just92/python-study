# -*- coding: utf-8 -*- 
#根据checklist中的大版本、内部版本号、系统分类、对象类型、SVN路径、对象名称、SQL脚本
#读取excel指定内容生成1.list

import sys
import os
#import chardet
import time
import pfile
import pssh
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

ini_file = os.path.join(sys.path[0],'ck.conf')
cf = ConfigParser.ConfigParser()
cf.read(ini_file)
acrm_hostname = unicode(cf.get("ssh_acrm_uat", "hostname"))
ssh_htsc=pssh.htsc()

#source_list中的job列表 CK	
def job_list(source_list,file_path):
	#设置文件路径
	build = sys.argv[2]
	#build = int(filter(lambda x:x.isdigit(),build))
	file_list=r'%s\%s_job.list' %(file_path,sys.argv[1])
	
	try:
		#过滤结果集 job所有去重并排序job_rdv_seq
		jobs_Dlist = pfile.filter_result(source_list,[4],[u'ETL-JOB'])
		jobs_list =[]
		if any(jobs_Dlist):
			print u'[INFO]:写入list文件 %s' %file_list
			for rows in jobs_Dlist:
				number=str(int(rows[0])) if isinstance(rows[0],(int)) else 'Null'
				jobs = rows[7]
				jobs = int(jobs) if isinstance(jobs,(float)) else jobs
				jobs =str(jobs).strip()
				if u'\n' in jobs:	#一个元素存在多行记录
					#jobs.replace()
					jobs = jobs.split('\n')
					jobs_list.extend(jobs)
				else:
					jobs_list.append(jobs)
			jobs_list=list(set(jobs_list))	#去重
			jobs_list.sort()	#排序
			jobs = (u','.join(jobs_list))
			file_vals = [u'最后一行-'+number,jobs]	#获取写入文件内容二维表
			pfile.create_dir(file_path)
			pfile.write_list(file_list,file_vals)
			#获取vss地址相关信息数组：本地路径(序号)，VSS/SVN/CK标识，系统分类，对象分类，vss/SVN路径，本地路径
			file_num = str(len(file_vals))	#获取文件个数
			dir_info = [file_path,u'CK',file_num,u'ALL',u'job',file_list,file_path+'\n']	
			pfile.write_list(file_path+'\\'+'dir.list',dir_info)
			return file_vals
		else:
			print u'[INFO]:本版本没有JOB'
	except Exception as ex:
		print(u"[ERROR]:JOB填写格式有误! 问题行位于序号: %s " %number)
		print Exception,":",ex 
		sys.exit()
		
#根据版本号，对象类型分类创建目录结构并处理文件
def job_do(job_path,release,build = None,from_host=u'192.168.55.78',to_host = None):
	#设置参数
	nowdate = time.strftime('%Y%m%d',time.localtime(time.time()))
	job_file = '%s.jobs' %nowdate
	#job2_file = '%s_%s' %(build,job_file)
	#job_file = r'D:\SVN\tmp\DEV\8.1.1\build00\8.1.1_job.list'
	job_list = r'%s\%s_job.list' %(job_path,release)
	remotepath = r'/app11/easyetl'
	localpath = job_path
	print u'[INFO]:服务器%s导出job文件至UAT,并下载到本地 %s' %(from_host,job_file)
	if os.path.exists(job_list):
		#获取job编号
		job_id = pfile.readtext(job_list)[0]
		#定义远程脚本
		job_export = 'job_export.sh %s' %job_id
		export_cmd = ['pwd','. ~/.bash_profile;%s' %job_export]
		job_import = 'job_import %s' %job_file
		import_cmd = ['ls -l %s' %job_file,'. ~/.bash_profile;%s %s' %(job_import,nowdate)]
		#DEV导出
		ssh_htsc.ssh_acrm(from_host,export_cmd)
		#拷贝到目标服务器
		if to_host:
			scp_cmd = ['pwd','scp %s %s:%s/' %(job_file,to_host,remotepath)]
			ssh_htsc.ssh_acrm(from_host,scp_cmd)
		#UAT导入
		#ssh_htsc.ssh_acrm(u'192.168.55.77',import_cmd)
		#ssh_htsc.ssh78(command_list)
		#下载job文件到本地版本目录中
		if build:
			job2_file = '%s_%s' %(build,job_file)
			ssh_htsc.sftp_get_acrm(from_host,remotepath,localpath,job_file,job2_file)
		else:
			ssh_htsc.sftp_get_acrm(from_host,remotepath,localpath,job_file)
	else:
		1==1
		
def _main_(root_dir,release,build,fname,sname):		
	#获取版本根目录
	list_dir = root_dir+'\\'+release+'\\'+build
	start = time.time()
	#读取checklist数据
	tables = pfile.read_excel(fname,sname)
	source_list = tables
	#job_do(tables,list_dir,range=(u'all'))
	job_list(source_list,list_dir)