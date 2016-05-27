# -*- coding: utf-8 -*- 
#根据checklist中的大版本、内部版本号、系统分类、对象类型、SVN路径、对象名称、SQL脚本
#读取excel指定内容生成1.list

import xlrd
import os
import shutil
import chardet
import sys
import re 
import commands
import time
import paramiko
#ssh
import datetime
import ConfigParser

reload(sys)
sys.setdefaultencoding('utf-8')



#通过用户名密码连接
def ssh_connect (host,port,user,password):
	ssh=paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host,port,user,password,timeout=30)
	return ssh
#通过密钥连接
def ssh_connect_key (host,port,user,key_file):
	ssh=paramiko.SSHClient()
	ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	key=paramiko.RSAKey.from_private_key_file(key_file)
	ssh.connect(host,port,user,pkey=key,timeout=30)
	return ssh

def ssh(hostname,port,username,password,command_list): 
	s=ssh_connect(hostname,port,username,password)
	#执行命令
	for cmd in command_list:
		print '>>%s' %cmd
		#time.sleep(1)
		stdin,stdout,stderr = s.exec_command(cmd)
		#stdin.write("Y")   #简单交互，输入 ‘Y’
		out = stdout.readlines()
		err = stderr.read()
		#print out
		#print any(err)
		#cmd_result = out if any(err) is False else '[ERROR]: %s' %err
		#print '>>%s' %cmd_result
		if  any(err):
			print '[ERROR]: %s' %err
		else:
			cmd_result = out
			for line in cmd_result:
				line_encode = chardet.detect(line).get('encoding')
				line = line.strip().decode('gbk','ignore') if line_encode == 'GB2312' else line.strip()
				print line
	s.close()
	
def sftp(hostname,port,username,password):
	t=paramiko.Transport((hostname,port))
	t.connect(username=username,password=password)
	sftp = paramiko.SFTPClient.from_transport(t)
	return sftp

def sftp_get(hostname,port,username,password,remotepath,localpath,file,targetfile=None):
	sf = sftp(hostname,port,username,password)
	rfile_path = '%s/%s' %(remotepath,file)
	lfile_path = os.path.join(localpath,file) if targetfile == None else os.path.join(localpath,targetfile)
	sf.get(rfile_path,lfile_path)
	print u'--Download file %s:%s to %s' %(hostname,rfile_path,lfile_path)
	sf.close()
	
def sftp_put(hostname,port,username,password,remotepath,localpath,file,targetfile=None):
	sf = sftp(hostname,port,username,password)
	rfile_path = '%s/%s' %(remotepath,file) if targetfile == None else os.path.join(remotepath,targetfile)
	lfile_path = os.path.join(localpath,file)
	sf.put(lfile_path,rfile_path)
	print u'--Upload file %s to %s' %(lfile_path,rfile_path)
	sf.close()
				
def upload_dir_win2unix(hostname,port,username,password,remote_dir,local_dir,exclude=(u'1.list')):
	sf = sftp(hostname,port,username,password)
	print u'[INFO]:upload file start %s ' % datetime.datetime.now()
	filesftpNum = 0
	for root,dirs,files in os.walk(local_dir):
		#print root,dirs,files
		for file in files:
			if file in exclude:
				continue
			local_file = os.path.join(root,file)
			a = local_file.replace(local_dir,'').replace('\\','/').rstrip('/')
			remote_file = u'%s%s' %(remote_dir,a)
			try:
				sf.put(local_file,remote_file)
			except Exception,e:
				sf.mkdir(os.path.split(remote_file)[0])	#返回一个路径的目录名和文件名
				sf.put(local_file,remote_file)
			print "--upload %s to remote %s" % (local_file,remote_file)
			filesftpNum += 1
		for name in dirs:
			local_path = os.path.join(root,name)
			a = local_path.replace(local_dir,'').replace('\\','/').rstrip('/')
			remote_path = u'%s%s' %(remote_dir,a)
			try:
				sf.mkdir(remote_path)
				print "--mkdir path %s" % remote_path
			except Exception,e:
				1==1
				#print "Path already exists %s" % remote_path
	sf.close()
	print u'[INFO]:Upload file success %s ' % datetime.datetime.now()
	print u'[INFO]:Upload the number of files %s' %filesftpNum
	
#暂未使用
def upload_file_win2unix(hostname,port,username,password,remote_dir,local_dir,ftp_file):
	sf = sftp(hostname,port,username,password)
	print u'[INFO]:upload file start %s ' % datetime.datetime.now()
	filesftpNum = 0
	
class htsc(object):	
	
	
	def __init__(self):
		self.name = u'htsc'
		self.ini_file = os.path.join(sys.path[0],'ck.conf')
		self.cf = ConfigParser.ConfigParser()
		self.cf.read(self.ini_file)
		
	def ssh_acrm(self,host,command_list):
		self.__init__()
		print self.ini_file
		if host==u'192.168.55.77':
			shostname = unicode(self.cf.get("ssh_acrm_uat", "hostname"))
			sport = int(self.cf.get("ssh_acrm_uat", "port"))
			susername = unicode(self.cf.get("ssh_acrm_uat", "username"))
			spassword = unicode(self.cf.get("ssh_acrm_uat", "password"))
		elif host==u'192.168.55.78':
			shostname = unicode(self.cf.get("ssh_acrm_dev", "hostname"))
			sport = int(self.cf.get("ssh_acrm_dev", "port"))
			susername = unicode(self.cf.get("ssh_acrm_dev", "username"))
			spassword = unicode(self.cf.get("ssh_acrm_dev", "password"))
		ssh(shostname,sport,susername,spassword,command_list)
		
	def sftp_get_acrm(self,host,remotepath,localpath,file,targetfile=None):
		self.__init__()
		if host==u'192.168.55.77':
			shostname = unicode(self.cf.get("ssh_acrm_uat", "hostname"))
			sport = int(self.cf.get("ssh_acrm_uat", "port"))
			susername = unicode(self.cf.get("ssh_acrm_uat", "username"))
			spassword = unicode(self.cf.get("ssh_acrm_uat", "password"))
		elif host==u'192.168.55.78':
			shostname = unicode(self.cf.get("ssh_acrm_dev", "hostname"))
			sport = int(self.cf.get("ssh_acrm_dev", "port"))
			susername = unicode(self.cf.get("ssh_acrm_dev", "username"))
			spassword = unicode(self.cf.get("ssh_acrm_dev", "password"))
		sftp_get(shostname,sport,susername,spassword,remotepath,localpath,file,targetfile=None)
		
	def sftp_put_acrm(self,host,remotepath,localpath,file,targetfile=None):
		self.__init__()
		if host==u'192.168.55.77':
			shostname = unicode(self.cf.get("ssh_acrm_uat", "hostname"))
			sport = int(self.cf.get("ssh_acrm_uat", "port"))
			susername = unicode(self.cf.get("ssh_acrm_uat", "username"))
			spassword = unicode(self.cf.get("ssh_acrm_uat", "password"))
		elif host==u'192.168.55.78':
			shostname = unicode(self.cf.get("ssh_acrm_dev", "hostname"))
			sport = int(self.cf.get("ssh_acrm_dev", "port"))
			susername = unicode(self.cf.get("ssh_acrm_dev", "username"))
			spassword = unicode(self.cf.get("ssh_acrm_dev", "password"))
		else:
			print u'[WARN]: %s Outside the scope of acrm' %host
			sys.exit()
		sftp_put(shostname,sport,susername,spassword,remotepath,localpath,file,targetfile=None)
	
	def upload_dir_win2unix_acrm(self,host,remote_dir,local_dir,exclude=(u'1.list')):
		self.__init__()
		if host==u'192.168.55.77':
			shostname = unicode(self.cf.get("ssh_acrm_uat", "hostname"))
			sport = int(self.cf.get("ssh_acrm_uat", "port"))
			susername = unicode(self.cf.get("ssh_acrm_uat", "username"))
			spassword = unicode(self.cf.get("ssh_acrm_uat", "password"))
		elif host==u'192.168.55.78':
			shostname = unicode(self.cf.get("ssh_acrm_dev", "hostname"))
			sport = int(self.cf.get("ssh_acrm_dev", "port"))
			susername = unicode(self.cf.get("ssh_acrm_dev", "username"))
			spassword = unicode(self.cf.get("ssh_acrm_dev", "password"))
		else:
			print u'[WARN]: %s 不在acrm的范围内' %host
			sys.exit()
		upload_dir_win2unix(shostname,sport,susername,spassword,remote_dir,local_dir,exclude)
		
	def upload_prod(self,host,remotepath,localpath,file,targetfile=None):
		self.__init__()
		if host==u'192.168.53.22':
			hostname = unicode(self.cf.get("sftp_prod", "hostname"))
			port = int(self.cf.get("sftp_prod", "port"))
			username = unicode(self.cf.get("sftp_prod", "username"))
			password = unicode(self.cf.get("sftp_prod", "password"))
			defaultremotepath = unicode(self.cf.get("sftp_prod", "remotepath"))
		else:
			print u'[WARN]: %s 不在prod ftp的范围内' %host
			sys.exit()	
		sf = sftp(hostname,port,username,password)
		rfile_path = '%s/%s' %(remotepath,file) if targetfile == None else os.path.join(remotepath,targetfile)
		lfile_path = os.path.join(localpath,file)
		#print sf.listdir(defaultremotepath)
		relativelypath = remotepath[len(defaultremotepath):] if defaultremotepath in remotepath else remotepath
		dstpath = defaultremotepath
		rellist =  relativelypath.split(r'/')
		for i in range(1,len(rellist)):
			#print rellist[i],sf.listdir(dstpath)
			if rellist[i] in sf.listdir(dstpath): 
				dstpath = r'%s/%s' %(dstpath,rellist[i])
				#print 1
			else:
				dstpath = r'%s/%s' %(dstpath,rellist[i])
				#print 2
				sf.mkdir(dstpath)
		sf.put(lfile_path,rfile_path)
		'''
		try:
			sf.put(local_file,remote_file)
		except Exception,e:
			
			if sdefaultremotepath in remotepath:
				relativelypath = remotepath[len(sdefaultremotepath):]
			sf.mkdir(os.path.split(remote_file)[0])	#返回一个路径的目录名和文件名
			sf.put(local_file,remote_file)
		sf.put(lfile_path,rfile_path)
		'''
		print u'--上传文件 %s 到 %s' %(lfile_path,rfile_path)
		sf.close()

		
#设置参数，并执行主程序
def main():
	#job_rdv_seq(tables)
	remotepath='/app11/easyetl'
	localpath=r'D:\SVN\tmp\py_CK'
	file = '20160324.jobs'
	sftp77_get(remotepath,localpath,file)
	#sftp.get(rfile,lfile)
	print u"[SUCCESS]:程序执行成功!"

if __name__=="__main__":
	main()
