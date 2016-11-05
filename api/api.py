import falcon,json,ast,requests
import os, sys
import uuid
import mimetypes
sys.path.append('..')
from db.db import DBUtil

CONTENT_TYPE = 'application/json'
RESP = {'msg':''}

class Index(object):
    def on_get(self, req, resp):
        try:
            resp.status = falcon.HTTP_200
            resp.content_type = CONTENT_TYPE
            RESP['msg'] = "The God Emperor Reigns Supreme! Imperial Fist"
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
                else:
                    resp.status = falcon.HTTP_500
                    RESP['msg'] = "An ERROR Occured"
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
            # RESP['msg'] ={}
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
                DBUtil().add_incident_image({'image_path':image_path,'incident_id':incident_id})
                RESP['msg'] ="GOOD"
        except Exception as identifier:
            print identifier.message
        finally:
            resp.data = json.dumps(RESP)


