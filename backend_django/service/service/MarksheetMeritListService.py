from service.models import Marksheet
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Role business logics.   
'''
class MarksheetMeritListService(BaseService):

    def search(self):
        sql="select id,rollNumber,name,physics,chemistry,maths,(physics+chemistry+maths) as total,(physics+chemistry+maths)/3 as percentage from ors_marksheet where physics>32 and chemistry>32 and maths>32 order by percentage desc limit 0,10;"
        cursor = connection.cursor()
        cursor.execute(sql)
        # params['index'] = ((params['pageNo'] - 1) * self.pageSize)+1
        result = cursor.fetchall()
        columnNames=("id","rollNumber","name","physics","chemistry","maths","total","percentage")
        res={
            "data":[]
        }
        for x in result:
            # params['MaxId'] = x[0]
            res['data'].append({columnNames[i] :  x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Marksheet
