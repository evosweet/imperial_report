import falcon,json,ast,requests
import os, sys
import uuid
import mimetypes
sys.path.append('..')
from db.db import DBUtil

CONTENT_TYPE = 'application/json'
RESP = {'msg':'','result': ''}

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
    def on_post(self, req, resp):
        try:
            data = ast.literal_eval(req.stream.read(req.content_length or 0))
            if data:
                report_id = DBUtil().add_incident(data)
                if report_id:
                    resp.status = falcon.HTTP_200
                    resp.content_type = CONTENT_TYPE
                    RESP['msg'] = {"reference_no":report_id}
                    RESP['result'] = 'SUCCESS'
                else:
                    resp.status = falcon.HTTP_500
                    RESP['msg'] = "An ERROR Occured"
                    RESP['result'] = 'ERROR'
            else:
                RESP['msg'] = "we jamming"
        except Exception as identifier:
            resp.status = falcon.HTTP_500
            RESP['msg'] = identifier.message
        finally:
            resp.data = json.dumps(RESP)


class SaveIncidentImage(object):
    def __init__(self, storage_path):
        self.storage_path = storage_path

    def on_post(self, req, resp):
        try:
            ext = mimetypes.guess_extension(req.content_type) 
            incident_id = req.get_header("INCIDENT-ID")
            filename = '{uuid}{ext}'.format(uuid=uuid.uuid4(), ext=ext)
            image_path = os.path.join(self.storage_path, filename)
            with open(image_path, 'wb') as image_file:
                while True:
                    chunk = req.stream.read(4096)
                    if not chunk:
                        break
                    image_file.write(chunk)
                DBUtil().add_incident_image({'image_path':filename,'incident_id':incident_id})
                RESP['msg'] ="GOOD"
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
            params = req.get_param('path')
            if params:
                try:
                    resp.content_type = 'image/png'
                    print type(params)
                    image_path = os.path.join(self.storage_path, params)
                    print image_path
                    resp.stream = file(image_path, 'rb').read()
                    resp.stream_len = os.path.getsize(image_path)
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


