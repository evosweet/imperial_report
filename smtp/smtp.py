import smtplib,uuid,time
import socket,json,Queue,threading
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

pending_q = Queue.Queue()
worker_q = Queue.Queue(maxsize=40)

class SendMail(threading.Thread):
    """Send mail class"""
    def __init__(self,request,q):
        self.LOGIN = 'guytestgov@gmail.com'
        self.PASS = 'uS4BCha5UgMxy78Y'
        self.msg = MIMEMultipart()
        self.msg['From'] = self.LOGIN
        self.req = request
        self.q = q
    
    def run(self):
        try:
            self.q.put(uuid.uuid1())
            self.sendmail(self.req['sub'], self.req['message'], self.req['_to'])
        except Exception as identifier:
            print identifier
        finally:
            self.q.get()
            self.q.task_done()

    def sendmail(self, subject, message, _to):
        """sends mail"""
        self.msg['To'], self.msg['subject'] = _to, subject
        self.msg.attach(MIMEText(message))
        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        # identify ourselves to smtp gmail client
        mailserver.ehlo()
        # secure our email with tls encryption
        mailserver.starttls()
        # re-identify ourselves as an encrypted connection
        mailserver.ehlo()
        mailserver.login(self.LOGIN, self.PASS)
        mailserver.sendmail(self.LOGIN, _to, self.msg.as_string())
        mailserver.quit()



def start_mail_socket():
    try:
        prov_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        prov_soc.bind(('',9088))
        prov_soc.listen(100)
    except Exception as e:
        print e
    finally:
        while 1:
            try:
                data,address = prov_soc.accept()
                request = json.loads(data.recv(3000).decode('UTF-8'))
                pending_q.put(request)
            except Exception as e:
                print  e
            finally:
                pass

def process_req_q():
    while 1:
        try:
            if worker_q.full() is False:
                request = pending_q.get()
                pending_q.task_done()
                worker = SendMail(request, worker_q)
                worker.setDaemon(True)
                worker.start()
        except Exception as e:
            print e

def show_status():
    while 1:
        try:
            threadstatus = {'Backlog':pending_q.qsize(),'WorkerThreads':worker_q.qsize()}
            print threadstatus
            time.sleep(5)
        except Exception as e:
            print e

# application status
status_thread = threading.Thread(target=show_status)
status_thread.setDaemon = True
status_thread.start()

p_thread = threading.Thread(target=process_req_q)
p_thread.setDaemon(True)
p_thread.start()
# SEND = SendMail()
# SEND.sendmail('this is a test', 'This is how we do it', 'desonalleyne@yahoo.com')
