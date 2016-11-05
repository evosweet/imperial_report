import falcon,ast,datetime
from falcon_cors import CORS
import smtplib,uuid,time
import socket,json,Queue,threading
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

CORZ = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)
API = falcon.API(middleware=[CORZ.middleware])



# req = {"email":"l@b.com","type":"FIRE","id":1,"desc":"blah blah","Date":str(datetime.date.today())}
# print BODY % (req['email'],req['type'],req['id'],req['type'],req['desc'],req['Date'],req['email'])
class SendMail(object):
    """Send mail class"""
    def __init__(self):
        self.LOGIN = 'guytestgov@gmail.com'
        self.PASS = 'uS4BCha5UgMxy78Y'
        self.msg = MIMEMultipart('alternative')
        self.msg['From'] = self.LOGIN
        self.msg['subject']  = "An incident has been reported"
        self.citizen ="""
            <html>
            <head>
                <link type="text/css" rel="stylesheet" href="https://html-online.com/editor/tinymce/skins/lightgray/content.min.css">
            </head>
            <body>
                <h1 style="color: #5e9ca0;"><span style="color: #333399;"><strong>Citizen Incident Reporting System</strong></span><img style="float: right;" src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Coat_of_arms_of_Guyana.svg/250px-Coat_of_arms_of_Guyana.svg.png" alt="" width="96" height="92" /></h1>
            <h2 style="padding-left: 30px; text-align: center;"><span style="color: #3366ff;"><strong>Lorem Ispum Ispum Lorem</strong></span></h2>
            <hr />
            <h2 style="text-align: center;">&nbsp;<span style="color: #3366ff;">Report submitted!</span></h2>
            <p>&nbsp;</p>
            <p>Hi <strong>%s</strong>,</p>
            <p>You have successfully submitted a <strong>%s-Related</strong> incident report. Thank you.</p>
            <p>&nbsp;</p>
            <p>This report has been sent to the relevant authorities for further action:</p>
            <p>&nbsp;</p>
            <p><br />You can check this incident's status and follow up with the authorities by entering the Reference # %s at http://192.168.43.234 &nbsp;</p>
            <p>&nbsp;</p>
            <p><strong>Thanks.</strong></p>
            <p><strong>The CIRS team.&nbsp;</strong></p>
            <h2>&nbsp;</h2>
            <p style="text-align: center;"><strong>A GoG Initiative! &nbsp;</strong></p>
            <p style="text-align: center;"><strong>Brought to you by Imperial Fist &reg; and&nbsp;<a href="https://html-online.com/editor/">Html-Online</a></strong></p>
            <p><strong>&nbsp;</strong></p>
            </body>
            </html>
"""
        self.auth ="""
            <html>
            <head>
                <link type="text/css" rel="stylesheet" href="https://html-online.com/editor/tinymce/skins/lightgray/content.min.css">
            </head>
            <body>
                <h1 style="color: #5e9ca0;"><span style="color: #333399;"><strong>Citizen Incident Reporting System</strong></span><img style="float: right;" src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Coat_of_arms_of_Guyana.svg/250px-Coat_of_arms_of_Guyana.svg.png" alt="" width="96" height="92" /></h1>
            <h2 style="padding-left: 30px; text-align: center;"><span style="color: #3366ff;"><strong>Lorem Ispum Ispum Lorem</strong></span></h2>
            <hr />
            <h2 style="text-align: center;">&nbsp;<span style="color: #3366ff;">Report submitted!</span></h2>
            <p>&nbsp;</p>
            <p> Dear Government Officer(s),</p>
            <p>A  <strong>%s-Related</strong> incident has been successfully submitted by a watchful citizen. Thank you.</p>
            <p>&nbsp;</p>
            <p><br />You can check this incident's status and make updates by entering the Reference # %s at http://192.168.43.234 &nbsp;</p>
            <p>&nbsp;</p>
            <p><strong>Thanks.</strong></p>
            <p><strong>The CIRS team.&nbsp;</strong></p>
            <h2>&nbsp;</h2>
            <p style="text-align: center;"><strong>A GoG Initiative! &nbsp;</strong></p>
            <p style="text-align: center;"><strong>Brought to you by Imperial Fist &reg; and&nbsp;<a href="https://html-online.com/editor/">Html-Online</a></strong></p>
            <p><strong>&nbsp;</strong></p>
            </body>
            </html>
"""

    def on_post(self, req, resp):
        """sends mail"""
        try:
            data = ast.literal_eval(req.stream.read(req.content_length or 0))
            if data:
                if 'email'  in data:
                    recipients = data['email']
                    self.msg['To'] = data['email']
                    body = self.citizen % (data['email'], data['type'], data['id'])
                else:
                    recipients = data['_to']
                    self.msg['To'] = ", ".join(data['_to'])
                    body = self.auth % (data['type'],data['id'])
                self.msg.attach(MIMEText(body,'html'))
                mailserver = smtplib.SMTP('smtp.gmail.com', 587)
                # identify ourselves to smtp gmail client
                mailserver.ehlo()
                # secure our email with tls encryption
                mailserver.starttls()
                # re-identify ourselves as an encrypted connection
                mailserver.ehlo()
                mailserver.login(self.LOGIN, self.PASS)
                mailserver.sendmail(self.LOGIN, recipients, self.msg.as_string())
                mailserver.quit()
            resp.status = falcon.HTTP_200
        except Exception as identifier:
            print  identifier

EMAIL = SendMail()

API.add_route('/', EMAIL)
# SEND = SendMail()
# SEND.sendmail('this is a test', 'This is how we do it', 'desonalleyne@yahoo.com')

