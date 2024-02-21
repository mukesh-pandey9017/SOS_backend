from collections import UserList
from service.models import User
from service.utility.DataValidator import DataValidator
from.BaseService import BaseService

# It contains user business logics.

class ChangePasswordService(BaseService):
    def authenticate(self,params):
        userList = self.search(params)
        if (userList.count() > 0 ):
            print('88888888->',userList[0].login_id)
            return userList[0]
        else:
            return None

    def get_model(self):
        return User
