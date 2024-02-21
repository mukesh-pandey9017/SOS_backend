import json

from django.http.response import JsonResponse
from service.models import User
from .BaseCtl import BaseCtl


class MyProfileCtl(BaseCtl):

    def get(self,request,params={}):
        json_request = json.loads(request.body)
        print("json_request_data----->>",json_request)
        UserObjList = User.objects.filter(login_id = json_request["login_id"], firstName = json_request["firstName"])
        res = {}
        userDict = {}
        if UserObjList.count()>0:
            userDict = UserObjList[0].to_json()
            res["error"] = False
            res["message"] = ""
        else:
            res["error"] = True
            res["message"] = "OOPs try after some time"
        return JsonResponse({"data":userDict,"result":res})
        