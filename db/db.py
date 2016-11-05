import pymysql
import ConfigParser
import ast
import datetime


class DBUtil():
    def __init__(self):
        pass

    def getConfig(self, section, value=None):
        if value is None:
            value = section
        config = ConfigParser.RawConfigParser()
        config.read("app.cfg")
        return ast.literal_eval(config.get(section, value))

    def connect(self):
        try:
            con = pymysql.connect(**self.getConfig('db', 'db'))
            return con
        except Exception as identifier:
            pass

    def add_incident(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['add_incident']
            dt_reported = datetime.datetime.now()

            if 'dt_occured' not in params:
                params['dt_occured'] = dt_reported
            if 'contact_no' not in params:
                params['contact_no'] = None
            if 'path' not in params:
                params['path'] = None
            if 'email' not in params:
                params['email'] = None

            with con.cursor() as cur:
                cur.execute(sql, (params['description'], params['location'],
                    params['event_id'], dt_reported, params['dt_occured'], params['email'], params['contact_no'],))
                incident_id = con.insert_id()
                con.commit()
            return incident_id
        except Exception as identifier:
            print identifier, "error"

    def get_incident(self, params):
        try:
            images = []
            images = self.get_incident_image(params)
            con = self.connect()
            sql = self.getConfig('sql')['get_incident']
            incidents = []
            with con.cursor() as cur:
                cur.execute(sql, (params['id'],))
                for rec in cur.fetchall():
                    # incident = {'id': rec[1], 'name': rec[2], 'desc': rec[3], 'email': rec[4], 'person_of_contact': rec[5], 'phone': rec[6], 'address': rec[7], 'website': rec[8]}
                    incident = {'id': rec[0], 'description': rec[1], 'location': rec[2], 'dt_reported': str(rec[3]), 'event_id': rec[4], 'dt_occured': str(rec[5]), 'contact_email': rec[6], 'contact_no': rec[7], 'has_image': rec[8], 'status_id': rec[9], 'images':images}
                    incidents.append(incident)
            return incidents
        except Exception as identifier:
            print identifier, "error"

    def get_incident_event(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['get_incident_event']
            incidents = []
            with con.cursor() as cur:
                cur.execute(sql, (params['event_id'],))
                rows = cur.fetchall()
                for rec in rows:
                    incident = {'id': rec[0], 'description': rec[1], 'location': rec[2], 'dt_reported': str(rec[3]), 'event_id': rec[4], 'dt_occured': str(rec[5]), 'contact_email': rec[6], 'contact_no': rec[7], 'has_image': rec[8], 'status_id': rec[9]}
                    incidents.append(incident)
            return incidents
        except Exception as identifier:
            print identifier, "error"

    def get_incident_status(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['get_incident_status']
            incidents = []
            with con.cursor() as cur:
                cur.execute(sql, (params['status_id'],))
                rows = cur.fetchall()
                for rec in rows:
                    incident = {'id': rec[0], 'description': rec[1], 'location': rec[2], 'dt_reported': str(rec[3]), 'event_id': rec[4], 'dt_occured': str(rec[5]), 'contact_email': rec[6], 'contact_no': rec[7], 'has_image': rec[8], 'status_id': rec[9]}
                    incidents.append(incident)
            return incidents
        except Exception as identifier:
            print identifier, "error"

    def add_incident_image(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['add_incident_image']

            with con.cursor() as cur:
                cur.execute(sql, (params['incident_id'], params['image_path'],))
                out = con.insert_id()
                con.commit()
        except Exception as identifier:
            print identifier, "error"

    def get_incident_image(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['get_incident_image']
            images = []
            with con.cursor() as cur:
                cur.execute(sql, (params['id'],))
                rows = cur.fetchall()
                for rec in rows:
                    image = {'id': rec[0], 'incident_id': rec[1], 'image_path': rec[2]}
                    images.append(image)
            return images
        except Exception as identifier:
            print identifier, "error"

    def get_incident_auth(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['get_incident_auth']
            incidents = []
            with con.cursor() as cur:
                cur.execute(sql, (params['authority_id'],))
                for rec in cur.fetchall():
                    incident = {'incident_id': rec[0], 'description': rec[1], 'location': rec[2], 'event_type': rec[3], 'dt_reported': str(rec[4]), 'dt_occured': str(rec[5]), 'contact_email': rec[6], 'status_id': rec[7], 'auth_name': rec[8]}
                    incidents.append(incident)
                return incidents
        except Exception as identifier:
            print identifier, "error"
