# -*- coding: utf-8 -*- 
#根据checklist中的大版本、内部版本号、系统分类、对象类型、SVN路径、对象名称、SQL脚本
'''
popen的参数，第一个为字符串（或者也可以为多个非命名的参数），表示你要执行的命令和命令的参数；后面的均为命名参数；
shell=True,表示你前面的传入的命令将在shell下执行，如果你的命令是个可执行文件或bat，不需要指定此参数；
stdout=subprocess.PIPE用来将新进程的输出重定向，
stderr=subprocess.STDOUT将新进程的错误输出重定向到stdout，
stdin=subprocess.PIPE用来将新进程的输入重定向；
universal_newlines=True表示以text的方式打开stdout和stderr。
'''

import sys
import subprocess
import os
#import unicodedata
import chardet
import shutil
import time
import pfile
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')

#设置VSS默认访问方式
vss_arvg = r'-server 192.168.55.61 -port 8877 -username huzhonghai -pwd 7216797 -alias htsc_vss'
vss_tmpdir = r'-tempdir c:\\temp'
'''
SVN_BASE_URL = r'https://192.168.55.120/svn/crm_code'
SVN_TRUNK_URL = r'%s/trunk' %SVN_BASE_URL
SVN_BRANCHES_DEV_URL = r'%s/branches/dev' %SVN_BASE_URL
SVN_USERNAME = u'yuanhuangliang'
SVN_PASSWORD = u'yuanhuangliang'
BASE_WORKSPACE = r'D:\a.golive_src_code'
'''
ini_file = os.path.join(sys.path[0],'ck.conf')
cf = ConfigParser.ConfigParser()
cf.read(ini_file)
SVN_BASE_URL = unicode(cf.get("svn", "SVN_BASE_URL"))
SVN_TRUNK_URL = unicode(cf.get("svn", "SVN_TRUNK_URL"))
SVN_BRANCHES_DEV_URL = unicode(cf.get("svn", "SVN_BRANCHES_DEV_URL"))
SVN_USERNAME = unicode(cf.get("svn", "SVN_USERNAME"))
SVN_PASSWORD = unicode(cf.get("svn", "SVN_PASSWORD"))
BASE_WORKSPACE = unicode(cf.get("svn", "BASE_WORKSPACE"))

	
def __excmd__(vcmd):
	vcmd = vcmd.encode('gbk','ignore')	#windows 命令默认只识别编码格式gbk，需格式转换
	#print vcmd
	#print type(vcmd)
	#print chardet.detect(vcmd)
	#os.system(vcmd)
	child=subprocess.Popen(vcmd,shell = True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	#print child
	#child.wait()
	com = child.communicate()
	return com[0].strip()
	#print child.stdout
	#print child.stderr
	#print child.returncode
	
def _export_(svn_url,work_path):
	#svn_url = r'%s/%s' %(SVN_BASE_URL,relative_path)
	svncmd = r'svn export %s %s --force'%(svn_url,work_path)
	#print svncmd
	stdout = __excmd__(svncmd)
	if stdout.find(r'svn: ') != -1:
		#print stdout
		return stdout

def _list_(svn_url):
	#svn_url = r'%s/%s' %(SVN_BASE_URL,relative_path)
	svncmd = r'svn list %s'%(svn_url)
	#print svncmd
	stdout = __excmd__(svncmd)
	if stdout.find(r'svn: ') != -1:
		#print stdout
		return stdout
	
def _checkout_(svn_url,WORKSPACE):
	svncmd = r'svn checkout %s %s --username %s --password %s'%(svn_url,WORKSPACE,SVN_USERNAME,SVN_PASSWORD)
	print svncmd
	print __excmd__(svncmd)
	
def _update_(WORKSPACE):
	svncmd = r'svn update %s '%(WORKSPACE)
	#print svncmd
	print __excmd__(svncmd)
	
def _merge_(svn_url,WORKSPACE):
	svncmd = r'svn merge %s %s '%(svn_url,WORKSPACE)
	print svncmd
	print __excmd__(svncmd)
	
def _commit_(m_log,WORKSPACE):
	svncmd = r'svn commit -m "%s" %s '%(m_log,WORKSPACE)
	print svncmd
	stdout =  __excmd__(svncmd)
	print stdout
	#if stdout.find(r'svn: ') != -1:
	#	print stdout
	
def _add_(WORKSPACE):
	#增加
	svncmd = r'svn add %s --force'%(WORKSPACE)
	print svncmd
	print __excmd__(svncmd)
	
def _revert_(WORKSPACE):
	#还原
	svncmd = r'svn revert %s -R'%(WORKSPACE)
	#print svncmd
	stdout =  __excmd__(svncmd)
	if stdout.find(r'svn: ') != -1:
		print stdout
	
def _lastrev_(svn_url):
	svncmd = r'svn info %s|sed -n -e "s#Last Changed Rev: ##p"' %svn_url
	last_rev = __excmd__(svncmd)
	return last_rev
	
def check_exist(relative_path):
	relative_path=relative_path.replace('\\','/').strip('/')
	svn_url = r'%s/%s' %(SVN_BASE_URL,relative_path)
	stdout = _list_(svn_url)
	if stdout != None:
		#print stdout
		print u'[WARN]:This is invalid file %s' %svn_url
	return stdout
	
def export_dev_file(relative_path,base_path):
	relative_path=relative_path.replace('\\','/').strip('/')
	base_path=base_path.replace('/','\\')
	svn_url = r'%s/%s' %(SVN_BASE_URL,relative_path)
	path_list = relative_path.split('/')
	for i in range(0,len(path_list)):
		if path_list[0] == u'a.backend':
			break
		else:
			del path_list[0]
	del path_list[0]	#去除u'a.backend'
	#base_list = path_list[0:2]
	#print type(list)
	fname = path_list.pop() if path_list[-1].find(r'.') != -1 else ''
	sep ='\\'
	base_list = path_list
	rpath = (sep.join(base_list)).strip(sep)
	work_dir = (sep.join(path_list)).strip(sep)
	'''
	声明：s为字符串，rm为要删除的字符序列
	s.strip(rm)		删除s字符串中开头、结尾处，位于 rm删除序列的字符
	s.lstrip(rm)	删除s字符串中开头处，位于 rm删除序列的字符
	s.rstrip(rm)	删除s字符串中结尾处，位于 rm删除序列的字符
	'''
	work_path = '%s\\%s\\' %(base_path,work_dir)
	fpath = os.path.join(work_path,fname)
	#print work_path
	#print base_path
	if not os.path.exists(work_path):
		#print u'[INFO]:目录不存在 %s' %work_path
		os.makedirs(work_path) 
	if os.path.isfile(fpath):
		#print u'[INFO]:删除已存在文件 %s' %fpath
		os.remove(fpath)
	#导出文件到本地目录
	stdout = _export_(svn_url,work_path)
	if stdout != None:
		#print stdout
		print u'[WARN]:Unable to export invalid file %s' %svn_url
	else:
		print u'--Export to file %s' %fpath
	return rpath,stdout


				
def src2uat_file(MYSPACE,work_path,src_base_path,m_info):
	print u'[INFO]:SVN file export&Merger -dev2uat'
	WORKSPACE = r'%s\%s' %(BASE_WORKSPACE,MYSPACE)
	src = '%s\%s' %(src_base_path,work_path)
	dst = '%s\%s' %(WORKSPACE,work_path)
	uat_url = r'%s/trunk/%s' %(SVN_BASE_URL,MYSPACE)
	#work_path = export_dev_file(relative_path,base_path)
	#print dst
	if not os.path.exists(WORKSPACE):
		print u'--Get Workspace %s %s' %(WORKSPACE,uat_url)
		_checkout_(uat_url,WORKSPACE)
	print u'--Update Workspace %s' %WORKSPACE
	_update_(WORKSPACE)	#获取工作空间最新内容
	print u'--Restore Workspace %s' %WORKSPACE
	_revert_(WORKSPACE)
	print u'--Copying File %s --> %s' %(src,dst)
	copynum = pfile._copyFiles_(src,dst)	#拷贝文件build2uat
	print u'[INFO]:Copy to %s , Number of files %s' %(dst,copynum)
	m_log = r'Merged %s from CK about %s' %(m_info,work_path)
	print u'--Submit workspace %s' %WORKSPACE
	_add_(WORKSPACE)
	_commit_(m_log,WORKSPACE)
	return copynum
	
	
def dev2uat_dir(MYSPACE,m_info):
	WORKSPACE = r'%s\%s' %(BASE_WORKSPACE,MYSPACE)
	dev_url = r'%s/branches/dev/%s' %(SVN_BASE_URL,MYSPACE)
	uat_url = r'%s/trunk/%s' %(SVN_BASE_URL,MYSPACE)
	_update_(WORKSPACE)	#获取工作空间最新内容
	shutil.copy("oldfile","newfile") 
	print u'[INFO]:开始SVN Merge分支合并'
	merge(dev_url,WORKSPACE)
	last_rev = _lastrev_(dev_url)
	m_log = r'Merged %s from %s@%s' %(m_info,dev_url,last_rev)
	print u'[INFO]:提交SVN合并内容到服务器，备注："%s"' %m_log
	_commit_(m_log,WORKSPACE)
	print (u'[INFO]:已合并开发到UAT')
	

