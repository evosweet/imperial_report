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

    def add_record(self, params):
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
                    params['event_id'], dt_reported, params['dt_occured'], params['email'], params['contact_no'], params['path'],))
                con.commit()
                return con.insert_id()
        except Exception as identifier:
            print identifier,"error"

db = DBUtil()
params = {'description': 'SOMETHING SOMETHING BLAH BLAH BLAH', 'location': 'KINGSTON', 'dt_reported': '2016-11-04 17:24:00', 'email':'email@mail.com', 'event_id': 1}
# print params
db.add_record(params)
