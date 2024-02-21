from service.models import Student
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Student business logics
'''


class StudentService(BaseService):

    def get_model(self):
        return Student

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from ors_student where 1=1"
        val = params.get('firstName', None)
        if (DataValidator.isNotNull(val)):
            sql += " and firstName = '" + val + "' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("---------------->", sql, pageNo, self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'firstName', 'lastName', 'dob', 'mobileNumber', 'email', 'college_ID', 'collegeName')
        res = {
            'data': []
        }
        count = 0
        for x in result:
            # print({columnName[i]: x[i] for i,_ in enumerate(x)})
            params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res



