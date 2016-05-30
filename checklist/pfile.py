# -*- coding: utf-8 -*- 
#根据checklist中的大版本、内部版本号、系统分类、对象类型、SVN路径、对象名称、SQL脚本
#读取excel指定内容生成1.list

import xlrd,xlwt
from xlutils.copy import copy
import sys,os,shutil
import chardet,codecs,stat
import re #正则表达式
#import commands
import time,datetime
import ConfigParser
import zipfile

reload(sys)
sys.setdefaultencoding('utf-8')

#w = Workbook()  
#ws = w.add_sheet('Sheet1') 

#读取eccel文件内容获取二维数组row_list
def read_excel(fname,sname,colnameindex=0):
	#print u'######################'
	if os.path.isfile(fname):
		print u"[INFO]:读取excel文件 name:%s sheet:%s" % (fname,sname)
		bk = xlrd.open_workbook(fname)	#打开excel
		#定位指定sheet页
		try:
			#print 1
			sh = bk.sheet_by_name(sname)
			#print "[INFO]:读取excel文件 name:%s sheet:%s" % (fname,sname)
			nrows = sh.nrows	#获取行数
			ncols = sh.ncols	#获取列数
			#print u" 行数 %d, 列数 %d" % (nrows,ncols)
			#colnames = sh.row_values(colnameindex) #某一行数据 
			#获取第一行第一列数据 
			cell_value = sh.cell_value(0,0)
			#print " %s" %cell_value
		except:
			print "[ERROR]:No sheet in %s named %s" % (fname,sname)
			sys.exit()
	else:
		print u'没有找到文件 %s' %fname
		sys.exit()
	
	#读取表格数据到二维数组
	try:
		#获取正文数据	
		row_list = []
		#range(起始行,结束行)
		for i in range(2,nrows):
			row = sh.row_values(i)
			#print row
			#print row
			#筛除数组row中的编码异常到rows ignore-忽略;replace-替换显示
			rows = []
			for j in row :
				if isinstance(j, basestring):
					str=unicode(j.encode('gbk','ignore'),'gbk')
				else:
					str=j
				rows.append(str)
			#追加数组元素rows到二维数组row_list
			row_list.append(rows)
		return row_list
	except:
		print "[ERROR]:填写格式有误 in %s named %s"  % (fname,sname) 
		sys.exit()
	finally:
		1==1
		#print u'[INFO]:读取文件结束'

#执行excel首行合并9列单元格，并写入提示信息
def write_excel_value(file_path,warn_value,isheet=0):
	#from xlutils.copy import copy    # http://pypi.python.org/pypi/xlutils
	#import xlwt
	# 设置cell的font
	font = xlwt.Font() # Create the Font
	font.name = u'宋体'
	font.bold = True
	font.colour_index = 2 # 0:black, 1: white, 2: red, 3:light green, 4:blue
	# 设置cell内部定位
	alignment = xlwt.Alignment() # Create Alignment
	alignment.horz = xlwt.Alignment.HORZ_CENTER # May be: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
	alignment.vert = xlwt.Alignment.VERT_CENTER # May be: VERT_TOP, VERT_CENTER, VERT_BOTTOM, 
	#定义一个类型
	style = xlwt.XFStyle() # Create the Style
	style.font = font # Apply the Font to the Style
	style.alignment = alignment # Add Alignment to Style
	nfile_path = '%s_tmp' %file_path
	rb = xlrd.open_workbook(file_path,formatting_info=True)	#formatting_info=True保存之前数据的格式
	#r_sheet = rb.sheet_by_index(isheet) #only read
	wb = copy(rb) #调用xlutils改为read+write
	#w_sheet = wb.get_sheet(isheet) #read+write
	#w_sheet.write_merge(0, 0, 0, 9,warn_value,style) # Merges row 0's columns 0 through 9.
	wb.save(nfile_path)
		
#读取文本文件内容并返回内容数组
def readtext(file):
	#file = file_dir+'\\'+file_name
	with open(file,'r') as f:
		lines = f.readlines()
	return lines

#在目标文件file_name中写入二维数组文件内容file_vals，首列为标记
def write_dlist(file_name,file_values):
	#print u'######################'
	#print file_list
	#读写模式打开文件并追加写入1.list
	try:
		fo = open(file_name,'a+')
		print u"[INFO]:写入list文件:%s" %file_name
		for rows in file_values:
			number = rows[0]
			del rows[0]	#删除序号值
			#以指定的字符(分隔符)连接字符串数组
			a = ' '
			fo.write(a.join(rows))
			print u"--成功写入: 序号%s" %number
		fo.close()
	#print u"[INFO]:关闭文件"
	except IOError :
		print("[ERROR]:fail to open file \"%s\" " %file_name)
		
#在目标文件file_name中写入数组文件内容file_vals，首列为标记
def write_list(file_name,file_value):
	#print u'######################'
	#print file_list
	#读写模式打开文件并追加写入1.list
	try:
		fo = open(file_name,'a+')
		#print u"[INFO]:写入list文件:%s" %file_name
		number = file_value[0]
		del file_value[0]
		#print file_value
		#以指定的字符(分隔符)连接字符串数组
		a = ','
		fo.write(a.join(file_value))
		#print u"--成功写入: 地址内容" 
		fo.close()
	#print u"[INFO]:关闭文件"
	except IOError :
		print("[ERROR]:fail to open file \"%s\" " %file_name)

#数组列筛选:系统类型，对象类型 (第num1-1,num2-1列)，首尾去空后去重
#源集二维数组中筛选指定列(数组)到目标列二维数组new_list，并去重
def filter_cols_rdv (source_list,col_nums):
	cols_list =[]
	for rows in source_list:
		#print row
		#tmp = [val for val in a if val in b] #交集
		col_rows=[]
		for i in col_nums:
			#字符串首尾去空白符
			col_rows.append(rows[i].strip())
		cols_list.append(col_rows)	
	#去重
	#flist=rows(set(cols_list))
	new_list = []
	for rows in cols_list:
		if rows not in new_list:
			new_list.append(rows)
	#news_ids.sort(stype_list.index) #排序
	return new_list
	
#从源集二维数组中根据指定列号筛选，获取结果集二维数组result_list
#source_list二维数组源集,col_nums选择列数组,Filters筛选条件数组
def filter_result(source_list,colnum_list,filters_list):
	result_list = []
	for nrow in source_list:
		#根据列号获取某行中列所在值，并与筛选条件比较
		cols_row=[]
		for i in colnum_list:
			cols_row.append(nrow[i])
		if cols_row == filters_list:
			result_list.append(nrow)
		else:
			1==1
	return result_list
	
#source_list二维数组源集,col_nums选择列数,Filters筛选条件元组Tuple,获取结果集二维数组result_list
def filter_per_multi_result(source_list,colnum,filters_tuple):
	result_list = []
	for nrow in source_list:
		#print nrow
		#print colnum
		#print nrow[colnum]
		#根据列号获取某行中列所在值，并与筛选条件比较
		if nrow[colnum] in filters_tuple:
			result_list.append(nrow)
		else:
			1==1
	return result_list

#从源集二维数组中根据指定列号筛选，获取目标列二维数组col_result_list，并加回车符
def filter_cols_enter(source_list,col_nums):
	col_result_list = []
	for nrow in source_list :
		#根据列号获取某行中列所在值
		cols_row=[]
		for i in col_nums:
			cols_row.append(nrow[i])
		#该行最后一个元素后加回车符
		cols_row[-1] = cols_row[-1]+'\n'
		col_result_list.append(cols_row)
	return col_result_list
	
#从源集二维数组中根据指定列号筛选，加回车符，获取字符串result，
def filter_str_enter(source_dlist,col_nums =[]):
	#print source_dlist
	nsource_list = []
	for rows_list in source_dlist:
		nrows_list =[]
		col_nums = range(0,len(rows_list)) if len(col_nums) == 0 else col_nums
		for i in col_nums:
			row = rows_list[i]
			nrow = str(int(row)) if isinstance(row,(int,float)) else row
			nrows_list.append(nrow)
		nrows = "	".join(nrows_list)+'\n'
		#该行最后一个元素后加回车符
		nsource_list.append(nrows)
	#print nsource_list
	result = "".join(nsource_list)
	#print result
	return result
		
#创建目录，若已存在则清空再创建
def del_cre_dir(file_dir):
	#print file_dir
	if os.path.exists(file_dir):  #判断目录是否存在
		rm_dir_tree(file_dir)	
		os.rmdir(file_dir)	#若目录已存在则清空目录
		#raise IOError
	os.makedirs(file_dir)   #创建多级目录	
		
#创建目录，若不存在则创建
def create_dir(file_dir):
	if not os.path.exists(file_dir):  #判断目录是否存在
		os.makedirs(file_dir)   #创建多级目录
	#else:
	#	print(u"[INFO]:目录%s已创建！" %file_dir)
	1==1

def rm_dir_tree(dir_path):
	for root, dirs, files in os.walk(dir_path,topdown=False):
		#print root, dirs, files
		for name in files:
			rm_file(os.path.join(root, name))
		for name in dirs:
			os.rmdir(os.path.join(root, name))
	
def rm_file(file_path):
	if os.path.exists(file_path):
		#print u'[INFO]:清除文件%s' %file_path
		os.chmod(file_path,stat.S_IWRITE)
		os.remove(file_path)
		
#删除满足目录下满足格式的文件
def rm_format_file(dir_path,format):
	files = os.listdir(dir_path)
	for file in files:
		file_extension = os.path.splitext(file)[1]
		file_path=os.path.join(dir_path,file)
		if file_extension == format:
			rm_file(file_path)
			print u'--清除文件%s' %file_path

		
#判断元素是否定义，暂无效
def isset(v): 
   try : 
     type (eval(v)) 
   except : 
     return  0 
   else : 
     return  1 
	 
#通过第二个参数选择处理方式，暂无效
def argv2_opt_doing(argv2):
	# 将正则表达式编译成Pattern对象，注意hello前面的r的意思是“原生字符串” 
	pattern = re.compile(r'build',re.I)

#二维数组去重并去空值
def dlist_rdv_rnull(dlist):
	tmp_dlist = []
	for list in dlist:
		if (list not in tmp_dlist) and any(list):
			tmp_dlist.append(list)
	return tmp_dlist

#windows 命令默认只识别编码格式gbk，需格式转换
def dlist_form2_gbk(file_vals):
	file_vals2 =[]
	for rows in file_vals:
		rows2 = []
		for row in rows:
			row=str(int(row)) if isinstance(row,(int,float)) else row
			rows2.append(row.encode('gbk','ignore'))
		file_vals2.append(rows2)
	return file_vals2

#读取list数组，警告/提示信息输出
def warn_prompt(warnlist):
	if any(warnlist):
		warnlist.sort(reverse = True)	#排序
		for warnvalue in warnlist:
			if warnvalue == None:
				continue
			print u'--%s' %warnvalue
	
#输入起始值和结束值，输出起始到结束的范围值list
def range_seq(start_value,end_value):
	start_int = start_value if isinstance(start_value,(int,float)) else int(start_value)
	'''
	if isinstance(start_value,(int,float)):
		start_int = start_value
	else :
		start_int = int(start_value)
	'''
	end_int = end_value if isinstance(end_value,(int,float)) else int(end_value)
	range_list=[]
	#print start_int,end_int,end_value
	for i in range(start_int,end_int+1):
		range_list.append(i)
		#print i
	return range_list
	
#拷贝目录下文件，按条件排除
def _copyFiles_(src,dst,exclude=(u'1.list')):
	srcFiles = os.listdir(src)
	#print srcFiles
	#dstFiles = dict(map(lambda x:[x, ''], os.listdir(dst)))	#字典
	filesCopiedNum = 0
	dirsCopiedNum =0
	#print dstFiles
	#print u'[INFO]:拷贝文件 %s --> %s ' %(src,dst)
    # 对源文件夹中的每个文件若不存在于目的文件夹则复制
	for file in srcFiles:
		#print file
		if file in exclude:
			continue
		src_path = os.path.join(src, file)
		dst_path = os.path.join(dst, file)
        # 若源路径为文件夹，若存在于目标文件夹，则递归调用本函数；否则先创建再递归。
		if not os.path.isdir(dst):
			os.makedirs(dst)
		if os.path.isdir(src_path):
			if not os.path.isdir(dst_path):
				os.makedirs(dst_path)
			dirsCopiedNum += _copyFiles_(src_path,dst_path)
        # 若源路径为文件，则复制，不重复则放入版本控制中，否则无操作。
		elif os.path.isfile(src_path):                
			shutil.copyfile(src_path, dst_path)
			filesCopiedNum += 1
			#print u'--拷贝文件 %s' %dst_path
			#if not dstFiles.has_key(file):
				#print u'--拷贝文件 %s' %dst_path
				#_add_(dst_path)
	#print u'[INFO]:拷贝文件个数 %s' %filesCopiedNum
	return filesCopiedNum

#列出目录dpath下后缀为fsuffix(.py)的文件,迭代读取内容写入 dstfile(result.txt)
def merge_dir(srcpaths,dstpath,exclude=(u'1.list')):
	try:
		#print(ur'[INFO]: 合并开始...')
		del_cre_dir(dstpath)
		for srcpath in srcpaths:
			print(ur'[INFO]: 合并目录 %s --> %s '%(srcpath,dstpath))
			_copyFiles_(srcpath,dstpath,exclude)
		#print (ur'[INFO]: 合并结束.')
	except Exception as ex:
		print u'[ERROR]:合并目录出错 %s-->%s' %(srcpath,dstpath)
		print Exception,":",ex 
		sys.exit()
		
def alter_list(list,alter_value):
	for row in list:
		1==1
	
#dpath = ur'D:\上线\DEV\8.3.1\build06\ACRM\oracle'
#fsuffix = '.sql'
#dstfile = "result.txt"	
#列出目录dpath下后缀为fsuffix(.py)的文件,迭代读取内容写入 dstfile(result.txt)
def merge_dir_file(dpath,fsuffix,dstfile,exclude=(u'1.list')):
	flist=[r for r in os.listdir(dpath) if os.path.splitext(r)[-1]==fsuffix]
	#dstfilepath = os.path.join(dpath,dstfile)
	print u'[INFO]:合并文件到 %s' %dstfile
	with open(dstfile,"a+") as save:
		for file in flist:
			print file
			if file in exclude:
				continue
			txthead = ('--%s\n' %file).encode('gbk','ignore')	
			txtpart = '\n'
			try:
				fpath = os.path.join(dpath,file)
				txtcontent=open(fpath).read()
				print txtcontent
				if any(txtcontent):
					save.write(txthead)	#写入文件名注释
					save.write(txtcontent)	#写入文件内容
					save.write(txtpart)	#写入分隔行
					rm_file(fpath)	#删除已合并文件
					#os.remove(fpath)	#删除已合并文件
				else:
					print u'[INFO]:文件内容为空 %s' %fpath
			except Exception as ex:
				print u'[ERROR]:合并文件出错 %s-->%s' %(fpath,dstfile)
				print Exception,":",ex 
				sys.exit()

#读取目录dpath下rfile文件中的第二列数据为文件名,迭代将内容写入 dstfile(result.txt)
def merge_file(dpath,rfile,dstfile,tmpfile='c:\\tmpfile'):
	#flist=[r for r in os.listdir(dpath) if os.path.splitext(r)[-1]==fsuffix]
	#dstfilepath = os.path.join(dpath,dstfile)
	rfile_path = os.path.join(dpath,rfile)
	#UTF8_2_GBK(rfile_path,tmpfile)
	lines = readtext(rfile_path)
	#print lines
	flist = []
	for line in lines:
		line = line.split(' ')
		flist.append(line[1].strip())
	#print flist
	print u'[INFO]:合并文件到 %s' %dstfile
	with open(dstfile,"a+") as save:
		filenum = 1
		for file in flist:
			print u'--合并文件%s: %s' %(filenum,file)
			try:
				txthead = ('--%s\n' %file).encode('gbk','ignore')	
				txtpart = '\n'
				fpath = os.path.join(dpath,file)
				file_2_GBK(fpath,tmpfile)
				txtcontent=open(tmpfile,'r').read()
				#print txtcontent
				if any(txtcontent):
					save.write(txtpart)	#写入分隔行
				save.write(txthead)	#写入文件名注释
				save.write(txtcontent)	#写入文件内容
				save.write(txtpart)	#写入分隔行
				rm_file(fpath)	#删除已合并文件
				#os.remove(fpath)	#删除已合并文件
				filenum += 1
			except Exception as ex:
				print u'[ERROR]:合并文件出错 %s-->%s' %(fpath,dstfile)
				print Exception,":",ex 
				sys.exit()
	
#修改配置文件信息	
def alter_ini(section,option,value,file='ck.ini'):
	cf = ConfigParser.ConfigParser()
	cf.read(file)
	cf.set(section,option,value) 
	f = open(file,'w+')
	cf.write(f)
	f.close()
	
def print_warn(*warns_arg):
	if len(warns_arg) != 0:
		print u'[WARN]:!!!!!!!!!!!!!!!!!!!!!!!!!'
		print u'[WARN]:存在告警/提示信息!!!'
		for warns in warns_arg:
			if warns is not None:
				warn_prompt(warns)
			else:
				print 'None!'
	else:
		print u'[INFO]:不存在告警/提示信息.'
		
def zip_dir(dirname,zipfilename):
	"""
	| ##@函数目的: 压缩指定目录为zip文件
	| ##@参数说明：dirname为指定的目录，zipfilename为压缩后的zip文件路径
	| ##@返回值：无
	| ##@函数逻辑：
	"""
	filelist = []
	dirname = os.path.abspath(dirname)  
	zipfilename = os.path.abspath(zipfilename)  
	if not os.path.exists(dirname):  
		print "[ERROR]: Dir/File %s is not exist." % dirname
		sys.exit()
	print ur'[INFO]:压缩%s 到 %s' %(dirname,zipfilename)
	if os.path.isfile(dirname):
		filelist.append(dirname)
	else :
		for root, dirs, files in os.walk(dirname):
			for name in files:
				filelist.append(os.path.join(root, name))
	zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
	for eachfile in filelist:
		arcname = eachfile[len(dirname):]
		#print arcname
		zf.write(eachfile,arcname)
	zf.close()
	print "[INFO]: Zip folder succeed!"  
	
def unzip_file(zipfilename, unzipdirname):
	"""
	| ##@函数目的: 解压zip文件到指定目录
	| ##@参数说明：zipfilename为zip文件路径，unziptodir为解压文件后的文件目录
	| ##@返回值：无
	| ##@函数逻辑：
	"""
	zipfilename = os.path.abspath(zipfilename)  
	#abspath 返回规范化的绝对路径。   
	unzipdirname = os.path.abspath(unzipdirname)  
	print "[INFO]: Start to unzip file %s to folder %s ..." %(zipfilename, unzipdirname)  
	if not os.path.exists(zipfilename):  
		print "[ERROR]: Dir/File %s is not exist" %zipfilename
		sys.exit()
	if not os.path.exists(unzipdirname):
		os.mkdir(unzipdirname)
	else:
		if os.path.isfile(unzipdirname):
			print "[INFO]: %s is file and exist." % unzipdirname  
	srcZip = zipfile.ZipFile(zipfilename)
	starttime = time.time()
	for eachfile in srcZip.namelist():
		print "Unzip file %s ..." % eachfile 
		eachfilename = os.path.normpath(os.path.join(unzipdirname, eachfile)) 
		eachdirname = os.path.dirname(eachfilename)
		if not os.path.exists(eachdirname):  
			os.makedirs(eachdirname)
		#fd=open(eachfilename, 'wb')
		#fd.write(srcZip.read(eachfile))
		#fd.close()
		srcZip.extract(eachfile,unzipdirname)
		#print eachfile
		dt = datetime.datetime.fromtimestamp(os.path.getmtime(eachfile))
		#print dt
		ConverTime2 = time.mktime(dt.timetuple())
		os.utime(eachfilename, (ConverTime2,ConverTime2))
	#srcZip.extractall(unzipdirname)	#解压缩
	srcZip.close()
	endtime = time.time()
	times = endtime - starttime
	print "[INFO]: Unzip file succeed! Spend time %fs" %times
	
def ReadFile(filePath):
	buf = open(filePath, "rb").read()
	result = chardet.detect(buf)
	encoding = result["encoding"]
	#print encoding
	with codecs.open(filePath,"r",encoding) as f:
		data = str(f.read())
		if data[:3] == codecs.BOM_UTF8:
			data = data[3:]
		return data.decode("utf-8")
 
def WriteFile(filePath,u,encoding="gbk"):
    with codecs.open(filePath,"w",encoding) as f:
        f.write(u)
 
def file_2_GBK(src,dst):
    content = ReadFile(src)
    WriteFile(dst,content,encoding="gb18030")
	