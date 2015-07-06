import requests



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


    def _prepare_csrftoken(self,url):
        self.client.get(url)
        csrftoken=self.client.cookies['csrftoken']
        return csrftoken


if __name__=='__main__':
    up=login_uploader()
    up.login('admin','admin','http://127.0.0.1:8000/blog/login')
    up.upload('/tmp/t.jpg','http://127.0.0.1:8000/blog/images_upload/')
