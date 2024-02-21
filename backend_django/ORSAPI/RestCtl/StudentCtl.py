from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Student
from service.service.StudentService import StudentService
from service.service.CollegeService import CollegeService
from django.http.response import JsonResponse
import json


class StudentCtl(BaseCtl):
    def preload(self, request,params={}):
        collegeList = CollegeService().preload()
        preloadList = []
        for collegeObj in collegeList:
            preloadList.append(collegeObj.to_json())
        return JsonResponse({"preloadList":preloadList})

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["dob"] = requestForm["dob"]
        self.form["mobileNumber"] = requestForm["mobileNumber"]
        self.form["email"] = requestForm["email"]
        self.form["college_ID"] = requestForm["college_ID"]

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            self.form["error"] = True
            inputError["firstName"] = "First Name can not be null"
        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "DOB can not be null"
            self.form["error"] = True 
        if(DataValidator.isNotNull(self.form["dob"])):
            if(DataValidator.isDate(self.form["dob"])):
                self.form["error"] = True
                inputError["dob"] = "Invalid date of birth"
        if(DataValidator.isNull(self.form["mobileNumber"])):
            inputError["mobileNumber"] = "Mobile No can not be null"
            self.form["error"] = True
        if(DataValidator.isNotNull(self.form["mobileNumber"])):
            if( DataValidator.ismobilecheck(self.form['mobileNumber'])):
                self.form["error"] = True
                inputError["mobileNumber"] = "Enter Correct Mobile No."
        if(DataValidator.isNull(self.form["email"])):
            inputError["email"] = "Email can not be null"
            self.form["error"] = True
        if(DataValidator.isNotNull(self.form["email"])):
            if(DataValidator.isemail(self.form["email"])):
                self.form["error"] = True
                inputError["email"] = "Email Id must be like abc@gmail.com"
        if(DataValidator.isNull(self.form["college_ID"])):
            inputError["college_ID"] = "College Name can not be null"
            self.form["error"] = True
        return self.form["error"]
    
    def get(self,request,params):
        studentObject = self.get_service().get(params["id"])
        print(studentObject)
        res = {}
        if studentObject != None:
            data_dict = studentObject.to_json()
            res["error"] = False
            res["message"] = ""
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data":data_dict,"result":res})
    
    def delete(self,request,params={}):
        studentObject = self.get_service().get(params["id"])
        res = {}
        if (studentObject != None):
            self.get_service().delete(params["id"])
            res["data"] = studentObject.to_json()
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
        studentListOfDict = self.get_service().search(params)
        res = {}
        if (studentListOfDict["data"] != [] ):
            res["data"] = studentListOfDict["data"]
            res["MaxId"] = params["MaxId"]
            res["index"] = params["index"]
            res["LastId"] = Student.objects.last().id
            res["error"] = False
            res["mesg"] = ''
        else:
            res["error"] = True
            res["mesg"] = "No record found"
        print("RES_____+__+_+_+_+_= ",res)
        return JsonResponse({"result":res})
    
    def form_to_model(self, obj):
        c = CollegeService().get(self.form["college_ID"])
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.dob = self.form["dob"]
        obj.mobileNumber = self.form["mobileNumber"]
        obj.email = self.form["email"]
        obj.college_ID = self.form["college_ID"]
        obj.collegeName = c.collegeName
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
                duplicateStudentObj = Student.objects.exclude(pk=self.form["id"]).filter(email = self.form['email'])
                if (duplicateStudentObj.count()>0):
                    res["error"] = True
                    res["message"] = "Email Id already exists"
                else:
                    studentObj = self.form_to_model(Student())
                    self.get_service().save(studentObj)
                    res["data"] = studentObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Updated successfully"
            else:
                duplicateStudentObj = Student.objects.filter(email = self.form['email'])
                if (duplicateStudentObj.count()>0):
                    res["error"] = True
                    res["message"] = "Email Id already exists"
                else:
                    studentObj = self.form_to_model(Student())
                    self.get_service().save(studentObj)
                    res["data"] = studentObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form,})


    def get_service(self):
        return StudentService()


