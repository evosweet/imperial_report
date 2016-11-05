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
                out =  con.insert_id()
                con.commit()
            print out
        except Exception as identifier:
            print identifier,"error"

    def get_incident(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['get_incident']

            with con.cursor() as cur:
                cur.execute(sql, (params['id'],))
                for rec in cur.fetchall():
                    print rec
        except Exception as identifier:
            print identifier,"error"

    def get_incident_event(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['get_incident']

            with con.cursor() as cur:
                cur.execute(sql, (params['event_id'],))
                for rec in cur.fetchall():
                    print rec
        except Exception as identifier:
            print identifier,"error"

    def get_incident_status(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['get_incident']

            with con.cursor() as cur:
                cur.execute(sql, (params['status_id'],))
                for rec in cur.fetchall():
                    print rec
        except Exception as identifier:
            print identifier,"error"


    def add_incident_image(self, params):
        try:
            con = self.connect()
            sql = self.getConfig('sql')['add_incident_image']

            with con.cursor() as cur:
                cur.execute(sql, (params['incident_id'],params['image_path'],))
                out =  con.insert_id()
                con.commit()
            print out
        except Exception as identifier:
            print identifier,"error"

# db = DBUtil()
# params = {'description': 'SOMETHING SOMETHING BLAH BLAH BLAH', 'location': 'KINGSTON', 'dt_reported': '2016-11-04 17:24:00', 'email':'email@mail.com', 'event_id': 1}
# # print params
# # params = {'event_id':'1'}
# params = {'incident_id':'1', 'image_path':'/image.png'}
# db.add_incident_image(params)
# # db.get_incident_event(params)
