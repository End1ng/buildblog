# -*- coding: UTF-8 -*-
import os
import linecache

#        作者：End1ng
#        --------------------------------
# 自己的博客简单框架
# 报错再来一次
blogname = "End1ng"
personemail = "XXXXXXXX@qq.com"
# 定义blog源码路径
NUM = 0
# 博客内容
contentpath = "concent"
# 公共文件
publicpath = "public"
# 资源文件
sourcepath = "source"
# 生成的博客源码路径
destpath = "../local3"
# html头尾文件
headerpath = "header.html"
footerpath = "footer.html"
indexpath = "index.html"

slash = '/'
# 不建立的文件或文件夹
nolist = ['index.html','sqlierror.html']

contentlen = len(contentpath)

# 安装初始化####################################################
if not os.path.exists(contentpath):
    os.mkdir(contentpath)

if not os.path.exists(publicpath):
    os.mkdir(publicpath)

if not os.path.exists(sourcepath):
    os.mkdir(sourcepath)

if not os.path.exists(destpath):
    os.mkdir(destpath)

if not os.path.exists(os.path.join(contentpath,indexpath)):
    with open(os.path.join(contentpath,indexpath), 'w') as f:
        f.write(indexpath)

if not os.path.exists(os.path.join(publicpath,headerpath)):
    with open(os.path.join(publicpath,headerpath), 'w') as f:
        f.write("public/header")

if not os.path.exists(os.path.join(publicpath,footerpath)):
    with open(os.path.join(publicpath,footerpath), 'w') as f:
        f.write("public/footer")
#################################################################

# 读取公共文件
with open(os.path.join(publicpath,headerpath), 'r') as f:
    headercont = f.read()

with open(os.path.join(publicpath,footerpath), 'r') as f:
    footercont = f.read()

# 索引内容
dircontent = """
                            <div class="panel-group">
"""
# 索引头
panelstart = """
                                <div class="panel panel-default" >
                                    <div class="panel-heading" data-toggle="collapse" data-target="#{datatarget}">
                                        <h4 class="panel-title"><span class="glyphicon glyphicon-step-forward"> {datatarget}</span></h4>
                                    </div>
                                <div id="{datatarget}" class="panel-collapse collapse">
                                    <div class="panel-body">
"""
# 索引尾
paneltail = """
                                    </div>
                                </div>
                                </div>
"""
# 链接格式
panellink = """
                                        <a href="{link}" class="btn btn-default btn-block">
                                            <span class="glyphicon glyphicon-tag"> {title}</span>
                                        </a>
"""
# 根据content目录形成索引
def getfilelist(thepath):
    global dircontent
    global panelstart
    global panellink
    global NUM
    filelist = os.listdir(thepath);
    for file in filelist:
        if os.path.isfile(thepath + slash + file):
            if file not in nolist:
                NUM += 1
                title = linecache.getline(thepath + slash + file,2).strip()
                dircontent += panellink.format(link=thepath[contentlen:].decode('gbk').encode('utf-8') + \
                    slash + file.decode('gbk').encode('utf-8'),title=title)
        else:
            dircontent += panelstart.format(datatarget=file.decode('gbk').encode('utf-8'))
            getfilelist(thepath + slash + file)
            dircontent += paneltail

getfilelist(contentpath)
dircontent += """
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-8 col-md-offset-2">
<!------------------------------------------------------------------------------>
"""
# 写入博客源码目录
def writefile(thepath):
    global headercont
    filelist = os.listdir(thepath);
    for file in filelist:
        if os.path.isfile(thepath + slash + file):
            headercontent = headercont.format(blogname=blogname,personemail = personemail,title=os.path.splitext(file)[0])
            with open(thepath + slash + file,'r') as f:
                content = f.read()
            with open(destpath + thepath[contentlen:] + slash + file,'w') as f:
                f.write(headercontent + dircontent + content + footercont)
        else:
            if not os.path.exists(destpath + thepath[contentlen:] + slash + file):
                os.makedirs(destpath + thepath[contentlen:] + slash + file)
            writefile(thepath + slash + file)

# 复制资源文件
def copyFiles(sourcepath,  destpath):
    for file in os.listdir(sourcepath):
        sourceFile = sourcepath + slash + file
        targetFile = destpath + slash + file
        if os.path.isfile(sourceFile):
            if not os.path.exists(destpath):
                os.makedirs(destpath)
            open(targetFile, "wb").write(open(sourceFile, "rb").read())
        if os.path.isdir(sourceFile):
            copyFiles(sourceFile, targetFile)
# 清空博客源码目录
def removeFileInFirstDir(destpath):
    for file in os.listdir(destpath):
        if file != ".git":
            targetFile = destpath + slash + file
            if os.path.isfile(targetFile):
                os.remove(targetFile)
            if os.path.isdir(targetFile):
                removeFileInFirstDir(targetFile)
                os.rmdir(targetFile)

# 清空博客源码目录
removeFileInFirstDir(destpath)
# 复制资源文件
copyFiles(sourcepath,  destpath)
# 写入博客源码目录
writefile(contentpath)

print "build " + str(NUM) + " pages"