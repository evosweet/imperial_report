import falcon,os
from falcon_cors import CORS
from api import Index, SaveIncidentImage,CreateIncident,GetIncidentInfo,GetIncidentByEvent,GetIncidentByAuth

CORZ = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)
API = falcon.API(middleware=[CORZ.middleware])

INDEX = Index()
GETINCIDENT = GetIncidentInfo()
GETINCIDENTEVENT = GetIncidentByEvent()
SAVEIMAGE = SaveIncidentImage(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'incident_images')))
ADDINCIDENT = CreateIncident()
GETINCIDENTAUTH = GetIncidentByAuth()


API.add_route('/', INDEX)
API.add_route('/save_image', SAVEIMAGE)
API.add_route('/make_report', ADDINCIDENT)
API.add_route('/get_incident', GETINCIDENT)
API.add_route('/get_incident_event', GETINCIDENTEVENT)
API.add_route('/get_incident_auth', GETINCIDENTAUTH)


