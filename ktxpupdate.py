#coding=utf-8
import os
import _elementpath as DONTUSE
from pyquery import PyQuery as pq  
import urllib
import sys
import sqlite3
import webbrowser

dirNow=os.path.dirname(sys.argv[0])

tLast="2012/04/05 00:00"
strfile=dirNow+'\list.txt'
try:
        f2 = file(strfile, 'rb')
except:
        print "请在目录下创建list.txt，并以行为分隔写入关键词".decode('utf').encode('gbk')
        os.system('pause')
        sys.exit(0)

strfile=dirNow+'\\time.txt'
try:
        f3 = file(strfile, 'rb')
        tTemp=f3.readlines()
        tLast=tTemp[0]
        f3.close()    
except:
        try:
                f3.close()
        except:
                None
        print 'time.txt不存在或为空，默认起始时间为2012/04/05 00:00，你可以编辑time.txt修改起始时间，格式为"yyyy/mm/dd hh:mm"'.decode('utf').encode('gbk')
        os.system('pause')

print "正在更新中……".decode('utf').encode('gbk')

cx = sqlite3.connect("ktxp.db")
cx.isolation_level = None
cx.text_factory = str
cu = cx.cursor()
cu.execute('create table if not exists t1(id integer primary key,subTime string,name string UNIQUE,magnetAdd string)')
hasNew=0
for keyword in f2:
    t = []
    name=[]
    add=[]
    k=0
    s_utf=keyword.decode(sys.stdin.encoding).encode("utf-8")
    url_str='http://bt.ktxp.com/search.php?keyword=%s'%urllib.quote(s_utf)
    d = pq(url=url_str)
    div=d('tbody td')
    for i in div(":contains(':')"):
        t.append(pq(i).attr('title'))
        k=k+1
    diva=div('a')
    for i in diva("[href^='/html']"):
        name.append(pq(i).text().encode('utf'))
    for i in diva("[href$='.torrent']"):
        add.append(pq(i).attr('href'))
    for i in range(0,k):
        if t[i]>tLast:
            strTemp='\''+t[i]+'\',\''+name[i]+'\',\''+add[i]+'\')'
            try:
                    cu.execute("insert into t1(subTime,name,magnetAdd) values('%s','%s','%s')"%(t[i],name[i],add[i]))
                    print name[i].decode('utf').encode('gbk')
                    hasNew=hasNew+1
            except:
                    None
f2.close()
cx.commit()

cu.execute("select * from t1 Order by subTime desc")
res = cu.fetchall()
f = file('index.html', 'w')
f.write('''
<html>
    <head>
        <meta charset="utf-8">
        <title>团子极影动漫更新列表</title>
        <link href="css/bootstrap.css" rel="stylesheet">
        <link href="css/bootstrap-responsive.css" rel="stylesheet">
    <head>
    <body>

  <div class="navbar">
    <div class="navbar-inner">
    <div class="container" style="width: auto;">
    
    <!-- .btn-navbar is used as the toggle for collapsed navbar content -->
    <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
    <span class="icon-bar"></span>
    <span class="icon-bar"></span>
    <span class="icon-bar"></span>
    </a>
    <a class="brand" href="#"><strong>极影动漫更新列表</strong></a>
      <div class="nav-collapse">
        <ul class="nav">
            <li>
                <a href="http://bt.ktxp.com" style="font-size:20">极影官网</a>
            </li>
        </ul>

        <ul class="nav pull-right">
            <a><h2><span class="label label-info" style="font-size:20">BY 叉烧团子</span></h2></a>
        </ul>
        <ul class="nav pull-right">
            <a><h2  style="color:#AAAAAA;margin: 0 40 0 0">有 <span class="label label-important" style="font-size:20">%s</span> 个更新</h2></a>
        </ul>
    </div>
    </div>
    </div>
    </div>
    
<div class="container-fluid">
<div class="row-fluid">
<div class="span" style="margin: 0 0 0 10;">
        '''%str(hasNew))
j=0;
for (dbid,dbtime,dbname,dbadd) in res:
    if dbtime>tLast:
            tLast=dbtime
    strTemp='''
    <div class="row show-grid">
        <div class="span" style="background-color: #EEEEEE;border-radius: 8;margin: 5;padding: 5">
            <a href=\"http://bt.ktxp.com/%s\"><h3><strong>%s %s</strong></h3></a>
        </div>
    </div>'''%(dbadd,dbtime,dbname)
    f.write(strTemp)
f.write('''
                </div>
            </div>
        </div>
    </body>
</html>
        ''')
f.close()

f3 = file(strfile, 'wb')
f3.write(tLast)
f3.close()

cu.close()
cx.close()

print "更新结束".decode('utf').encode('gbk')
if hasNew:
        print "总共更新了%s个!".decode('utf').encode('gbk')%str(hasNew)
else:
        print "暂时没有更新，查看过去更新的内容请打开index.html。".decode('utf').encode('gbk')

os.system('pause')
if hasNew:
        webbrowser.open_new_tab(os.getcwd()+'\index.html')
