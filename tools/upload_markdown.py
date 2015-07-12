import requests
import re
import os
import shutil
from datetime import datetime
import time



class markdown_media_parser:


    def __init__(self,basicurl):
        basicurl=basicurl if basicurl[-1] == '/' else basicurl+'/'
        self.loginurl=basicurl+'login/'
        self.posturl=basicurl+'post_upload/'
        self.fileurl=basicurl+'file_upload/'
        self.up=login_uploader()

    def login(self,username,password):
        self.up.login(username,password,self.loginurl)

    def upload(self, filename, category='Uncategorized', authorname='admin', isdraft=False):
        basepostname=os.path.basename(filename)
        basefilename=os.path.splitext(basepostname)[0]

        file_list, content = self.parse_local_files(filename)
        print("parsing markdown file")
        try:
            os.mkdir(basefilename, mode=0o775)
        except FileExistsError:
            pass

        for f in file_list:
            newfilename=os.path.join(basefilename,os.path.basename(f))
            try:
                shutil.copyfile(f,newfilename)
            except shutil.SameFileError:
                pass

        contentlocal=self.contentreplace(content, file_list, basefilename)
        with open(basepostname, 'w') as fd:
            fd.write(contentlocal)

        print("uploading static files")
        for f in file_list:
            self.up.post_file(f, self.fileurl,  os.path.basename(basefilename))  #upload images

        print("uploading post")
        contentweb=self.contentreplace(content,file_list, '/media/', authorname, basefilename)
        self.up.post_blog(contentweb,self.posturl,category,authorname,isdraft)

        print("uploading markdown file")
        self.up.post_file(basepostname,self.fileurl) #upload_file

    def contentreplace(self, content,file_list, *pathargs):
        path=os.path.join(*pathargs)
        for i in file_list:
            newname=os.path.join(path, os.path.basename(i))
            content=content.replace(i,newname)
        return content

    def parse_local_files(self, filename):
        content=None

        with open(filename,'r') as f:
            content=f.read()

        if not content:
            return False


        p=re.compile(r'(?P<id>!\[.*\])\((?P<url>.*?)(\)|\s+.*\))')
        ret=p.findall(content)
        file_list=[ x[1] for x in ret if not re.match(r'^https?://',x[1])]

        return file_list,content


class login_uploader:

    def __init__(self):
        self.client=requests.session()

    def login(self,username, password, url):
        csrftoken=self._prepare_csrftoken(url)
        login_data={'username':username,'password':password,'csrfmiddlewaretoken':csrftoken}
        self.client.post(url,login_data)

    def post_file(self,filearg, url, subdir=""):
        with open(filearg,'rb') as fd:
            files={'files':fd}
            csrftoken=self.client.cookies['csrftoken']
            upload_data={'csrfmiddlewaretoken':csrftoken, "name":subdir}
            try:
                r=self.client.post(url,upload_data,files=files)
            except:
                pass
            # if r.status_code != 200:
            #     print(r.status_code)
            #     return False
            return True


    def post_blog(self, content, url, category='Uncategorized',
                  authorname='admin', isdraft=False, pub_date=""):

        content=content.strip()
        ret=re.search(r'#{1}.+\n',content)
        if ret:
            title=ret.group(0)[1:].strip()
            body=content.replace(str(ret.group(0)),"")
        else:
            title="No Subject"
            body=content

        url=url if url[-1] == '/' else url+'/'
        url=url+re.sub(r'[^_\w\d]','_',title)

        r=self.client.get(url)
        csrftoken=self.client.cookies['csrftoken']
        webcontent=str(r.content)

        ret=re.search(r'(?P<pub_date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',webcontent)
        date=ret.groupdict(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        ret=re.findall(r'<option.+?/option>',webcontent)
        author=None
        for i in ret:
            ret=re.search(r'value="(?P<v>\d+)".*?>(?P<name>\w+)<',i)
            if ret:
                d=ret.groupdict()
                if authorname == d['name']:
                    author=d['v']


        if not author:
            print("warning: no user %s on the website, try to use default one"%authorname)

        author=1

        payload={
            'title': title,
            'pub_date': date['pub_date'],
            'author': author,
            'isdraft':isdraft,
            'category': category,
            'body':body,
            'csrfmiddlewaretoken':csrftoken,
        }

        try:
            r=self.client.post(url,data=payload)
        except:
            pass
        # if r != 200:
        #     return False
        return True


    def _prepare_csrftoken(self,url):
        self.client.get(url)
        csrftoken=self.client.cookies['csrftoken']
        return csrftoken


if __name__=='__main__':
    import argparse
    import sys

    parser=argparse.ArgumentParser()

    parser.add_argument('-u',nargs=1,required=True)
    parser.add_argument('-p',nargs=1,required=True)
    parser.add_argument('-a',nargs=1,required=True)
    parser.add_argument('-c',nargs=1,required=True)
    parser.add_argument('-f',nargs=1,required=True)
    parser.add_argument('--url', nargs=1,required=True)

    args=vars(parser.parse_args(sys.argv[1:]))
    argdict={ k: args[k][0] for k in args}

    p=markdown_media_parser(argdict['url'])
    p.login(argdict['u'],argdict['p'])
    p.upload(filename=argdict['f'],category=argdict['c'],authorname=argdict['u'])



