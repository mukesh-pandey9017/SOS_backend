from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService
from service.service.FacultyService import FacultyService
from service.service.SubjectService import SubjectService
from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Faculty
from django.http.response import JsonResponse
import json

class FacultyCtl(BaseCtl):

    def preload(self, request,params={}):
        print("This is Preload")
        courseList = CourseService().preload()
        subjectList = SubjectService().preload()
        collegeList = CollegeService().preload()
        coursedata = []
        for courseObj in courseList:
            coursedata.append(courseObj.to_json())
        subjectdata = []
        for subjectObj in subjectList:
            subjectdata.append(subjectObj.to_json())
        collegedata = []
        for collegeObj in collegeList:
            collegedata.append(collegeObj.to_json())
        return JsonResponse({"subpreload":subjectdata,"coupreload":coursedata,"colpreload":collegedata})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["email"] = requestForm["email"]
        self.form["password"] = requestForm["password"]
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["dob"] = requestForm["dob"]
        self.form["college_ID"] = requestForm["college_ID"]
        self.form["subject_ID"] = requestForm["subject_ID"]
        self.form["course_ID"] = requestForm["course_ID"]

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            self.form["error"] = True
            inputError["firstName"] = "First Name can not be null"
        if (DataValidator.isNull(self.form["lastName"])):
            self.form["error"] = True
            inputError["lastName"] = "Last Name can not be null"
        if (DataValidator.isNull(self.form["email"])):
            self.form["error"] = True
            inputError["email"] = "Email can not be null"
        if(DataValidator.isNotNull(self.form["email"])):
            if(DataValidator.isemail(self.form["email"])):
                self.form["error"] = True
                inputError["email"] = "Email Id must be like abc@gmail.com"
        if (DataValidator.isNull(self.form["password"])):
            self.form["error"] = True
            inputError["password"] = "Password can not be null"
        if (DataValidator.isNull(self.form["address"])):
            self.form["error"] = True
            inputError["address"] = "Address can not be null"
        if (DataValidator.isNull(self.form["gender"])):
            self.form["error"] = True
            inputError["gender"] = "Gender can not be null"
        if (DataValidator.isNull(self.form["dob"])):
            self.form["error"] = True
            inputError["dob"] = "Date of Birth can not be null"
        if(DataValidator.isNotNull(self.form["dob"])):
            if(DataValidator.isDate(self.form["dob"])):
                self.form["error"] = True
                inputError["dob"] = "Invalid date of birth "
        if (DataValidator.isNull(self.form["college_ID"])):
            self.form["error"] = True
            inputError["college_ID"] = "College can not be null"            
        if (DataValidator.isNull(self.form["subject_ID"])):
            self.form["error"] = True
            inputError["subject_ID"] = "Subject can not be null"
        if (DataValidator.isNull(self.form["course_ID"])):
            self.form["error"] = True
            inputError["course_ID"] = "Course can not be null"
        return self.form["error"]
    
    def get(self,request,params):
        facultyObject = self.get_service().get(params["id"])
        print(facultyObject)
        res = {}
        if facultyObject != None:
            data_dict = facultyObject.to_json()
            res["error"] = False
            res["message"] = ""
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data":data_dict,"result":res})
    
    def delete(self,request,params={}):
        facultyObject = self.get_service().get(params["id"])
        res = {}
        if (facultyObject != None):
            self.get_service().delete(params["id"])
            res["data"] = facultyObject.to_json()
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
            params["firstName"] = json_request.get("firstName",None)
            params["pageNo"] = json_request.get("pageNo",None)
        facultyListOfDict = self.get_service().search(params)
        res = {}
        if (facultyListOfDict["data"] != [] ):
            res["data"] = facultyListOfDict["data"]
            res["MaxId"] = params["MaxId"]
            res["index"] = params["index"]
            res["LastId"] = Faculty.objects.last().id
            res["error"] = False
            res["mesg"] = ''
        else:
            res["error"] = True
            res["mesg"] = "No record found"
        print("RES_____+__+_+_+_+_= ",res)
        return JsonResponse({"result":res})
    
    def form_to_model(self, obj):
        col = CollegeService().get(self.form["college_ID"])
        cou = CourseService().get(self.form["course_ID"])
        sub = SubjectService().get(self.form["subject_ID"])
        print("error",sub.SubjectName)
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.email = self.form["email"]
        obj.password = self.form["password"]
        obj.address = self.form["address"]
        obj.gender = self.form["gender"]
        obj.dob = self.form["dob"]
        obj.college_ID = self.form["college_ID"]
        obj.course_ID = self.form["course_ID"]
        obj.subject_ID = self.form["subject_ID"]
        obj.collegeName = col.collegeName
        obj.courseName = cou.courseName
        obj.subjectName = sub.SubjectName
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
                duplicateFacultyObj = Faculty.objects.exclude(pk=self.form["id"]).filter(email=self.form['email'])
                if (duplicateFacultyObj.count()>0):
                    res["error"] = True
                    res["message"] = "Email Id already exists"
                else:
                    facultyObj = self.form_to_model(Faculty())
                    self.get_service().save(facultyObj)
                    res["data"] = facultyObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Updated successfully"
            else:
                duplicateFacultyObj = Faculty.objects.filter(email=self.form['email'])
                if (duplicateFacultyObj.count()>0):
                    res["error"] = True
                    res["message"] = "Email Id already exists"
                else:
                    facultyObj = self.form_to_model(Faculty())
                    self.get_service().save(facultyObj)
                    res["data"] = facultyObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form,})
    
    def get_service(self):
        return FacultyService()