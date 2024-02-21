from service.models import Role
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

# it contains Role Business logics

class RoleService(BaseService):
    def search(self,params):
        print('Page No -->',params['pageNo'])
        pageNo = (params['pageNo']-1)*self.pageSize
        sql = 'select * from ORS_ROLE where 1=1'
        val = params.get('name',None)
        if (DataValidator.isNotNull(val)):
            sql += " and name ='"+val+"' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("--------------->",sql,pageNo,self.pageSize)
        params['index'] = ((params['pageNo'] - 1 )* self.pageSize)+1
        cursor.execute(sql,[pageNo,self.pageSize])
        result = cursor.fetchall()
        columName = ('id','name','description')
        res = {
            "data":[]
        }
        count = 0
        for x in result:
            print({columName[i] : x[i] for i,_ in enumerate(x)})
            params['MaxId'] = x[0]
            res['data'].append({columName[i] : x[i] for i,_ in enumerate(x)})
        return res

    def get_model(self):
        return Role