import requests
import re
import os
from datetime import datetime



class markdown_media_parser:

    MEDIA_PATH='/media/'

    def __init__(self,basicurl):
        basicurl=basicurl if basicurl[-1] == '/' else basicurl+'/'
        self.loginurl=basicurl+'login/'
        self.posturl=basicurl+'post_upload/'
        self.fileurl=basicurl+'file_upload/'
        self.up=login_uploader()

    def login(self,username,password):
        self.up.login(username,password,self.loginurl)

    def upload(self, filename, category='Uncategorized', authorname='admin', isdraft=False):

        file_list, content = self.parse_local_files(filename,authorname)
        sub=os.path.splitext(os.path.basename(filename))[0]
        for f in file_list:
            self.up.upload(f, self.fileurl, os.path.basename(sub))  #upload images

        self.up.post_blog(content,self.posturl,category,authorname,isdraft)
        self.up.upload(filename,self.fileurl) #upload_file


    def parse_local_files(self, filename, authorname):
        content=None

        with open(filename,'r') as f:
            content=f.read()

        if not content:
            return False

        basefile=os.path.splitext(os.path.basename(filename))[0]

        p=re.compile(r'(?P<id>!\[.*\])\((?P<url>.*?)(\)|\s+.*\))')
        ret=p.findall(content)
        file_list=[ x[1] for x in ret if not re.match(r'^https?://',x[1])]
        for i in file_list:
            newname=os.path.join(self.MEDIA_PATH, authorname,basefile,os.path.basename(i))
            content=content.replace(i,newname)

        return file_list,content


class login_uploader:

    def __init__(self):
        self.client=requests.session()

    def login(self,username, password, url):
        csrftoken=self._prepare_csrftoken(url)
        login_data={'username':username,'password':password,'csrfmiddlewaretoken':csrftoken}
        self.client.post(url,login_data)

    def upload(self,filearg, url, subdir=""):
        files={'files':open(filearg, 'rb')}
        csrftoken=self._prepare_csrftoken(url)
        upload_data={'csrfmiddlewaretoken':csrftoken, "name":subdir}
        r=self.client.post(url,upload_data,files=files)
        if r.status_code != 200:
            return False
        return True


    def post_blog(self, content, url, category='Uncategorized', authorname='admin', isdraft=False):

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
        pub_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        r=self.client.get(url)
        csrftoken=self.client.cookies['csrftoken']
        ret=re.findall(r'<option.+?/option>',str(r.content))

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
            'pub_date': pub_date,
            'author': author,
            'isdraft':isdraft,
            'category': category,
            'body':body,
            'csrfmiddlewaretoken':csrftoken,
        }


        r=self.client.post(url,data=payload)
        if r != 200:
            return False
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



