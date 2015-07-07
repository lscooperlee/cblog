import requests
import re
from datetime import datetime


class login_uploader:

    def __init__(self):
        self.client=requests.session()

    def login(self,username, password, url):
        csrftoken=self._prepare_csrftoken(url)
        login_data={'username':username,'password':password,'csrfmiddlewaretoken':csrftoken}
        self.client.post(url,login_data)

    def upload(self,filearg, url):
        from _collections_abc import Iterable

        if isinstance(filearg, Iterable) and not isinstance(filearg, str):
            for f in filearg:
                self.upload(f)
        if isinstance(filearg, str):
            files={'images':open(filearg, 'rb')}
            csrftoken=self._prepare_csrftoken(url)
            upload_data={'csrfmiddlewaretoken':csrftoken}
            self.client.post(url,upload_data,files=files)


    def post_blog(self, content, url, category='Uncategorized', authorname='admin', isdraft=False):

        content=content.strip()
        ret=re.search(r'#{1}.+\n',content)
        if ret:
            title=ret.group(0)[1:]
            body=content[len(title):]
        else:
            title="No Subject"
            body=content

        pub_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        r=self.client.get(url)
        csrftoken=self.client.cookies['csrftoken']

        ret=re.findall(r'<option.+?/option>',str(r.content))
        for i in ret:
            ret=re.search(r'value="(?P<v>\d+)".*?>(?P<name>\w+)<',i)
            if ret:
                d=ret.groupdict()
                if authorname == d['name']:
                    author=d['v']

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



    def _prepare_csrftoken(self,url):
        self.client.get(url)
        csrftoken=self.client.cookies['csrftoken']
        return csrftoken


if __name__=='__main__':
    up=login_uploader()
    up.login('admin','admin','http://127.0.0.1:8000/blog/login')
    aaa="""
            #this is tiasdfasdftleaa
            ##subtitles aaaa
        """
    up.post_blog(aaa, 'http://127.0.0.1:8000/blog/edit/','cate')
#    up.upload('/tmp/t.jpg','http://127.0.0.1:8000/blog/images_upload/')

