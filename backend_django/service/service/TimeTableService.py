from service.models import TimeTable
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains TimeTable business logics
'''


class TimeTableService(BaseService):
    def preload(self, params):
        pass

    def get_model(self):
        return TimeTable

    def search(self, params):
        print("Page No------------>", params['pageNo'])
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from ors_timetable where 1=1"
        val = params.get("semester", None)
        if (DataValidator.isNotNull(val)):
            sql += " and semester = '" + val + "' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("-------------->", sql, pageNo, self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'examTime', 'examDate', 'subject_ID', 'subjectName', 'course_ID', 'courseName', 'semester')
        res = {
            'data': []
        }
        count = 0
        for x in result:
            print({columnName[i]: x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

