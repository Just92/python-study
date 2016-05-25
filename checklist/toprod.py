# -*- coding: utf-8 -*- 

import sys,os,shutil
import dock
import time
import pfile,pvss,psvn,pssh
import dolist,dojob
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')


if __name__=="__main__":
#设置传递参数
	if len(sys.argv) !=5:
		print u"格式：%s sysname release sbuild ebuild" %(sys.argv[0])
		print u"Example: %s acrm/uac 8.3.1 build01 build05" %(sys.argv[0])
		sys.exit()
	else:
		print u'执行命令: %s' %(" ".join(sys.argv))
		sysname=sys.argv[1]
		release_value = sys.argv[2]
		#build_value = sys.argv[2] 
		sbuild= sys.argv[3]
		ebuild= sys.argv[4]
	ini_file = os.path.join(sys.path[0],'ck.conf')
	
	pfile.alter_ini("prod", "release", release_value,file=ini_file)
	pfile.alter_ini("prod", "sbuild", sbuild,file=ini_file)
	pfile.alter_ini("prod", "ebuild", ebuild,file=ini_file)
	
	#设置常量参数
	nowdate = time.strftime('%Y%m%d',time.localtime(time.time()))
	cf = ConfigParser.ConfigParser()
	cf.read(os.path.join(sys.path[0],ini_file))
	release = unicode(cf.get("prod", "release"))
	sbuild = unicode(cf.get("prod", "sbuild"))
	ebuild = unicode(cf.get("prod", "ebuild"))
	vss_prj = unicode(cf.get("vss_ck", "project"))
	vss_ldir = unicode(cf.get("vss_ck", "localdir"))
	ck_file = unicode(cf.get("vss_ck", "file"))
	fname = unicode(cf.get("vss_ck", "fpath"))
	sname = unicode(cf.get("vss_ck", "sname"))
	root_path = unicode(cf.get("public", "rootpath"))
	release_path = '%s\\%s' %(root_path,release)
	
	_start_time_ = time.time()
	acrm_uat_host = unicode(cf.get("ssh_acrm_uat", "hostname"))
	
	sftp_prod_hostname = unicode(cf.get("sftp_prod", "hostname"))
	sftp_prod_port = int(cf.get("sftp_prod", "port"))
	sftp_prod_username = unicode(cf.get("sftp_prod", "username"))
	sftp_prod_password = unicode(cf.get("sftp_prod", "password"))
	sftp_prod_defaultremotepath = unicode(cf.get("sftp_prod", "remotepath"))
	ck_workspace = unicode(cf.get("jenkins_ck", "workspace"))
	remotepath = r'%s/%s/%s/acrm' %(sftp_prod_defaultremotepath,release,nowdate)
	ssh_htsc=pssh.htsc()
	
	online = '%s_%s_%s' %(release.replace('.',''),sbuild.replace('build','b'),ebuild.replace('build','b'))
	online_dir = '%s_%s' %(sysname,online)
	online_zipfile = r'%s.zip' %online_dir
	pfile.alter_ini("prod", "online_zipfile",online_zipfile,file=ini_file)
	#int(filter(lambda x:x.isdigit(),build))+1
	
	print u'####################[STAGE 1]####################'
	print u'###############Merger Online Dir#################' 
	print u'[INFO]:Order cover to a directory %s: "%s~%s" --> %s'%(release_path,sbuild,ebuild,online_dir)
	start_value = int(filter(lambda x:x.isdigit(),sbuild))	#去字母
	end_value = int(filter(lambda x:x.isdigit(),ebuild))	#去字母
	range_values = pfile.range_seq(start_value,end_value)	#获取序列数组
	dstpath = ur'%s\%s'  %(release_path,online_dir)
	#print range_values
	srcpaths = []
	for i in range(0,len(range_values)):
		range_values[i] = 'build%02d' %range_values[i]
		srcpaths.append(r'%s\%s' %(release_path,range_values[i]))
	print range_values
	pfile.merge_dir(srcpaths,dstpath,exclude=(u'1.list'))
	print u'####################[STAGE 2]####################'
	print u'##########JOB Export releases builds#############' 
	# job /
	list_dir = dstpath
	tables = pfile.read_excel(fname,sname)
	build_list = pfile.filter_per_multi_result(tables,2,range_values)
	
        #dojob.job_list(build_list,list_dir)
        #print acrm_uat_host
        #dojob.job_do(list_dir,release,from_host = acrm_uat_host)	#test
	print u'####################[STAGE 3]####################'
	print u'##############On-line file packaging#############'
	zipfile = r'%s\%s' %(release_path,online_zipfile)
	pfile.zip_dir(dstpath,zipfile)
	print u'####################[STAGE 4]####################'
	print u'############On-line file upload FTP##############'
	'''
	pfile.create_dir(ck_workspace)
	src_path = os.path.join(release_path, online_zipfile)
	dst_path = os.path.join(ck_workspace, online_zipfile)
	onlinefile_path = os.path.join(ck_workspace, 'online.list')
	shutil.copyfile(src_path, dst_path)
	with open(onlinefile_path,'w+') as fo:
		fo.write(online_zipfile)
	'''
	print u'[INFO]:The on-line file: %s' %online_zipfile
	localpath = release_path	
	ssh_htsc.upload_prod(sftp_prod_hostname,remotepath,localpath,online_zipfile)
	ctime = time.time() - _start_time_
	print(u'[INFO]:Publish acrm_checklist run time:%0.2f'%(ctime))
	
