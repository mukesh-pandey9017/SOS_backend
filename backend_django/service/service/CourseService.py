from service.models import Course
from service.utility.DataValidator import DataValidator
from.BaseService import BaseService
from django.db import connection

# It contains course business logics

class CourseService(BaseService):
    def get_model(self):
        return Course

    def search(self, params):
        pageNo = (params['pageNo']-1) * self.pageSize
        sql = 'select * from ORS_COURSE where 1=1'
        val = params.get("courseName", None)
        if DataValidator.isNotNull(val):
            sql += " and courseName = '"+val+"' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        result = cursor.fetchall()
        columnName = ('id', 'courseName', 'courseDescription', 'courseDuration')
        res = {
            "data": []
        }
        for x in result:
            print({columnName[i]: x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res
