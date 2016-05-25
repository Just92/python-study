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
	#���ô��ݲ���
	if len(sys.argv) !=4:
		print u"��ʽ��%s release build objtype" %(sys.argv[0])
		print u"Example: %s 8.3.1 build01 sql/oracle/job" %(sys.argv[0])
		sys.exit()
	else:
		print u'ִ������: %s' %(" ".join(sys.argv))
		release_value = sys.argv[1]
		build_value = sys.argv[2]
		objtype = sys.argv[3]		
		
	ini_file = os.path.join(sys.path[0],'ck.conf')
	pfile.alter_ini("vss_ck", "release", release_value,file=ini_file)
	pfile.alter_ini("release", "build", build_value,file=ini_file)
	#���ó�������
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
	ck_warn_value = u'����д build%s' %(int(filter(lambda x:x.isdigit(),build))+1)
	#print ck_warn_value
	_start_time_ = time.time()
	
	#��ʼ����
	print 'START...'
	print u'###############[STAGE 1]###############'
	print u'##########��VSS�л�ȡ����CK�ļ�########' 
	print u'[INFO]:��ȡ�ļ� %s/%s %s'%(vss_prj,ck_file,vss_ldir)
	#pvss.CheckOutFile(vss_prj,vss_ldir,ck_file)
	pvss.GetFile(vss_prj,vss_ldir,ck_file)
	print u'###############[STAGE 2]###############'
	print u'##########����CK�ļ�����list�ļ�#######'
	dock._main_(release,build,fname,sname,root_dir,ck_warn_value)
	print u'###############[STAGE 3]###############'
	print u'##########����list�ļ�#################'
	listwarns=dolist.list_do_obj(root_dir,release,build,SVN_MYSPACE)
	print u'###############[STAGE 4]###############'
	print u'####����list�ļ����ɵĶ���#############'
	objwarns=dolist.obj_do(root_dir,release,build)
	print u'###############[STAGE 5]###############'
	#print u'##########�ύ/�ع�checklist�ļ�#######'
	print u'##########��ʾ/������Ϣ���############'
	dock.read_release_content(ck_file,build,fname,sname=u'�汾����')
	#print build_contents
	vss_comment = release+'_'+build
	#pvss.undoCheckOutFile(vss_prj,vss_ldir,ck_file)
	#CheckInFile(vss_prj,work_dir,vss_file,vss_comment)
	#������Ϣ���
	print u'[WRAN]: ���ֶ��޸�checklist�ļ�"�汾��ʾ��Ϣ"Ϊ %s' %ck_warn_value
	pfile.print_warn(listwarns,objwarns)
	ctime = time.time() - _start_time_
	print(u'[INFO]:����acrm_checklist���к�ʱ:%0.2f'%(ctime))
	print 'END.'
	