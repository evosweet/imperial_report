import pymysql
import ConfigParser
import ast
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


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
            con = self.connect()
            sql = self.getConfig('sql')['get_incident']
            incidents = []
            with con.cursor() as cur:
                cur.execute(sql, (params['id'],))
                for rec in cur.fetchall():
                    # incident = {'id': rec[1], 'name': rec[2], 'desc': rec[3], 'email': rec[4], 'person_of_contact': rec[5], 'phone': rec[6], 'address': rec[7], 'website': rec[8]}
                    incident = {'id': rec[0], 'description': rec[1], 'location': rec[2], 'event_type': rec[3], 'dt_reported': str(rec[4]), 'dt_occured': str(rec[5]), 'contact_email': rec[6], 'status': rec[7], 'auth': rec[8], 'auths': [], 'images': []}
                    images = self.get_incident_image(incident)
                    auths = self.get_incident_auth(incident)
                    feedbacks = self.get_feedbacks(incident)
                    incident['images'] = images
                    incident['auths'] = auths
                    incident['feedbacks'] = feedbacks
                    incidents.append(incident)
            return incidents
        except Exception as identifier:
            print identifier, "error"

    def get_incident_event(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['get_incident_by_event']
            incidents = []
            with con.cursor() as cur:
                cur.execute(sql, (params['event_id'],params['status_id'],))
                rows = cur.fetchall()
                for rec in rows:
                    incident = {'id': rec[0], 'description': rec[1], 'location': rec[2], 'event_type': rec[3], 'dt_reported': str(rec[4]), 'dt_occured': str(rec[5]), 'contact_email': rec[6], 'status': rec[7], 'auths': [], 'images': [], 'feedbacks': []}
                    images = self.get_incident_image(incident)
                    auths = self.get_incident_auth(incident)
                    feedbacks = self.get_feedbacks(incident)
                    incident['images'] = images
                    incident['auths'] = auths
                    incident['feedbacks'] = feedbacks
                    incidents.append(incident)
            return incidents
        except Exception as identifier:
            print identifier, "error"

    def get_incident_email(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['get_incident_by_email']
            incidents = []
            with con.cursor() as cur:
                cur.execute(sql, (params['contact_email'],))
                rows = cur.fetchall()
                for rec in rows:
                    incident = {'id': rec[0], 'description': rec[1], 'location': rec[2], 'event_type': rec[3], 'dt_reported': str(rec[4]), 'dt_occured': str(rec[5]), 'contact_email': rec[6], 'status': rec[7], 'auths': [], 'images': [], 'feedbacks':[]}
                    images = self.get_incident_image(incident)
                    auths = self.get_incident_auth(incident)
                    feedbacks = self.get_feedbacks(incident)
                    incident['images'] = images
                    incident['auths'] = auths
                    incident['feedbacks'] = feedbacks
                    incidents.append(incident)
            return incidents
        except Exception as identifier:
            print identifier, "error"

    def get_incident_status(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['get_incident_by_status']
            incidents = []
            with con.cursor() as cur:
                cur.execute(sql, (params['status_id'],))
                rows = cur.fetchall()
                for rec in rows:
                    incident = {'id': rec[0], 'description': rec[1], 'location': rec[2], 'event_type': rec[3], 'dt_reported': str(rec[4]), 'dt_occured': str(rec[5]), 'contact_email': rec[6], 'status': rec[7], 'auths': [], 'images': [], 'feedbacks': []}
                    images = self.get_incident_image(incident)
                    auths = self.get_incident_auth(incident)
                    feedbacks = self.get_feedbacks(incident)
                    incident['images'] = images
                    incident['auths'] = auths
                    incident['feedbacks'] = feedbacks
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
            auths = []
            with con.cursor() as cur:
                cur.execute(sql, (params['id'],))
                for rec in cur.fetchall():
                    auth = {'auth': rec[0], 'auth_id': rec[1]}
                    auths.append(auth)
                return auths
        except Exception as identifier:
            print identifier, "error"

    def update_incident(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['update_incident']
            with con.cursor() as cur:
                out = cur.execute(sql, (params['status_id'], params['id'],))
                con.commit()
            return out
        except Exception as identifier:
            print identifier, "error"
            return 0

    def get_event_email(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['get_event_email']
            emails = []
            with con.cursor() as cur:
                cur.execute(sql, (params['event_id'],))
                rows = cur.fetchall()
                for rec in rows:
                    emails.append(rec[0])
            return emails
        except Exception as identifier:
            print identifier, "error"

    def get_event_by_id(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['get_event_by_id']
            with con.cursor() as cur:
                cur.execute(sql, (params['id'],))
                rows = cur.fetchall()
                for rec in rows:
                    event = rec[1]
            return event
        except Exception as identifier:
            print identifier, "error"

    def add_feedback(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['add_feedback']
            dt = datetime.datetime.now()
            with con.cursor() as cur:
                cur.execute(sql, (params['incident_id'], params['comment'], dt, params['user_id'],))
                feedback_id = con.insert_id()
                con.commit()
            return feedback_id
        except Exception as identifier:
            print identifier, "error"

    def get_feedbacks(self, params):
        try:
            feedbacks = []
            con = self.connect()
            sql = self.getConfig('sql')['get_feedback']
            feedbacks = []
            with con.cursor() as cur:
                cur.execute(sql, (params['id'],))
                for rec in cur.fetchall():
                    feedback = {'id': rec[0], 'incident_id': rec[1], 'comment': rec[2], 'dt': str(rec[3]), 'user': rec[4]}
                    feedbacks.append(feedback)
            return feedbacks
        except Exception as identifier:
            print identifier, "error"

    def hash_pw(self, password):
        return generate_password_hash(password)

    def check_pw(self, password, hashed):
        return check_password_hash(hashed, password)

    def add_user(self, params):
        try:
            params['pw'] = self.hash_pw(params['pw'])
            print params['pw']
            con = self.connect()
            sql = self.getConfig('sql')['add_user']
            params['dt_created'] = datetime.datetime.now()
            print "endling"

            # if 'dt_occured' not in params:
            #     params['dt_occured'] = dt_reported
            # if 'contact_no' not in params:
            #     params['contact_no'] = None
            # if 'path' not in params:
            #     params['path'] = None
            # if 'email' not in params:
            #     params['email'] = None

            with con.cursor() as cur:
                cur.execute(sql, (params['username'], params['pw'], params['level'], params['created_by'], params['dt_created'], params['auth_id'],))
                user_id = con.insert_id()
                con.commit()
            return user_id
        except Exception as identifier:
            print identifier, "error"

    def edit_user(self, params):
        try:
            params['pw'] = self.hash_pw(params['pw'])
            print params['pw']
            con = self.connect()
            sql = self.getConfig('sql')['add_user']
            params['dt_created'] = datetime.datetime.now()
            print "endling"

            # if 'dt_occured' not in params:
            #     params['dt_occured'] = dt_reported
            # if 'contact_no' not in params:
            #     params['contact_no'] = None
            # if 'path' not in params:
            #     params['path'] = None
            # if 'email' not in params:
            #     params['email'] = None

            with con.cursor() as cur:
                cur.execute(sql, (params['username'], params['pw'], params['level'], params['created_by'], params['dt_created'], params['auth_id'],))
                user_id = con.insert_id()
                con.commit()
            return user_id
        except Exception as identifier:
            print identifier, "error"

    def login(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['login']
            with con.cursor() as cur:
                cur.execute(sql, (params['username'],))
                rows = cur.fetchall()
                for rec in rows:
                    pw = rec[0]
            return self.check_pw(params['pw'], pw), rec[1], rec[2]
        except Exception as identifier:
            print identifier, "error"
