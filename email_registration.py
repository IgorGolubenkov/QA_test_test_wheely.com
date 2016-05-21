
import hashlib
import requests

class Emailhelper:

    def get_hash_email(self, email):
        return hashlib.md5(email.encode('utf-8')).hexdigest()


    def get_mailbox(self, email):
        email_hash = self.get_hash_email(email)
        url_get = 'http://api.temp-mail.ru/request/mail/id/%s/format/json/' % email_hash
        req = requests.get(url=url_get)
        return req.json()

req = Emailhelper()
#print(req.get_mailbox("gebufu@divismail.ru"))

hash = req.get_hash_email("gebufu@divismail.ru")
url_get = 'http://api.temp-mail.ru/request/mail/id/%s/format/json/' % hash
req_get = requests.get(url=url_get, verify=False)
print()
