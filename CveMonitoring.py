#coding=utf-8

import requests
import re
import time
import smtplib
from email.mime.text import MIMEText

class CVE(object):
    def __init__(self):
        self.headres={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
        self.open=open("CVE.html","w+")
    def cve_scan(self):
        url="https://cassandra.cerias.purdue.edu/CVE_changes/today.html"
        urlscan=requests.get(url,headers=self.headres,verify=False)
        cve_re=re.compile(r"<A HREF = '(.+?)'>(.+?)</A><br />")
        re_cve=re.findall(cve_re,urlscan.text)
        for cve in re_cve:
            print ("CVE-"+cve[1])
            urlcve=requests.get(cve[0],headers=self.headres,verify=False)
            recve=re.compile(r'<tr>.+?<th colspan="2">Description</th>.+?</tr>.+?<tr>.+?<td colspan="2">(.+?)</td>.+?</tr>',re.DOTALL)
            cvere=re.findall(recve,urlcve.text)
            for cvecve in cvere:
                self.open.write("<style>a{text-decoration: none;}</style>CVE-ID：<a href="+cve[0]+" target='_blank'>CVE-"+cve[1]+"</a><p>描述："+cvecve+"</p></br>")
                self.open.flush()
                print(cvecve)

    def email(self):
        _user = "XXX@XXX.com" #发件人邮箱账号
        _pwd  = "password"  #SMTP发件人密码
        _to   = "XXXXXX@XXX.com" #接收邮箱账号
        f_f=open("CVE.html",'r+')
        f_ff=f_f.read()
        if len(f_ff)==0:
            pass
        if len(f_ff)>0:
            print (f_ff)
            msg = MIMEText(f_ff,_subtype='html',_charset='utf-8')
            msg["Subject"] = u"CVE漏洞监控列表"
            msg["From"]    = _user
            msg["To"]      = _to

            try:
                s = smtplib.SMTP("xxx.com",25)
                s.login(_user, _pwd)
                s.sendmail(_user, _to, msg.as_string())
                s.quit()
                print ("Success!")
            except:
                print ("Falied")

if __name__ == '__main__':
    CVESCAN=CVE()
    CVESCAN.cve_scan()
    CVESCAN.email()
