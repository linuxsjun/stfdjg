from django.test import TestCase

# Create your tests here.

from django.db import models

class hr_Test(models.Model):
    name=models.CharField(max_length=32)
    crnu=models.IntegerField(default=1)

    class Meta:
        db_table='hr_test'

#         < div
#
#         class ="app" >
#
#         < form
#         action = "#"
#         method = "post"
#         name = "mailto"
#         id = "mailto" >
#         < p > < input
#
#         class ="input-file" type="file" placeholder="Add your files" > < / p >
#
#         < p > < input
#
#         class ="input-mail" type="email" placeholder="Email to" > < / p >
#
#         < p > < input
#
#         class ="input-mail" type="email" placeholder="you mail" > < / p >
#
#         < p > < input
#
#         class ="input-note" type="text" placeholder="Message" > < / p >
#
#         < p > < input
#
#         class ="but-mailto" type="submit" value="Transfer" > < / p >
#
#     < / form >
#     < div
#
#     class ="notes" >
#
#     < p >
#     欢迎使用
#
# < / p >
# < p >
# 应用程序
# < / p >
# < / div >
# < / div >
# < div
#
#
# class ="app" >
#
# < img
# src = "/static/img/ftp-icon.jpg"
# alt = "" / >
# < p > < h4 > FTP < / h4 > < / p >
# < / div >

    # var = base_conf.objects.get(id=1)
    # print(var.expirestime)
    #  if var.token:
    #     nowtime=time.time()
    #     if time.mktime(time.strptime(var.expirestime)) > nowtime:
    #         print('token is ok')
    #     else:
    #         print('token is no')
    # else:
    #     print('token is no')
    #
    # if var.corpid :
    #     id=var.corpid
    #     secrect=var.corpsecret
    #
    # #todo 判断Token是否有效，如无效重新申请并存进数据库
    # #todo Token 为空？
    # #不为空在有效时间内？
    # #有效用
    # #无效：获取
    # sendurl='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s'%(id,secrect)
    #
    # r = requests.get(sendurl)
    #
    # print(r.content)
