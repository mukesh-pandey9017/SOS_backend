from service.models import College
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

# It Contains College Business Logics

class CollegeService(BaseService):
    def get_model(self):
        return College

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from ORS_COLLEGE where 1=1"
        val = params.get("collegeName",None)
        if DataValidator.isNotNull(val):
            sql += " and collegeName = '"+val+"' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("-----------",sql,pageNo,self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize)+1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'collegeName', 'collegeAddress', 'collegeState', 'collegeCity', 'collegePhoneNumber')
        res = {
            "data" : [],

            "MaxId" : 1
        }
        count = 0
        for x in result:
            res["MaxId"] = params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i,_ in enumerate(x)})
        print("MMMMMMMMMMM",params.get("MaxId"))
        return res








