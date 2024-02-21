from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Subject
from service.service.SubjectService import SubjectService
from service.service.CourseService import CourseService
from django.http.response import JsonResponse
import json

class SubjectCtl(BaseCtl):
    def preload(self, request,params={}):
        courseList = CourseService().preload()
        preloadList = []
        for courseObj in courseList:
            preloadList.append(courseObj.to_json())
        return JsonResponse({"preloadList":preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["subjectName"] = requestForm["subjectName"]
        self.form["subjectDescription"] = requestForm["subjectDescription"]
        self.form["course_ID"] = requestForm["course_ID"]

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["subjectName"])):
            self.form["error"] = True
            inputError["subjectName"] = "Name can not be null"
        if(DataValidator.isNull(self.form["subjectDescription"])):
            inputError["subjectDescription"] = "Description can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "Course can not be null"
            self.form["error"] = True
        return self.form["error"]
    
    def get(self,request,params):
        subjectObject = self.get_service().get(params["id"])
        print(subjectObject)
        res = {}
        if subjectObject != None:
            data_dict = subjectObject.to_json()
            res["error"] = False
            res["message"] = ""
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data":data_dict,"result":res})
    
    def delete(self,request,params={}):
        subjectObject = self.get_service().get(params["id"])
        res = {}
        if (subjectObject != None):
            self.get_service().delete(params["id"])
            res["data"] = subjectObject.to_json()
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
            params["subjectName"] = json_request.get("subjectName",None)
            params["pageNo"] = json_request.get("pageNo",None)
        subjectListOfDict = self.get_service().search(params)
        res = {}
        if (subjectListOfDict["data"] != [] ):
            res["data"] = subjectListOfDict["data"]
            res["MaxId"] = params["MaxId"]
            res["index"] = params["index"]
            res["LastId"] = Subject.objects.last().id
            res["error"] = False
            res["mesg"] = ''
        else:
            res["error"] = True
            res["mesg"] = "No record found"
        print("RES_____+__+_+_+_+_= ",res)
        return JsonResponse({"result":res})

    def form_to_model(self, obj):
        c = CourseService().get(self.form["course_ID"])
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.SubjectName = self.form["subjectName"]
        obj.SubjectDescription = self.form["subjectDescription"]
        obj.Course_ID = self.form["course_ID"]
        obj.courseName = c.courseName
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
                duplicateSubjectObj = Subject.objects.exclude(pk=self.form["id"]).filter(SubjectName = self.form['subjectName'])
                if (duplicateSubjectObj.count()>0):
                    res["error"] = True
                    res["message"] = "Subject Name already exists"
                else:
                    subjectObj = self.form_to_model(Subject())
                    self.get_service().save(subjectObj)
                    res["data"] = subjectObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Updated successfully"
            else:
                duplicateSubjectObj = Subject.objects.filter(SubjectName = self.form['subjectName'])
                if (duplicateSubjectObj.count()>0):
                    res["error"] = True
                    res["message"] = "Subject Name already exists"
                else:
                    subjectObj = self.form_to_model(Subject())
                    self.get_service().save(subjectObj)
                    res["data"] = subjectObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form,})


    def get_service(self):
        return SubjectService()