
import jwt, datetime,ldap, ast,time,falcon,sys
sys.path.append('..')
from db.db import DBUtil


class Auth():
    
    def __init__(self):
        self.db = DBUtil()

    def authenticate(self,token,actionlvl):
        response = {"Allow":0,"res":falcon.HTTP_401}
        try:
            if token is not None:
                payload = jwt.decode(token,'secret')
                print 'here we go',payload
                if payload['auth_level'] >= actionlvl:
                    response ={"Allow":1,"res":falcon.HTTP_200,"level":payload['auth_level'],"user":payload['user']}
                else:
                    response['res'] = falcon.HTTP_403
                    response['msg'] = "Not Authorized! Please contact an admin about gaining access to this feature."
                    response['Result'] = "ERROR"
            else:
                response['res'] = falcon.HTTP_403
                response['msg'] = "Not Authorized! Please contact an admin about gaining access to this feature."
                response['Result'] = "ERROR"
        except Exception as identifier:
            if "expired" in str(identifier):
                response['msg'] = "Your session has expired. Please login and try again."
            elif "verification" in str(identifier):
                response['msg'] = "Not Authenticated"
            else:
                response['msg'] = str(identifier)
            response['Result'] = "ERROR"
        finally:
            return response

    def gettoken(self, req):
        """gets token"""
        token = {'authToken':None}
        isverified, auth_id = self.db.login(req)
        print isverified
        # isverified = {'resp':1}
        if isverified == 1:
            if auth_id == 32:
                user_level = 'admin'
                user_lvl = 2
            else:
                user_level = 'user'
                user_lvl = 1
            token['authToken'] = jwt.encode({'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=28800), 'auth_id':auth_id,'user':req['username'],'auth_level':user_lvl}, 'secret', algorithm='HS256')
            token['user_level'] = user_level
            token['Result'] = 'SUCCESS'
        else:
            token['msg'] = 'INCORRECT PASSWORD or USERNAME'
            token['Result'] = 'ERROR'
        print token
        return token

# auth = CSRAuth()
# req = {'username':'e9900905','password':'Re:Zer_0'}
# print auth.gettoken(req)
# print auth.verifylogin(req)
# db = auth.getConfig('db','csr_db')
# print db,type(db)

# token = jwt.encode({'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=10)},'secret',algorithm='HS256')
# print token
# resp = jwt.decode(token,'secret')
# print resp
# try:
#     resp = jwt.decode('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0NzUwODcxMzR9.NBtHamws64_dPf0MWuHfhE0GoK6W09beNz9dlBY102-','secret')
# except Exception as identifier:
#     print identifier

# time.sleep(11)
# resp = jwt.decode(token,'secret')


	
