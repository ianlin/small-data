#-*- coding: utf-8 -*-
from urllib import urlretrieve
import urllib2
from datetime import datetime, timedelta
import sys,os,time
import zipfile

class AutoDownload:
	def __init__(self):
		#=======================================================NEED TO EDIT START
		#SET what object you want to download
		self.target_list = ['TaiFex']
		#Skip Holiday
		self.ignore_holiday = True
		#In order to avoid lock IP
		self.need_sleep = False
		self.sleep_time = 2
		#===========Path for SUCKS!! M$=============
		self.path_char = '\\'
		self.store_dir = 'C:\\Documents and Settings\\Administrator\\орн▒\\AutoDownload'
		#===========Path for Unix like===========
		#self.path_char = '/'
		#self.store_dir = '~/AutoDownload'
	
		#=======================================================NEED TO EDIT END

		#Check if DIR exist or make it
		self.chkDIR(self.store_dir)
		
		self.log_file = self.path_char.join([ self.store_dir,'log.txt' ])
		self.fp = file(self.log_file,"a")
		self.logMSG(self.fp,"\n\n" + 'Initial...')
		#Load Data Setup
		self.setTargetRule()
	def chkDIR(self,path):
		if not os.path.isdir(path):
			os.mkdir(path)
	def setTargetRule(self):
		self.setup = {'TaiFex' : {'Tick' : dict()}}
		#If You want to add other information see the follow:
		'''
		EXAMPLE1:
		self.setup['TaiFex']['OneMinK']['DO'] = True
		self.setup['TaiFex']['OneMinK']['url'] = 'http://www.froy.com.tw/DailyDownload'
		...etc

		EXAMPLE2: HeySong Stock ID:1234
		self.setup['TWSE']['1234']['DO'] = True
		self.setup['TWSE']['1234']['url'] = 'http://www.froy.com.tw/DailyDownload'
		...etc
		'''
		#TaiFex Tick File		
		self.setup['TaiFex']['Tick']['DO'] = True
		self.setup['TaiFex']['Tick']['url'] = 'http://www.taifex.com.tw/DailyDownload'
		self.setup['TaiFex']['Tick']['avail_days'] = 60
		self.setup['TaiFex']['Tick']['min_file_size'] = 1024 #Measure with KB
		self.setup['TaiFex']['Tick']['download_file_ext'] = 'zip'
		self.setup['TaiFex']['Tick']['need_unzip'] = True
		self.setup['TaiFex']['Tick']['need_convert'] = True
		self.setup['TaiFex']['Tick']['real_file_ext'] = 'rpt'
		self.setup['TaiFex']['Tick']['convert_to'] = 'csv'
	def chkLocalFile(self, filename, limit_size=None):
		if not os.path.exists(filename):
			return False , '%s -> File not exist' % (filename)
		if limit_size and os.path.getsize(filename) < limit_size:
			return False, '%s -> File size is too short: %d < %d ' % (filename,os.path.getsize(filename),limit_size )
		return True, ''
	def chkRemoteFile(self, remotefile, limit_size=None):
		resp = urllib2.urlopen(remotefile)
		if resp.code != 200:
			return False, '%s -> Http return %s Code' % (remotefile, resp.code)
		if limit_size:
			length = resp.headers.get('Content-Length',None)
			length = int(length)
			if length and length < limit_size:
				return False, '%s -> Remote file is too short: %d < %d ' % (remotefile,length,limit_size)
		return True, ''
	def logMSG(self,fp,text):
		cur_local_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
		row = cur_local_stamp + ': ' + text + "\n"
		fp.write(row)
	def MainLoop(self):
		for target_main in self.target_list:
			for target_sub in self.setup[target_main]:
				if self.setup[target_main][target_sub].get('DO',None):
					self.logMSG(self.fp,'[Starting] %s -> %s ...' % ( target_main,target_sub ))
					self.chkDIR(self.path_char.join([ self.store_dir,target_main]))
					self.chkDIR(self.path_char.join([ self.store_dir,target_main,target_sub]))
					self.EachLoop(target_main,target_sub)
	def EachLoop(self,target_main,target_sub):
		#If target_main='TaiFex' and target_sub='Tick' #Maybe use different function for each loop...
		today = datetime.today()
		#Define local file orig store path
		store_path_orig = self.path_char.join([ self.store_dir, target_main, target_sub, 'orig' ])
		#Check if DIR exist or make it
		self.chkDIR(store_path_orig)
		#If check file limit size
		chkMinSize = self.setup[target_main][target_sub].get('min_file_size',None)
		#Check IF need Unzip
		need_unzip = self.setup[target_main][target_sub].get('need_unzip',None)
		if need_unzip:
			unzip_dir = self.path_char.join([ self.store_dir, target_main, target_sub, self.setup[target_main][target_sub].get('real_file_ext','unzip') ])
			#Check if UNZIP DIR exist or make it
			self.chkDIR(unzip_dir)
		#Check IF need Convert
		need_convert = self.setup[target_main][target_sub].get('need_convert',None)
		if need_convert:
			convert_to_dir = self.path_char.join([ self.store_dir, target_main, target_sub, self.setup[target_main][target_sub].get('convert_to','convert_to') ])
			#Check if UNZIP DIR exist or make it
			self.chkDIR(convert_to_dir)
		for days in range(0,self.setup[target_main][target_sub].get('avail_days',32)):
			obj_day = today - timedelta(days)
			#Sat and Sun are no data
			if(self.ignore_holiday and obj_day.weekday()>=5):
				continue
			#Maybe custom by each target
			date_str = obj_day.strftime('%Y_%m_%d')
			#filename init
			o_filename = 'Daily_'+ date_str
			#filename
			filename = o_filename + '.' + self.setup[target_main][target_sub].get('download_file_ext','')
			#define remote url link
			remote_file = '/'.join([ self.setup[target_main][target_sub].get('url',''), filename ])
			local_file = self.path_char.join([ store_path_orig, filename ])
			sta = True
			errmsg = ''
			sta, errmsg = self.chkLocalFile(local_file, chkMinSize)
			if not sta:
				self.logMSG(self.fp,'[Current File START] -----> %s -----> [START]' % ( filename ))
				#Mark it if no need to debug
				self.logMSG(self.fp,errmsg)
				errmsg=''
				sta, errmsg = self.chkRemoteFile(remote_file, chkMinSize)
				if sta:
					sta = self.getFile(remote_file, local_file, chkMinSize)
					if sta and need_unzip:
						unzip_filename = o_filename + '.' + self.setup[target_main][target_sub].get('real_file_ext','')
						unzip_file_path = self.path_char.join([ unzip_dir, unzip_filename ])
						sta, errmsg = self.chkLocalFile(unzip_file_path, chkMinSize)
						if not sta:
							#file not unzip, do unzip
							self.logMSG(self.fp, 'Unzip From %s To %s' % (filename,unzip_filename) )
							sta = self.unzip_file(local_file,unzip_dir)
						else:
							#File already unzip, sta till true, so still need to check to convert or not
							pass
					if sta and need_convert:
						#Not Have done yet = =
						#chk_convert_filename = o_filename + '.' + self.setup[target_main][target_sub].get('convert_to','')
						pass
					if self.need_sleep:
						time.sleep(self.sleep_time)
				else:
					self.logMSG(self.fp,errmsg)
				self.logMSG(self.fp,'[Current File END] -----> %s -----> [END]' % ( filename ))
			else:
				continue
	def getFile(self,remote_file,local_file,chkMinSize):
		try:
			print remote_file
			urlretrieve(remote_file,local_file,chkSize)
			#urlretrieve(remote_file,local_file)
			sta, errmsg = self.chkLocalFile(local_file, chkMinSize)
			if not sta:
				self.logMSG(self.fp,errmsg)
				return False
			else:
				self.logMSG(self.fp,'%s -> Done!!' % (local_file))
				return True
		except IOError as IOE :
			self.logMSG(self.fp,'%s -> I/O ERROR' % ( local_file ))
			return False
	def unzip_file(self,from_file,to_dir):
		global zipfile
		try:
			f_zip = zipfile.ZipFile(from_file, 'r')
			#isBadZip = f_zip.testzip()
			#f_zip.extractall(output_dir)
			for f in f_zip.namelist():
				try:
					f_zip.extract(f, to_dir)
					self.logMSG(self.fp,'%s -> Unzip OK!!' % ( f ))
				except:
					self.logMSG(self.fp,'%s -> Unzip Fail!!' % ( f ))
					return False
			self.logMSG(self.fp,'Unzip ALL DONE!!')
			return True
		except zipfile.LargeZipFile:
			self.logMSG(self.fp,'%s -> Unzip Fail by [Large Zip File] ' % ( f ))
			return False
		except zipfile.BadZipfile:
			self.logMSG(self.fp,'%s -> Unzip Fail by [Bad Zip File] ' % ( f ))
			return False
		except:
			self.logMSG(self.fp,'%s -> Unzip Fail by [Unknow Error] ' % ( f ))
			return False
def chkSize(block_recieved,block_size_each,total_size):
	#for urlretrieve() third arg: hook function 
	#The third argument, if present, is a hook function that will be called once on establishment of the network connection and once after each block read thereafter.
	#The hook will be passed three arguments; 
	#1. count of blocks transferred so far
	#2. block size in bytes
	#3. total size of the file. may be -1 on older FTP servers which do not return a file size in response to a retrieval request.
	if total_size > 0:
		now_size = block_recieved * block_size_each 
		#if(now_size < total_size):
		if(now_size==0):
			print '%d/%d ...downloading...' % (now_size, total_size)
		elif(now_size >= total_size):
			print '%d/%d ...Done!!!' % (total_size, total_size)
		else:
			pass

if __name__ == '__main__':
	prog = AutoDownload()
	prog.MainLoop()
	raw_input("Please <Enter> for closing this window.")
