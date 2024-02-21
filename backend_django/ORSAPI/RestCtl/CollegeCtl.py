from ORSAPI.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import College
from service.service.CollegeService import CollegeService
from django.http.response import JsonResponse
import json


class CollegeCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form['collegeName'] = requestForm["collegeName"]
        self.form['collegeAddress'] = requestForm['collegeAddress']
        self.form['collegeState'] = requestForm["collegeState"]
        self.form['collegeCity'] = requestForm["collegeCity"]
        self.form['collegePhoneNumber'] = requestForm["collegePhoneNumber"]

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["collegeName"])):
            self.form["error"] = True
            inputError["collegeName"] = "Name can not be null"
        if (DataValidator.isNull(self.form['collegeAddress'])):
            self.form["error"] = True
            inputError["collegeAddress"] = "Address can not be null"
        if (DataValidator.isNull(self.form["collegeState"])):
            self.form["error"] = True
            inputError["collegeState"] = "State can not be null"
        if (DataValidator.isNull(self.form["collegeCity"])):
            self.form["error"] = True
            inputError["collegeCity"] = "City can not be null"
        if (DataValidator.isNull(self.form["collegePhoneNumber"])):
            self.form["error"] = True
            inputError["collegePhoneNumber"] = "Phone Number can not be null"
        if (DataValidator.isNotNull(self.form["collegePhoneNumber"])):
            if(DataValidator.ismobilecheck(self.form["collegePhoneNumber"])):
                self.form["error"] = True
                inputError["collegePhoneNumber"] = "Enter correct phone no"
        return self.form["error"]
    
    def get(self,request,params):
        collegeObject = self.get_service().get(params["id"])
        print(collegeObject)
        res = {}
        if collegeObject != None:
            data_dict = collegeObject.to_json()
            res["error"] = False
            res["message"] = ""
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data":data_dict,"result":res})
    
    def delete(self,request,params={}):
        collegeObject = self.get_service().get(params["id"])
        res = {}
        if (collegeObject != None):
            self.get_service().delete(params["id"])
            res["data"] = collegeObject.to_json()
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
            params["collegeName"] = json_request.get("collegeName",None)
            params["pageNo"] = json_request.get("pageNo",None)
        collegeListOfDict = self.get_service().search(params)
        res = {}
        if (collegeListOfDict["data"] != [] ):
            res["data"] = collegeListOfDict["data"]
            res["MaxId"] = params["MaxId"]
            res["index"] = params["index"]
            res["LastId"] = College.objects.last().id
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
        obj.collegeName = self.form["collegeName"]
        obj.collegeAddress = self.form["collegeAddress"]
        obj.collegeState = self.form["collegeState"]
        obj.collegeCity = self.form["collegeCity"]
        obj.collegePhoneNumber = self.form["collegePhoneNumber"]
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
                duplicateCollegeObj = College.objects.exclude(pk=self.form["id"]).filter(collegeName=self.form['collegeName'])
                if (duplicateCollegeObj.count()>0):
                    res["error"] = True
                    res["message"] = "College Name Already Exists"
                else:
                    collegeObj = self.form_to_model(College())
                    self.get_service().save(collegeObj)
                    res["data"] = collegeObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Updated successfully"
            else:
                duplicateCollegeObj = College.objects.filter(collegeName=self.form['collegeName'])
                if (duplicateCollegeObj.count()>0):
                    res["error"] = True
                    res["message"] = "College Name Already Exists"
                else:
                    collegeObj = self.form_to_model(College())
                    self.get_service().save(collegeObj)
                    res["data"] = collegeObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form,})
    
    # Service of College
    def get_service(self):
        return CollegeService()
    




    

     

