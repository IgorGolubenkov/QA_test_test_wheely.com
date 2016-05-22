
from email_temporary import TempMail

tm = TempMail()
print(tm.get_mailbox('gebufu@divismail.ru'))

list_email = [{
    'mail_text': '\nтекст текст текст\n\nС уважением,\nДима Новиков\ndmitriy_novikov_1984@inbox.ru',
    'mail_html': '\n<HTML><BODY><br>текст текст текст<br><br>С уважением,<br>Дима Новиков<br>dmitriy_novikov_1984@inbox.ru</BODY></HTML>\n',
    'mail_from': 'Дима Новиков <dmitriy_novikov_1984@inbox.ru>',
    'mail_preview': '...',
    'createdAt': {},
    'mail_text_only': '\n<HTML><BODY><br>текст текст текст<br><br>С уважением,<br>Дима Новиков<br>dmitriy_novikov_1984@inbox.ru</BODY></HTML>\n',
    'mail_subject': 'пробное письмо', '_id': {},
    'mail_timestamp': 1463921341.318,
    'mail_id': '38a676fdf38a791c80b9f2c7b576e5ce',
    'mail_address_id': '7dcb37af28030aeef064785c88973f50'}]
