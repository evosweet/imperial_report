import falcon,json,ast,requests,socket,datetime,random,string
import os, sys
import uuid
import mimetypes
from authenticate import Auth
sys.path.append('..')
from db.db import DBUtil
from smtp.smtp import SendMail

CONTENT_TYPE = 'application/json'
RESP = {'msg':'','result': ''}
URL = "http://localhost:8042"


class Index(object):
    def on_get(self, req, resp):
        try:
            resp.status = falcon.HTTP_200
            resp.content_type = CONTENT_TYPE
            RESP['msg'] = "The God Emperor Reigns Supreme! Imperial Fist"
            RESP['result'] = 'SUCCESS'
        except Exception as identifier:
            resp.status = falcon.HTTP_500
            resp.content_type = CONTENT_TYPE
            RESP['msg'] = identifier.message
        finally:
            resp.data = json.dumps(RESP)

class CreateIncident(object):
    """creates incidents"""
    def sendCitzen(self,id,email,type):
        try:
             r = requests.post(URL,json={'id':id, 'email':email, 'type':type},timeout=0.01)
        except Exception as identifier:
            pass
       
    
    def sendAuth(self,id,email,type):
        try:
            r = requests.post(URL,json={'id':id, '_to':email, 'type':type},timeout=0.01)
        except Exception as identifier:
            pass
    
    def on_post(self, req, resp):
        """"Post request"""
        try:
            data = ast.literal_eval(req.stream.read(req.content_length or 0))
            if data:
                report_id = DBUtil().add_incident(data)
                if report_id:
                    resp.status = falcon.HTTP_200
                    resp.content_type = CONTENT_TYPE
                    RESP['msg'] = {"reference_no":report_id}
                    RESP['result'] = 'SUCCESS'
                    event = DBUtil().get_event_by_id({'id':data['event_id']})
                    auth = DBUtil().get_event_email(data)
                    if 'email' in data:
                        self.sendCitzen(report_id, data['email'], event)
                    self.sendAuth(report_id, auth, event)
                else:
                    resp.status = falcon.HTTP_500
                    RESP['msg'] = "An ERROR Occured"
                    RESP['result'] = 'ERROR'
            else:
                RESP['msg'] = "we jamming"
        except Exception as identifier:
            print identifier.message
            resp.status = falcon.HTTP_500
            RESP['msg'] = identifier.message
        finally:
            resp.data = json.dumps(RESP)


class SaveIncidentImage(object):
    """Saves images"""
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def on_post(self, req, resp):
        """post request"""
        try:
            ext = mimetypes.guess_extension(req.content_type) 
            incident_id = req.get_header("INCIDENT-ID")
            print incident_id
            filename = '{uuid}{ext}'.format(uuid=uuid.uuid4(), ext=ext)
            image_path = os.path.join(self.storage_path, filename)
            with open(image_path, 'wb') as image_file:
                while True:
                    chunk = req.stream.read(4096)
                    if not chunk:
                        break
                    image_file.write(chunk)
                print image_path
                DBUtil().add_incident_image({'image_path':filename, 'incident_id': incident_id})
                RESP['msg'] = "GOOD"
                RESP['result'] = 'SUCCESS'
        except Exception as identifier:
            print identifier.message
        finally:
            resp.data = json.dumps(RESP)



class GetIncidentImage(object):
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def on_get(self, req, resp):
        try:
            params = req.get_param('name')
            if params:
                try:
                    resp.content_type = 'image/png'
                    image_path = os.path.join(self.storage_path, params)
                    resp.body = file(image_path, 'rb').read()
                except IOError as identifier:
                    print identifier
                    resp.status = falcon.HTTP_200
                    resp.content_type = CONTENT_TYPE
                    RESP['msg'] = identifier.strerror
                    RESP['result'] = 'ERROR'
            else:
                resp.status = falcon.HTTP_200
                RESP['msg'] = 'No Images associated with this incident'
                RESP['result'] = 'ERROR'
        except Exception as identifier:
            resp.status = falcon.HTTP_500
            RESP['msg'] = identifier.message
            RESP['result'] = 'ERROR'
        finally:
            resp.data = json.dumps(RESP)

class GetIncidentInfo(object):
    def on_post(self, req, resp):
        try:
            data = ast.literal_eval(req.stream.read(req.content_length or 0))
            if data:
                print data
                if data['searchType'] == 'id':
                    print "here"
                    info = DBUtil().get_incident({'id':data['value']})
                else:
                    info = DBUtil().get_incident_email({'contact_email':data['value']})
                if info:
                    resp.status = falcon.HTTP_200
                    resp.content_type = CONTENT_TYPE
                    RESP['msg'] = []
                    print type(RESP['msg'])
                    RESP['msg'] = info
                    RESP['result'] = 'SUCCESS'
                else:
                    resp.status = falcon.HTTP_200
                    RESP['msg'] = 'No Incidents Found with that Number'
                    RESP['result'] = 'ERROR'
        except Exception as identifier:
            resp.status = falcon.HTTP_500
            RESP['msg'] = identifier.message
            RESP['result'] = 'ERROR'
        finally:
            print type(RESP['msg'])
            resp.data = json.dumps(RESP)

class GetIncidentByEvent(object):
    def on_post(self, req, resp):
        try:
            data = ast.literal_eval(req.stream.read(req.content_length or 0))
            if data:
                info = DBUtil().get_incident_event(data)
                print info
                if info:
                    resp.status = falcon.HTTP_200
                    resp.content_type = CONTENT_TYPE
                    RESP['msg'] = []
                    RESP['msg'] = info
                    RESP['result'] = 'SUCCESS'
                else:
                    resp.status = falcon.HTTP_200
                    RESP['msg'] = 'No Incidents Found with that Number'
                    RESP['result'] = 'ERROR'
            else:
                resp.status = falcon.HTTP_400
                RESP['msg'] = 'Not enough Arguments passed'
                RESP['result'] = 'ERROR'
        except Exception as identifier:
            resp.status = falcon.HTTP_500
            RESP['msg'] = identifier.message
            RESP['result'] = 'ERROR'
        finally:
            resp.data = json.dumps(RESP)

class GetIncidentByAuth(object):
    def on_post(self, req, resp):
        try:
            data = ast.literal_eval(req.stream.read(req.content_length or 0))
            if data:
                info = DBUtil().get_incident_auth(data)
                if info:
                    resp.status = falcon.HTTP_200
                    resp.content_type = CONTENT_TYPE
                    RESP['msg'] = []
                    RESP['msg'] = info
                    RESP['result'] = 'SUCCESS'
                else:
                    resp.status = falcon.HTTP_200
                    RESP['msg'] = 'No Incidents found'
                    RESP['result'] = 'ERROR'
            else:
                resp.status = falcon.HTTP_400
                RESP['msg'] = 'Not enough Arguments passed'
                RESP['result'] = 'ERROR'
        except Exception as identifier:
            resp.status = falcon.HTTP_500
            RESP['msg'] = identifier.message
            RESP['result'] = 'ERROR'
        finally:
            resp.data = json.dumps(RESP)

class CreateUser(object):
    def on_post(self, req, resp):
        """post method"""
        try:
            isvalid = Auth().authenticate(req.get_header("authToken"), 2)
            print isvalid
            if isvalid['Allow'] == 1:
                print "here"
                data = ast.literal_eval(req.stream.read(req.content_length or 0))
                print data
                if data:
                    pw = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
                    print pw
                    params = {'username':data['username'], 'pw':pw,'level':'user', 'created_by':isvalid['user'], 'dt_created':str(datetime.datetime.now()), 'auth_id':data['auth_id']}
                    print params
                    if DBUtil().add_user(params):
                        resp.content_type = CONTENT_TYPE
                        resp.status = falcon.HTTP_200
                        RESP['msg'] = "GOOD"
                        RESP['result'] = 'SUCCESS'
                        try:
                            r = requests.post(URL,json={'pw':pw, 'user':email},timeout=0.01)
                        except Exception as identifier:
                            pass
                    else:
                        resp.content_type = CONTENT_TYPE
                        resp.status = falcon.HTTP_400
                        RESP['msg'] = "UNABLE TO ADD"
                        RESP['result'] = 'ERROR'
            else:
                resp.content_type = CONTENT_TYPE
                resp.status = isvalid['res']
                RESP['msg'] = isvalid['msg']
                RESP['result'] = 'ERROR'
        except Exception as identifier:
            print identifier
            resp.content_type = CONTENT_TYPE
            resp.status = falcon.HTTP_500
            RESP['msg'] = "UNABLE TO ADD"
            RESP['result'] = 'ERROR'
        finally:
            resp.data = json.dumps(RESP)

class Login(object):
    def on_post(self, req, resp):
        """post method"""
        try:
            data = ast.literal_eval(req.stream.read(req.content_length or 0))
            if data:
                token = Auth().gettoken(data)
                resp.status = falcon.HTTP_200
                RESP = token
        except Exception as identifier:
            print identifier
        finally:
            resp.data = json.dumps(RESP)


