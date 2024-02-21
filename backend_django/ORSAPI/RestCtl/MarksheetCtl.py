from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Marksheet
from service.service.MarksheetService import MarksheetService
from service.service.MarksheetMeritListService import MarksheetMeritListService
from django.http.response import JsonResponse
import json

class MarksheetCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["rollNumber"] = requestForm["rollNumber"]
        self.form["name"] = requestForm["name"]
        self.form["physics"] = requestForm["physics"]
        self.form["chemistry"] = requestForm["chemistry"]
        self.form["maths"] = requestForm["maths"]

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["rollNumber"])):
            self.form["error"] = True
            inputError["rollNumber"] = "Roll No can not be null"
        if (DataValidator.isNotNull(self.form["rollNumber"])):
            if (DataValidator.ischeckroll(self.form["rollNumber"])):
                self.form["error"] = True
                inputError["rollNumber"] = "Enter correct roll no"
        if (DataValidator.isNull(self.form["name"])):
            self.form["error"] = True
            inputError["name"] = "Name can not be null"
        if (DataValidator.isNull(self.form["physics"])):
            self.form["error"] = True
            inputError["physics"] = "Physics can not be null"
        if (DataValidator.isNotNull(self.form["physics"])):
            if (DataValidator.ischeck(self.form["physics"])):
                self.form["error"] = True
                inputError["physics"] = "Enter correct marks"
        if (DataValidator.isNull(self.form["chemistry"])):
            self.form["error"] = True
            inputError["chemistry"] = "Chemistry can not be null"
        if (DataValidator.isNotNull(self.form["chemistry"])):
            if (DataValidator.ischeck(self.form["chemistry"])):
                self.form["error"] = True
                inputError["chemistry"] = "Enter correct marks"
        if (DataValidator.isNull(self.form["maths"])):
            self.form["error"] = True
            inputError["maths"] = "Maths can not be null"
        if (DataValidator.isNotNull(self.form["maths"])):
            if (DataValidator.ischeck(self.form["maths"])):
                self.form["error"] = True
                inputError["maths"] = "Enter correct marks"
        return self.form["error"]
    
    def get(self,request,params):
        marksheetObject = self.get_service().get(params["id"])
        print(marksheetObject)
        res = {}
        if marksheetObject != None:
            data_dict = marksheetObject.to_json()
            res["error"] = False
            res["message"] = ""
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data":data_dict,"result":res})
    
    def delete(self,request,params={}):
        matksheetObject = self.get_service().get(params["id"])
        res = {}
        if (matksheetObject != None):
            self.get_service().delete(params["id"])
            res["data"] = matksheetObject.to_json()
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
            params["rollNumber"] = json_request.get("rollNumber",None)
            params["pageNo"] = json_request.get("pageNo",None)
        marksheetListOfDict = self.get_service().search(params)
        res = {}
        if (marksheetListOfDict["data"] != [] ):
            res["data"] = marksheetListOfDict["data"]
            res["MaxId"] = params["MaxId"]
            res["index"] = params["index"]
            res["LastId"] = Marksheet.objects.last().id
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
        obj.rollNumber = self.form["rollNumber"]
        obj.name = self.form["name"]
        obj.physics = self.form["physics"]
        obj.chemistry = self.form["chemistry"]
        obj.maths = self.form["maths"]
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
                duplicateMarksheetObj = Marksheet.objects.exclude(pk=self.form["id"]).filter(rollNumber = self.form['rollNumber'])
                if (duplicateMarksheetObj.count()>0):
                    res["error"] = True
                    res["message"] = "Roll Number already exists"
                else:
                    marksheetObj = self.form_to_model(Marksheet())
                    self.get_service().save(marksheetObj)
                    res["data"] = marksheetObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Updated successfully"
            else:
                duplicateMarksheetObj = Marksheet.objects.filter(rollNumber = self.form['rollNumber'])
                if (duplicateMarksheetObj.count()>0):
                    res["error"] = True
                    res["message"] = "Roll Number already exists"
                else:
                    marksheetObj = self.form_to_model(Marksheet())
                    self.get_service().save(marksheetObj)
                    res["data"] = marksheetObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form,})
    
    def meritlist(self,request,params):
        record = MarksheetMeritListService().search()
        data = record['data']
        if record == []:
            self.form['msg'] = 'No record found'
        return JsonResponse({"data":data})

    def get_service(self):
        return MarksheetService()
