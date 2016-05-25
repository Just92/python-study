# -*- coding: utf-8 -*- 

import sys,os,time
import dock,dolist,dojob,docheck
import pvss,psvn,pfile
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')
#在sys加载后,setdefaultencoding方法被删除了,所以我们要通过重新导入sys来设置系统编码

if __name__=="__main__":#判断是否是直接运行该python
	#设置传递参数
	if len(sys.argv) !=3:
		print u"格式：%s release build" %(sys.argv[0])
		print u"Example: %s 8.3.1 build01" %(sys.argv[0])
		sys.exit()
	else:
		print u'执行命令: %s' %(" ".join(sys.argv))
		release_value = sys.argv[1]
		build_value = sys.argv[2] 
		
	ini_file = os.path.join(sys.path[0],'ck.conf')
	pfile.alter_ini("vss_ck", "release", release_value,file=ini_file)
	pfile.alter_ini("release", "build", build_value,file=ini_file)
	#设置常量参数
	cf = ConfigParser.ConfigParser()
	cf.read(ini_file)
	release = unicode(cf.get("vss_ck", "release"))
	build = unicode(cf.get("release", "build"))
	vss_prj = unicode(cf.get("vss_ck", "project"))
	vss_ldir = unicode(cf.get("vss_ck", "localdir"))
	ck_file = unicode(cf.get("vss_ck", "file"))
	fname = unicode(cf.get("vss_ck", "fpath"))
	sname = unicode(cf.get("vss_ck", "sname"))
	root_path = unicode(cf.get("public", "rootpath"))
	SVN_MYSPACE = unicode(cf.get("public", "svnmyspace"))
	ck_warn_value = u'请填写 build%02d' %(int(filter(lambda x:x.isdigit(),build))+1)
	#print ck_warn_value
	_start_time_ = time.time()
	
	#开始程序
	print 'START...'
	print u'####################[STAGE 1]####################'
	print u'###############Get CK-file from VSS##############' 
	print u'[INFO]:获取文件 %s/%s %s'%(vss_prj,ck_file,vss_ldir)
	#pvss.CheckOutFile(vss_prj,vss_ldir,ck_file)
	pvss.GetFile(vss_prj,vss_ldir,ck_file)
	print u'####################[STAGE 2]####################'
	print u'####Processing CK-file generated list-file#######'
	dock._main_(release,build,fname,sname,root_path,ck_warn_value)
	print u'####################[STAGE 3]####################'
	print u'###########Checking list-file####################'
	docheck.list_check(root_path,release,build,SVN_MYSPACE)
	print u'####################[STAGE 4]####################'
	print u'##########Processing list-file###################'
	listwarns=dolist.list_do_obj(root_path,release,build,SVN_MYSPACE)
	print u'####################[STAGE 5]####################'
	print u'#####Object processing list-files generated######'
	objwarns=dolist.obj_do(root_path,release,build)
	print u'####################[STAGE 6]####################'
	print u'##########Prompt/Warn message output#############'
	dock.read_release_content(ck_file,build,fname,sname=u'版本内容')
	#print build_contents
	vss_comment = release+'_'+build
	#pvss.undoCheckOutFile(vss_prj,vss_ldir,ck_file)
	#CheckInFile(vss_prj,work_dir,vss_file,vss_comment)
	#警告信息输出
	print u'[WRAN]: Please manually modify the checklist File "version information" as %s' %ck_warn_value
	pfile.print_warn(listwarns,objwarns)
	_end_time_ =time.time()
	ctime = _end_time_ - _start_time_
	print(u'[INFO]:Publish acrm_checklist run time:%0.2f'%(ctime))
	print 'END.'
	
