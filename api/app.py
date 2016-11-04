import falcon,os
from falcon_cors import CORS
from api import Index, SaveIncidentImage,CreateIncident

CORZ = CORS(allow_all_origins=True, allow_all_methods=True, allow_all_headers=True)
API = falcon.API(middleware=[CORZ.middleware])

INDEX = Index()
SAVEIMAGE = SaveIncidentImage(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'incident_images')))
ADDINCIDENT = CreateIncident()


API.add_route('/', INDEX)
API.add_route('/save_image', SAVEIMAGE)
API.add_route('/make_report', ADDINCIDENT)

