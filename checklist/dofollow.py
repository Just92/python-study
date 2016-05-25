# -*- coding: utf-8 -*- 

import sys
import dock
import time
import pvss
import dolist
import psvn
import pfile
import dojob
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

def STAGE1(vss_prj,vss_ldir,ck_file):
	

if __name__=="__main__":
	#设置传递参数
	if len(sys.argv) !=4:
		print u"格式：%s release build objtype" %(sys.argv[0])
		print u"Example: %s 8.3.1 build01 sql/oracle/job" %(sys.argv[0])
		sys.exit()
	else:
		print u'执行命令: %s' %(" ".join(sys.argv))
		release_value = sys.argv[1]
		build_value = sys.argv[2]
		objtype = sys.argv[3]		
		
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
	root_dir = unicode(cf.get("public", "rootdir"))
	SVN_MYSPACE = unicode(cf.get("public", "svnmyspace"))
	ck_warn_value = u'请填写 build%s' %(int(filter(lambda x:x.isdigit(),build))+1)
	#print ck_warn_value
	_start_time_ = time.time()
	
	#开始程序
	print 'START...'
	print u'###############[STAGE 1]###############'
	print u'##########从VSS中获取锁定CK文件########' 
	print u'[INFO]:获取文件 %s/%s %s'%(vss_prj,ck_file,vss_ldir)
	#pvss.CheckOutFile(vss_prj,vss_ldir,ck_file)
	pvss.GetFile(vss_prj,vss_ldir,ck_file)
	print u'###############[STAGE 2]###############'
	print u'##########处理CK文件生成list文件#######'
	dock._main_(release,build,fname,sname,root_dir,ck_warn_value)
	print u'###############[STAGE 3]###############'
	print u'##########处理list文件#################'
	listwarns=dolist.list_do_obj(root_dir,release,build,SVN_MYSPACE)
	print u'###############[STAGE 4]###############'
	print u'####处理list文件生成的对象#############'
	objwarns=dolist.obj_do(root_dir,release,build)
	print u'###############[STAGE 5]###############'
	#print u'##########提交/回滚checklist文件#######'
	print u'##########提示/警告信息输出############'
	dock.read_release_content(ck_file,build,fname,sname=u'版本内容')
	#print build_contents
	vss_comment = release+'_'+build
	#pvss.undoCheckOutFile(vss_prj,vss_ldir,ck_file)
	#CheckInFile(vss_prj,work_dir,vss_file,vss_comment)
	#警告信息输出
	print u'[WRAN]: 请手动修改checklist文件"版本提示信息"为 %s' %ck_warn_value
	pfile.print_warn(listwarns,objwarns)
	ctime = time.time() - _start_time_
	print(u'[INFO]:发布acrm_checklist运行耗时:%0.2f'%(ctime))
	print 'END.'
	