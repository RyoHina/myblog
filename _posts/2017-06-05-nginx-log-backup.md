---
layout: post
title: "nginx服务器在生产环境中日志切割与备份"
categories: nginx 
tags: ubuntu nginx
---

* content
{:toc}


nginx在生产环境如果项目访问量很大，日志文件通常会增长的比较大，这时候就需要定时切割日志文件，否则会影响到nginx性能。
#### 定时执行任务 ####
假如每天凌晨4点备份nginx日志，然后重启nginx服务器。 linux下定时任务通常都是使用crontab -e命令。在Ubuntu系统下默认是nano编辑器，可以使用以下命令切换编辑器：
	
	# 切换为vi编辑器
	export EDITOR=vi 
	# 或者
	export VISUAL=vi

<!--more-->

然后用crontab -e 添加命令

	00 04 * * * /bin/bash /home/auto_backup_nginx_log.sh


crontab 文件中每个条目中各个域的意义和格式：

第一列 分钟： 1——59

第二列 小时： 1——23(0表示子夜)

第三列 日 ： 1——31

第四列 月 ： 1——12

第五列 星期： 星期0——6(0表示星期天，1表示星期一、以此类推)

第六列 要运行的命令

#### 编写脚本定时备份 ####
sh脚本内容

	python auto_backup_nginx_log.py


py脚本内容

	# coding=utf-8
	# qiniu upload file helper
	import os
	import datetime
	import pytz
	from qiniu import Auth, put_data, put_file

	access_key = '***'
	secret_key = '***'

	def backup_nginx_log():
		# 0. remove old zip file if exist
		backup_file_zip = 'nginx_backup.zip'
		if os.path.exists(backup_file_zip):
			os.remove(backup_file_zip)

		# 1. zip log files
		os.system('zip -r %s nginx_access.log nginx_error.log' % backup_file_zip)

		# 2. remove old log and restart nginx
		if os.path.exists('nginx_access.log'):
			os.remove('nginx_access.log')
		if os.path.exists('nginx_error.log'):
			os.remove('nginx_error.log')
		os.system('service nginx restart')

		# 3. upload zip file
		utc_time = datetime.datetime.utcnow()
		tz = pytz.timezone('Asia/Shanghai')
		# replace method
		utc_time = utc_time.replace(tzinfo=pytz.UTC)
		result_time = utc_time.astimezone(tz)
		result_str = result_time.strftime('%Y-%m-%d %H-%M-%S')

		file_name = 'nginx-backup-' + result_str + '.zip'
		q = Auth(access_key, secret_key)
		token = q.upload_token('你的存储空间名字', file_name, 3600)
		ret, info = put_file(token, file_name, backup_file_zip)
		print('qiniuhelper.py qiniu_backup_mysql ret:' + str(ret))
		print('qiniuhelper.py qiniu_backup_mysql info:' + str(info))

	backup_nginx_log()

这样我们就可以完成定时日志备份了.
