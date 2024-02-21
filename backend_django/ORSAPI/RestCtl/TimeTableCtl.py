from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import TimeTable
from service.service.TimeTableService import TimeTableService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from django.http.response import JsonResponse
import json

class TimeTableCtl(BaseCtl):
    def preload(self, request,params={}):
        courseList = CourseService().preload()
        subjectList = SubjectService().preload()
        coursedata = []
        for courseObj in courseList:
            coursedata.append(courseObj.to_json())
        subpreload = []
        for subjectObj in subjectList:
            subpreload.append(subjectObj.to_json())
        return JsonResponse({"subpreload":subpreload,"coupreload":coursedata})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["examTime"] = requestForm["examTime"]
        self.form["examDate"] = requestForm["examDate"]
        self.form["subject_ID"] = requestForm["subject_ID"]
        self.form["course_ID"] = requestForm["course_ID"]
        self.form["semester"] = requestForm["semester"]

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["examTime"])):
            self.form["error"] = True
            inputError["examTime"] = "Time can not be null"
        if(DataValidator.isNull(self.form["examDate"])):
            inputError["examDate"] = "Date can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["subject_ID"])):
            inputError["subject_ID"] = "Subject can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "Course can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["semester"])):
            inputError["semester"] = "Semester can not be null"
            self.form["error"] = True
        return self.form["error"]
    
    def get(self,request,params):
        timeTableObject = self.get_service().get(params["id"])
        print(timeTableObject)
        res = {}
        if timeTableObject != None:
            data_dict = timeTableObject.to_json()
            res["error"] = False
            res["message"] = ""
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data":data_dict,"result":res})
    
    def delete(self,request,params={}):
        timeTableObject = self.get_service().get(params["id"])
        res = {}
        if (timeTableObject != None):
            self.get_service().delete(params["id"])
            res["data"] = timeTableObject.to_json()
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
            params["semester"] = json_request.get("semester",None)
            params["pageNo"] = json_request.get("pageNo",None)
        timeTableListOfDict = self.get_service().search(params)
        res = {}
        if (timeTableListOfDict["data"] != [] ):
            res["data"] = timeTableListOfDict["data"]
            res["MaxId"] = params["MaxId"]
            res["index"] = params["index"]
            res["LastId"] = TimeTable.objects.last().id
            res["error"] = False
            res["mesg"] = ''
        else:
            res["error"] = True
            res["mesg"] = "No record found"
        print("RES_____+__+_+_+_+_= ",res)
        return JsonResponse({"result":res})
    
    def form_to_model(self, obj):
        c = CourseService().get(self.form["course_ID"])
        s = SubjectService().get(self.form["subject_ID"])
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.examTime = self.form["examTime"]
        obj.examDate = self.form["examDate"]
        obj.semester = self.form["semester"]
        obj.subject_ID = self.form["subject_ID"]
        obj.course_ID = self.form["course_ID"]
        obj.subjectName = s.SubjectName
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
                duplicateTimeTableObj = TimeTable.objects.exclude(pk=self.form["id"]).filter(subject_ID=self.form['subject_ID'], examTime=self.form['examTime'], examDate=self.form['examDate'])
                if (duplicateTimeTableObj.count()>0):
                    res["error"] = True
                    res["message"] = "Exam Time, Exam Date, Subject name already exists"
                else:
                    timeTableObj = self.form_to_model(TimeTable())
                    self.get_service().save(timeTableObj)
                    res["data"] = timeTableObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Updated successfully"
            else:
                duplicateTimeTableObj = TimeTable.objects.filter(subject_ID=self.form['subject_ID'], examTime=self.form['examTime'], examDate=self.form['examDate'])
                if (duplicateTimeTableObj.count()>0):
                    res["error"] = True
                    res["message"] = "Exam Time, Exam Date, Subject name already exists"
                else:
                    timeTableObj = self.form_to_model(TimeTable())
                    self.get_service().save(timeTableObj)
                    res["data"] = timeTableObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form,})


    def get_service(self):
        return TimeTableService()

