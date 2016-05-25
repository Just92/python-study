# -*- coding: utf-8 -*- 
#根据checklist中的大版本、内部版本号、系统分类、对象类型、SVN路径、对象名称、SQL脚本
#读取excel指定内容生成1.list

import sys
import os
#import chardet
import time
import pfile
import dojob

reload(sys)
sys.setdefaultencoding('utf-8')

#在对象子类型数组obj_dir中替选出满足子父类型(ftype)关系的windows目录结构化重组后字符串 wobj_dir
def vss_win_dir(obj_dir,ftype,number):
	try:
		#以分隔符'/'拆分字符串为数组
		sobj_dir = obj_dir[0].strip() #字符串首尾去空白符
		sobj_dir=sobj_dir.split('/') if ('/' in sobj_dir) else sobj_dir
		#print sobj_dir
		if ( u' ' in sobj_dir):
			#print u'[ERROE]对象子类型填写格式错误，中间有空格:%s' %obj_dir
			raise NameError(u'[ERROE] There is a space in serial number %s: %s' %(number,obj_dir))
		#获取子父类型(ftype)关系的数组sobj_dir
		for i in range(0,len(sobj_dir)):
			if sobj_dir[0] == ftype:
				break
			else:
				del sobj_dir[0]
		#del sub_obj[0] #去除父类型，暂保留
		sep =u'\\'
		wobj_dir = (sep.join(sobj_dir)).rstrip(sep)
		#objs_dir.append(sub_obj_dir) #二维数组拼接，暂无效
		return wobj_dir
	except Exception as ex:
		print(u"[ERROR]:对象子类型windows目录结构化失败!!!")
		print Exception,":",ex  
		#sys.exit()
	
#前端数据库导入
def dmp_do(dir_list,dir_name='dir.list'):
	#设置文件路径
	file_dir=dir_list
	file_list=file_dir+'\\'+sys.argv[1]+'_'+'dmp.list'
	print u'[INFO]:前端数据库导入信息 %s' %file_list
	#获取vss地址相关信息数组：本地路径(序号)，VSS/SVN/CK标识，文件个数，系统分类，对象分类，vss/SVN路径，本地路径
	dir_info = [dir_list,u'CK','1',u'ACRM',u'dmp',u'dmp',dir_list+'\n']	
	dir_path = r'%s\%s' %(dir_list,dir_name)
	pfile.write_list(dir_path,dir_info)
	
#备注文件
def remark_do(dir_list,dir_name='dir.list'):
	#设置文件路径
	file_dir=dir_list
	file_list=file_dir+'\\'+sys.argv[1]+'_'+'dmp.list'
	print u'[INFO]:获取备注文件 %s' %file_list
	#获取vss地址相关信息数组：本地路径(序号)，VSS/SVN/CK标识，文件个数，系统分类，对象分类，vss/SVN路径，本地路径
	dir_info = [dir_list,u'CK','1',u'ACRM',u'dmp',u'dmp',dir_list+'\n']	
	dir_path = r'%s\%s' %(dir_list,dir_name)
	pfile.write_list(dir_path,dir_info)

#前端java包发布，对象名称中获取java所属应用
def java_do(source_list,dir_list,dir_name='dir.list'):
	info_list = []
	#设置文件路径
	file_dir=dir_list
	file_list=file_dir+'\\'+sys.argv[1]+'_'+'java.list'
	print u'[INFO]:前端java包发布更新 %s' %file_list
	for row in source_list:
		number=str(int(row[0]))
		obj_name = row[7]
		#print obj_name
		#info = u'[WARN]前端java包发布，请发布前端包: '+obj_name
		#print info
		info_list.append(obj_name)
	java_list=list(set(info_list))	#去重
	java_list.sort()	#排序
	javas = (u','.join(java_list))
	file_vals = [u'最后一行-'+number,javas]	#获取写入文件内容数组
	pfile.create_dir(file_dir)
	pfile.write_list(file_list,file_vals)
	#获取vss地址相关信息数组：本地路径(序号)，VSS/SVN/CK标识，文件个数，系统分类，对象分类，vss/SVN路径，本地路径
	object_ncols=[0,7]
	file_vals=pfile.filter_cols_enter(source_list,object_ncols)	
	file_num = str(len(file_vals))	#获取文件个数
	dir_info = [dir_list,u'CK',file_num,source_list[0][1],u'java',u'java',dir_list+'\n']
	#print dir_info
	dir_path = r'%s\%s' %(dir_list,dir_name)
	pfile.write_list(dir_path,dir_info)
	#print info_list
	#ck_list(source_list,otype,file_list,dir_list)
	return javas

#SQl对象处理(元数据二维数组,类型数组,子类型识别符,文件根路径)
def sql_do(rows_list,types,dir_list,otype='sql',dir_file=None):
	if u'GP' in types[0] :
		file_dir=dir_list+'\\'+types[0]#+'\\'
	else:
		file_dir=dir_list+'\\'+types[0]+'\\oracle'#+otype
		
	dir_file = dir_file if dir_file else 'dir.list'
	
	systype=types[0].replace('\\','_') if '\\' in types[0] else types[0]
	
	if	types[1] == u'SQL脚本':
		print u'[INFO]:获取CK中的SQL脚本 %s' %systype
		file_path=ur'%s\%s_%s_%s.sql' %(file_dir,systype,sys.argv[1],sys.argv[2])
		#file_dir+'\\'+types[0]+'_'+sys.argv[1]+'_'+sys.argv[2]+'.'+otype
		pfile.rm_file(file_path)
		#print file_path
		ck_list(rows_list,otype,file_path,dir_list,file_dir,dir_name=dir_file)
	elif types[1] == u'SQL脚本文件':
		print u'[INFO]:写入SQL文件list'
		#file_dir=dir_list+'\\'+types[0]+'\\'+otype
		vss_list(rows_list,otype,file_dir,dir_list,dir_name=dir_file)
	else:
		print u'[INFO]:SQL对象类型不在范围之内'
		
def easyetl_do(rows_list,types,dir_list,otype='easyetl',dir_file=None):	
	dir_file = dir_file if dir_file else 'dir.list'
	#types[0] = u'ACRM'
	obj_svn_do(rows_list,types,otype,dir_list)
	

#SQl对象处理(元数据二维数组,类型数组,子类型识别符,文件根路径)
def readme_do(rows_list,types,dir_list,otype='readme',dir_file=None):
	file_dir=dir_list+'\\'+types[0]+'\\'+otype	
	dir_file = dir_file if dir_file else 'dir.list'
	if	types[1] == u'备注':
		print u'[INFO]:获取CK中的备注内容'
		file_path=file_dir+'\\'+types[0]+'_'+sys.argv[1]+'_'+sys.argv[2]+'.'+otype
		pfile.rm_file(file_path)
		#print file_path
		ck_list(rows_list,otype,file_path,dir_list,file_dir,dir_name=dir_file)
	#elif types[1] == u'备注文件':
	#	print u'[INFO]:写入备注文件list'
	#	#file_dir=dir_list+'\\'+types[0]+'\\'+otype
	#	vss_list(rows_list,otype,file_dir,dir_list,dir_name=dir_file)
	else:
		print u'[INFO]:readme对象类型不在范围之内'

#三级过滤：对象子类型处理(元数据二维数组,父类型,子类型识别符,文件根路径)
def sub_obj_do(rows_list,ftype,otype,dir_list):
	try:
		#获取类型筛选条件
		sobj_ncols = [6]	#类型子目录所在列号
		sub_objs = pfile.filter_cols_rdv(rows_list,sobj_ncols)	#获取去重后的子类型二维数组
		for obj_dir in sub_objs:
			srows_list = pfile.filter_result(rows_list,sobj_ncols,obj_dir)	#获取子类型分类的表格二维数组
			number = srows_list[0][0]
			wobj_dir = vss_win_dir(obj_dir,otype,number)	#子类型windows目录结构化
			file_dir=dir_list+'\\'+ftype+'\\'+wobj_dir
			vss_list(srows_list,otype,file_dir,dir_list)
	except Exception as ex:
		print(u"[ERROR]:对象子类型处理失败！对应序号: %s 子类型为: %s" %(number,obj_dir[0]))
		print Exception,":",ex 
		#sys.exit()

#写入ck相关信息到list文件 (源文件,对象分类,CK文件路径,DIR文件根路径,CK写入文件路径)
def ck_list(rows_list,otype,file_list,dir_list,file_dir,dir_name='dir.list'):
	try:
		number=str(int(rows_list[0][0])) if isinstance(rows_list[0][0],(int,float)) else 'Null'
		#print number
		object_ncols=[0,7]	#获取CK文件信息所在列
		file_vals=pfile.filter_cols_enter(rows_list,object_ncols)	##获取CK文件信息
		file_num = str(len(file_vals))	#SVN文件个数
		file_vals = pfile.dlist_form2_gbk(file_vals)
		pfile.create_dir(file_dir)	#若目录不存在则创建
		#print dir_name
		pfile.write_dlist(file_list,file_vals)	#写入list文件信息
		#获取vss地址相关信息数组：本地路径(序号)，VSS/SVN/CK标识，系统分类，对象分类，vss/SVN路径，本地路径
		dir_info = [file_dir,u'CK',file_num,rows_list[0][1],otype,rows_list[0][6],file_dir+'\n']	
		dir_path = r'%s\%s' %(dir_list,dir_name)
		pfile.write_list(dir_path,dir_info)
	except Exception as ex:
		print(u"[ERROR]:填写格式有误! 问题行位于序号: %s" %number)
		print Exception,":",ex 
		#sys.exit()
	
#写入VSS相关信息到list文件 (源文件,对象分类,VSS文件路径,DIR文件路径)
def vss_list(rows_list,otype,file_dir,dir_list,dir_name='dir.list'):
	#number=str(int(rows[0])) if isinstance(rows[0],(int)) else 'Null'
	file_list=file_dir+'\\'+'1.list'
	pfile.rm_file(file_list)
	object_ncols=[0,6,7] #获取VSS文件信息所在列
	file_vals=pfile.filter_cols_enter(rows_list,object_ncols)	##获取VSS文件信息
	pfile.create_dir(file_dir)	#若目录不存在则创建
	pfile.write_dlist(file_list,file_vals)	#写入list文件信息
	#获取vss地址相关信息数组：本地路径(序号)，VSS/SVN/CK标识，系统分类，对象分类，vss/SVN路径，本地路径
	file_num = str(len(file_vals))	#vss文件个数
	dir_info = [file_dir,u'VSS',file_num,rows_list[0][1],otype,rows_list[0][6],file_dir+'\n']	
	print dir_name
	dir_path = r'%s\%s' %(dir_list,dir_name)
	pfile.write_list(dir_path,dir_info)	#写入dir文件地址信息
	#return dir_info
	1==1
	
#写入SVN相关信息到list文件 (源文件,对象分类,VSS文件路径,DIR文件路径)
def svn_list(rows_list,otype,file_dir,dir_list,dir_name='dir.list'):
	#number=str(int(rows[0])) if isinstance(rows[0],(int)) else 'Null'
	file_list=file_dir+'\\'+'1.list'
	pfile.rm_file(file_list)
	object_ncols=[0,6]	#获取SVN文件信息所在列
	file_vals=pfile.filter_cols_enter(rows_list,object_ncols)	##获取SVN文件信息
	pfile.create_dir(file_dir)	#若目录不存在则创建
	#obj_url = [[number,rows_list[0][6]]]	#获取SVN地址信息二维数组
	#pfile.write_dlist(file_dir+'\\'+'svn.list',obj_url) #获取SVN地址写入文件
	pfile.write_dlist(file_list,file_vals)	#写入list文件信息
	#获取vss地址相关信息数组：本地路径(序号)，VSS/SVN/CK标识，系统分类，对象分类，vss/SVN路径，本地路径
	file_num = str(len(file_vals))	#SVN文件个数
	dir_info = [file_dir,u'SVN',file_num,rows_list[0][1],otype,u'SVN_URL',file_dir+'\n']	
	dir_path = r'%s\%s' %(dir_list,dir_name)
	pfile.write_list(dir_path,dir_info)
	
#VSS对象处理(元数据二维数组,类型数组,子类型识别符,文件根路径)		
def obj_vss_do(rows_list,types,otype,dir_list):
	try:
		number = rows_list[0][0] #获取当前对象类型首行序号
		#print number
		file_dir=dir_list+'\\'+types[0]+'\\'+otype
		vss_list(rows_list,otype,file_dir,dir_list)
	except Exception as ex:
		print(u"[ERROR]:对象处理失败！对应序号: %s 类型为: %s" %(number,rows_list[0][6]))
		print Exception,":",ex 
		#sys.exit()
	
#SVN对象处理(元数据二维数组,类型数组,子类型识别符,文件根路径)		
def obj_svn_do(rows_list,types,otype,dir_list):
	try:
		number = rows_list[0][0] #获取当前对象类型首行序号
		#print number
		file_dir=dir_list+'\\'+types[0]+'\\'+otype
		svn_list(rows_list,otype,file_dir,dir_list)
	except Exception as ex:
		print(u"[ERROR]:对象处理失败！对应序号: %s 类型为: %s" %(number,rows_list[0][6]))
		print Exception,":",ex 
		#sys.exit()

#VSS对象处理(元数据二维数组,类型数组,子类型识别符,文件根路径)		
def oracle_do(rows_list,types,otype,dir_list):
	try:
		number = rows_list[0][0] #获取当前对象类型首行序号
		#print number
		file_dir=dir_list+'\\'+types[0]+'\\'+otype
		svn_list(rows_list,otype,file_dir,dir_list)
		'''if rows_list[0][1] == 'ACRM':
			svn_list(rows_list,otype,file_dir,dir_list)
		else:
			vss_list(rows_list,otype,file_dir,dir_list)
			'''
	except Exception as ex:
		print(u"[ERROR]:对象处理失败！对应序号: %s 类型为: %s" %(number,rows_list[0][6]))
		print Exception,":",ex 
		#sys.exit()
		
#根据类型筛选后的二维数组集中的首行对象类型获取系统识别分类tname，及异常抛出问题对象
def query_object(source_list):
	#获取二维数组集中的首行
	nrow = source_list[0]
	#获取首行的对象类型并划分系统识别分类
	val = nrow[4]
	if val == u'SQL脚本' :
		tname = 'sql'
	elif val == u'SQL脚本文件' :
		tname = 'sql'
	elif val == u'ORACLE包文件' :
		tname = 'oracle\PACKAGE'
	elif val == u'ETL-JOB' :
		tname = 'job'
	elif val == u'ETL主机文件' :
		tname = 'easyetl'
	elif val == u'GP脚本文件' :
		tname = 'easyetl'
	elif val == u'报表文件' :
		tname = 'eps'
	elif val == u'报表配置文件' :
		tname = 'eps'
	elif val == u'JAVA包' :
		tname = 'java'
	elif val == u'导前端库' :
		tname = 'dmp'
	elif val == u'IFB文件' :
		tname = u'ifb'
	elif val == u'JAVA文件' :
                tname = u'ignore'
		1==1	#忽略
	elif val == u'备注' :
		tname = u'readme'
		1==1	#忽略
	else :
		print u"[ERROR]:CHECKLIST中对象类型匹配失败!!!"
		print u"--失败对象所在行序号:%s 所属系统:%s 对象类型:%s 修改人:%s" %(nrow[0],nrow[1],val,nrow[8])
		#sys.exit()
	return tname
	
#根据版本号，对象类型分类创建目录结构并处理文件
def create_dir_do(source_list,dir_list,build):
	#print u'######################'
	warn_info = []
	dirs_info = []
	dirs_dlist = []
	a_mark = 0
	#获取类型筛选条件
	type_ncols = [1,4] #类型所在列号
	try:	
		#零级筛选二维数组：内部版本号
		build_list = pfile.filter_result(source_list,[2],[build]) #build_ncols = [2]
		#获取对象类型二维数组
		type_lists = pfile.filter_cols_rdv(build_list,type_ncols)
		pfile.del_cre_dir(dir_list)	#目录清空并创建
		for types in type_lists:
			#获取类型筛选后的结果集
			rows_list = pfile.filter_result(build_list,type_ncols,types)
			#获取对象类型系统识别分类
			otype=query_object(rows_list)		
			#根据对象类型获取文件目录file_dir，文件名称file_list，文件内容file_vals
			if otype in (u'sql') :
				sql_do(rows_list,types,dir_list,otype)
			elif otype in (u'job') :
				1==1 #跳过
				a_mark = u'job'
			elif otype in (u'dmp') :
				dmp_do(dir_list)
			elif otype in (u'java') :
				javas=java_do(rows_list,dir_list)
				warn_info = [u'[WARN]前端java包发布，请发布前端包: %s' %javas]
			elif otype in (u'eps'):
				#sub_obj_do(rows_list,types[0],otype,dir_list)
				obj_svn_do(rows_list,types,otype,dir_list)
			elif otype in (u'easyetl'):
				easyetl_do(rows_list,types,dir_list,otype)
			elif (u'oracle') in otype:
				oracle_do(rows_list,types,otype,dir_list)
			elif otype in (u'readme') :
				readme_do(rows_list,types,dir_list,otype)
			elif otype in (u'ignore') :
				1==1
			else :
				obj_vss_do(rows_list,types,otype,dir_list)
				#print type(dirs_info)
			#dirs_dlist.append(dirs_info)
			#整合dir_info
		if a_mark == u'job':
			print u'[INFO]:写入JOB文件list'
			dojob.job_list(build_list,dir_list)
		'''
		print dirs_dlist
		dirs_dlist = pfile.dlist_rdv_rnull(dirs_dlist)
		print dirs_dlist
		pfile.write_dlist(dir_list+'\\'+'dir.list',pfile.dlist_rdv_rnull(dirs_dlist))
		'''
	except Exception as ex:
		print(u"[ERROR]:处理CK文件失败!!!")
		print Exception,":",ex  
		sys.exit()
	
	finally:
		#warn_info信息提醒
		if any(warn_info):
			#print 'warn_info is defined'
			for warn in warn_info:
				print warn
		else:
			1==1
			#print u'[INFO]不存在警告信息'	
			
#设置参数，并执行主程序
def _main_(release,build,fname,sname,root_dir,warn_value):
	#获取版本根目录
	list_dir = root_dir+'\\'+release+'\\'+build
	start = time.time()
	#读取checklist数据
	tables = pfile.read_excel(fname,sname)
	#print tables
	#创建目录并执行写入list
	print u"[INFO]:创建目录并执行写入list %s" %list_dir
	create_dir_do(tables,list_dir,build)
	#job_rdv_seq(tables) #获取job编号，暂无效
	#修改checklist首行，提示下次填写的版本号
	file_path = r'%s' %(fname)
	#print u'[INFO]:修改CK文件next build信息 "%s"' %(warn_value)
	#pfile.write_excel_value(file_path,warn_value)
	#print u"[SUCCESS]:checklist获取list成功!"
	c = time.time() - start
	print(u'[INFO]:处理checklist运行耗时:%0.2f'%(c))

def read_release_content(ck_file,build,fname,sname=u'版本内容'):
	contents_dlist = pfile.read_excel(fname,sname)
	build_dlist = pfile.filter_result(contents_dlist,[1],[build])
	#print contents_dlist
	#pfile.filter_cols_enter(build_list,[1,2,3,4,5])
	content = pfile.filter_str_enter(build_dlist,[1,2,3,4,5])
	print u'[INFO]: %s中%s已切换至UAT，版本内容如下：' %(ck_file,build)
	if len(content) ==0:
		print u'没有版本内容\n'
	else:
		print content
	#return content
	1==1

if __name__=="__main__":
	#设置传递参数
	print sys.argv
	print u"#命令执行示例：%s %s %s" %(sys.argv[0],sys.argv[1],sys.argv[2])
	release = sys.argv[1]
	build= sys.argv[2] #build= u'build01'
	#print u"脚本名:", sys.argv[0]
	#for i in range(1, len(sys.argv)):
	#	print u" 参数", i, sys.argv[i]
	#设置常量参数
	fname = "sql.xls"
	sname= u'代码类更新'
	root_dir = r'D:\SVN\tmp\DEV'
	warn_value = u'请填写 build02'
	_main_(release,build,fname,sname,root_dir,warn_value)
