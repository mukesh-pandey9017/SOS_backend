from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Role
from service.service.RoleService import RoleService
from django.http.response import JsonResponse
import json

class RoleCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["name"] = requestForm["name"]
        self.form["description"] = requestForm["description"]
    
    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["name"])):
            self.form["error"] = True
            inputError["name"] = "Name can not be null" 
        if (DataValidator.isNull(self.form["description"])):
            self.form["error"] = True
            inputError["description"] = "Description can not be null"
        return self.form["error"]
    
    def get(self,request,params):
        roleObject = self.get_service().get(params["id"])
        print(roleObject)
        res = {}
        if roleObject != None:
            data_dict = roleObject.to_json()
            res["error"] = False
            res["message"] = ""
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data":data_dict,"result":res})
    
    
    def delete(self,request,params={}):
        roleObject = self.get_service().get(params["id"])
        res = {}
        if (roleObject != None):
            self.get_service().delete(params["id"])
            res["data"] = roleObject.to_json()
            res["error"] = False
            res["message"] = "Data has been deleted successfully"
        else:
            res["error"] = True
            res["message"] = "Data was not deleted"
        return JsonResponse({"data":res})
    
    def search(self,request,params={}):
        json_request = json.loads(request.body)
        print("json_request_data----->>",json_request)
        if (json_request):
            params["name"] = json_request.get("name",None)
            params["pageNo"] = json_request.get("pageNo",None)
        roleListOfDict = self.get_service().search(params)
        res = {}
        if (roleListOfDict["data"] != [] ):
            res["data"] = roleListOfDict["data"]
            res["MaxId"] = params["MaxId"]
            res["index"] = params["index"]
            res["LastId"] = Role.objects.last().id
            res["error"] = False
            res["mesg"] = ''
        else:
            res["error"] = True
            res["mesg"] = "No record found"
        print("RES_____+__+_+_+_+_= ",res)
        return JsonResponse({"result":res})
    
    def form_to_model(self, obj):
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.name = self.form["name"]
        obj.description = self.form["description"]
        return obj

    def save(self,request, params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {}
        if (self.input_validation()):
            res["error"] = True
            res["message"] = ""
        else:
            if (self.form["id"]>0):
                duplicateRoleObj = Role.objects.exclude(pk=self.form["id"]).filter(name__iexact = str(self.form['name']))
                if (duplicateRoleObj.count()>0):
                    res["error"] = True
                    res["message"] = "Role Name already exists"
                else:
                    roleObj = self.form_to_model(Role())
                    self.get_service().save(roleObj)
                    res["data"] = roleObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Updated successfully"
            else:
                duplicateRoleObj = Role.objects.filter(name__iexact = str(self.form['name']))
                if (duplicateRoleObj.count()>0):
                    res["error"] = True
                    res["message"] = "Role Name already exists"
                else:
                    roleObj = self.form_to_model(Role())
                    self.get_service().save(roleObj)
                    res["data"] = roleObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form,})


    def get_service(self):
        return RoleService()