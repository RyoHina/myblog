---
layout: post
title: "如何在Web Server中使用七牛云存储资源？"
categories: qiniu 
tags: qiniu
---

* content
{:toc}


#### 1. 免费申请七牛云帐号 ####
注册帐号后，打开[https://portal.qiniu.com/create](https://portal.qiniu.com/create)，找到‘对象存储’官方资源，添加，新建存储空间
<!--more-->

#### 2. 如何上传资源？ ####
以python为例，上传资源代码如下：

	from qiniu import Auth, put_data, put_file

	# 个人中心->密钥管理找到 access_key 和 secret_key
	access_key = '***' 
	secret_key = '***'
	
	def qiniu_upload_image(file_data):
	    file_name = '取一个名字.png';
	    q = Auth(access_key, secret_key)
	    token = q.upload_token('这里是新建的存储空间的名字', file_name, 3600)
	    ret, info = put_data(token, file_name, file_data)
	    print('qiniuhelper.py qiniu_upload_image ret:' + str(ret))
	    print('qiniuhelper.py qiniu_upload_image info:' + str(info))
	    return '测试域名/' + file_name


这样就可以通过 '测试域名/取一个名字.png' 访问这个资源了。 然后数据库中直接存储这个地址，不需要以文件形式存储图片或者把图片资源存放到数据库。
#### 3. 定时备份数据库 ####
	import datetime
	import pytz
	
	def qiniu_backup_mysql():
	    # 1. dump mysql database
	    backup_file = 'backup.sql'
	    backup_file_zip = 'backup.sql.zip'
	    if os.path.exists(backup_file):
	        os.remove(backup_file)
	    if os.path.exists(backup_file_zip):
	        os.remove(backup_file_zip)
	    os.system('mysqldump -h%s -u%s -p%s %s &gt; %s' % (DATABASE_HOST,
	                                                    DATABASE_USERNAME,
	                                                    DATABASE_PASSWORD,
	                                                    DATABASE,
	                                                    backup_file))
	
	    # 2. zip file
	    os.system('zip -r %s %s' % (backup_file_zip, backup_file))
	
	    # 3. upload zip file
	    utc_time = datetime.datetime.utcnow()
	    tz = pytz.timezone('Asia/Shanghai')
	    # replace method
	    utc_time = utc_time.replace(tzinfo=pytz.UTC)
	    result_time = utc_time.astimezone(tz)
	    result_str = result_time.strftime('%Y-%m-%d %H-%M-%S')
	
	    file_name = 'mysql-backup-' + result_str + '.zip'
	    q = Auth(access_key, secret_key)
	    token = q.upload_token('这里是新建的存储空间的名字', file_name, 3600)
	    ret, info = put_file(token, file_name, backup_file_zip)
	    print('qiniuhelper.py qiniu_backup_mysql ret:' + str(ret))
	    print('qiniuhelper.py qiniu_backup_mysql info:' + str(info))

