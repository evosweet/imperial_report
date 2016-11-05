import falcon,ast
from falcon_cors import CORS
import smtplib,uuid,time
import socket,json,Queue,threading
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText



class SendMail(object):
    """Send mail class"""
    def __init__(self):
        self.LOGIN = 'guytestgov@gmail.com'
        self.PASS = 'uS4BCha5UgMxy78Y'
        self.msg = MIMEMultipart()
        self.msg['From'] = self.LOGIN

    def on_post(self, req, resp):
        """sends mail"""
        try:
            data = ast.literal_eval(req.stream.read(req.content_length or 0))
            if data:
                self.msg['To'], self.msg['subject'] = data['_to'], data['subject']
                self.msg.attach(MIMEText(data['msg']))
                mailserver = smtplib.SMTP('smtp.gmail.com', 587)
                # identify ourselves to smtp gmail client
                mailserver.ehlo()
                # secure our email with tls encryption
                mailserver.starttls()
                # re-identify ourselves as an encrypted connection
                mailserver.ehlo()
                mailserver.login(self.LOGIN, self.PASS)
                mailserver.sendmail(self.LOGIN, data['_to'], self.msg.as_string())
                mailserver.quit()
            resp.status = falcon.HTTP_200
        except Exception as identifier:
            pass
CORZ = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)
API = falcon.API(middleware=[CORZ.middleware])

EMAIL = SendMail()

API.add_route('/', EMAIL)
# SEND = SendMail()
# SEND.sendmail('this is a test', 'This is how we do it', 'desonalleyne@yahoo.com')
