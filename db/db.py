import pymysql
import ConfigParser
import ast


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
            print "his"
            sql = self.getConfig('sql')['add_incident']

            with con.cursor() as cur:
                print "hi"
                cur.execute(sql, (params['description'], params['location'],
                    params['event_id'], params['dt_reported'], params['dt_occured'], params['contact_email'], params['contact_no'], params['path'], params['statusid'],))
                print con.insert_id
                con.commit()
        except Exception as identifier:
            print identifier,"error"

db = DBUtil()
params = {'description': 'SOMETHING SOMETHING BLAH BLAH BLAH', 'location': 'KINGSTON', 'dt_reported': '2016-11-04 17:24:00', 'event_id': 1}
# print params
db.add_record(params)
