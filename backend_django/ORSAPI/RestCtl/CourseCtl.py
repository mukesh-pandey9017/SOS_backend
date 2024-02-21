import json
from django.http.response import JsonResponse
from ORSAPI.RestCtl.BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Course
from service.service.CourseService import CourseService



class CourseCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["courseName"] = requestForm["courseName"]
        self.form["courseDescription"] = requestForm["courseDescription"]
        self.form["courseDuration"] = requestForm["courseDuration"]

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["courseName"])):
            self.form["error"] = True
            inputError["courseName"] = "Name can not be null"
        if (DataValidator.isNull(self.form["courseDescription"])):
            self.form["error"] = True
            inputError["courseDescription"] = "Description can not be null"
        if (DataValidator.isNull(self.form["courseDuration"])):
            self.form["error"] = True
            inputError["courseDuration"] = "Duration can not be null"
        return self.form["error"]

    def get(self,request,params):
        coureObject = self.get_service().get(params["id"])
        print(coureObject)
        res = {}
        if coureObject != None:
            data_dict = coureObject.to_json()
            res["error"] = False
            res["message"] = ""
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data":data_dict,"result":res})
    
    def delete(self,request,params={}):
        courseObject = self.get_service().get(params["id"])
        res = {}
        if (courseObject != None):
            self.get_service().delete(params["id"])
            res["data"] = courseObject.to_json()
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
            params["courseName"] = json_request.get("courseName",None)
            params["pageNo"] = json_request.get("pageNo",None)
        courseListOfDict = self.get_service().search(params)
        res = {}
        if (courseListOfDict["data"] != [] ):
            res["data"] = courseListOfDict["data"]
            res["MaxId"] = params["MaxId"]
            res["index"] = params["index"]
            res["LastId"] = Course.objects.last().id
            res["error"] = False
            res["mesg"] = ''
        else:
            res["error"] = True
            res["mesg"] = "No record found"
        print("RES_____+__+_+_+_+_= ",res)
        return JsonResponse({"result":res})
    
    def form_to_model(self,obj):
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.courseName = self.form["courseName"]
        obj.courseDescription = self.form["courseDescription"]
        obj.courseDuration = self.form["courseDuration"]
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
                duplicateCourseObj = Course.objects.exclude(pk=self.form["id"]).filter(courseName = self.form['courseName'])
                if (duplicateCourseObj.count()>0):
                    res["error"] = True
                    res["message"] = "Course Name Already Exists"
                else:
                    courseObj = self.form_to_model(Course())
                    self.get_service().save(courseObj)
                    res["data"] = courseObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Updated successfully"
            else:
                duplicateCourseObj = Course.objects.filter(courseName = self.form['courseName'])
                if (duplicateCourseObj.count()>0):
                    res["error"] = True
                    res["message"] = "Course Name Already Exists"
                else:
                    courseObj = self.form_to_model(Course())
                    self.get_service().save(courseObj)
                    res["data"] = courseObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form,})
    
    def get_service(self):
        return CourseService()