import falcon,json,ast,requests
import os
import uuid
import mimetypes


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
            data = req.stream.read(req.content_length or 0)
            print data
            resp.status = falcon.HTTP_200
            resp.content_type = CONTENT_TYPE
            resp['msg'] = "The end is nigh"
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
            # data = req.stream.read(req.content_length or 0)
            # print data
            # if data:
            RESP['msg'] ={}
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
                    RESP['msg']['path'] = image_path
                    RESP['msg']['incident_id'] = incident_id
        except Exception as identifier:
            print identifier.message
        finally:
            resp.data = json.dumps(RESP)


