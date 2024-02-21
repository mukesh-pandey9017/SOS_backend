from service.models import Subject
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Subject business logics
'''
class SubjectService(BaseService):
    def get_model(self):
        return Subject

    def search(self,params):
        print("Page No------->",params['pageNo'])
        pageNo = (params['pageNo']-1) * self.pageSize
        sql = "select * from ors_subject where 1=1"
        val  = params.get("subjectName", None)
        if (DataValidator.isNotNull(val)):
            sql += " and subjectName = '"+val+"' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("------------------>",sql,pageNo,self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize)+1
        cursor.execute(sql,[pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id','subjectName','subjectDescription','dob','course_ID')
        res = {
            'data': []
        }
        count = 0
        for x in result:
            print({columnName[i]: x[i] for i,_ in enumerate(x)})
            params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i,_ in enumerate(x)})
        return res



