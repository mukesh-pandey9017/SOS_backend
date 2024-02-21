import json
from django.http.response import JsonResponse
from ORSAPI.RestCtl.BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import User
from service.service.RoleService import RoleService
from service.service.UserService import UserService


class UserCtl(BaseCtl):

    def preload(self, request,params={}):
        roleList = RoleService().preload()
        print(roleList)
        preloadList = []
        for roleObj in roleList:
            print(roleObj.to_json())
            preloadList.append(roleObj.to_json())
        print(preloadList)
        return JsonResponse({"preloadList":preloadList})
    
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]
        self.form["confirmpassword"] = requestForm["confirmpassword"]
        self.form["dob"] = requestForm["dob"]
        self.form["gender"] = requestForm["gender"]
        self.form["address"] = requestForm["address"]
        self.form["mobilenumber"] = requestForm["mobilenumber"]
        self.form["role_Id"] = requestForm["role_Id"]
        

    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = "First Name can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "Email Id can not be null"
            self.form["error"] = True
        if(DataValidator.isNotNull(self.form["login_id"])):
            if(DataValidator.isemail(self.form["login_id"])):
                self.form["error"] = True
                inputError["login_id"] = "Email Id must be like abc@gmail.com"
        if(DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["confirmpassword"])):
            inputError["confirmpassword"] = "Password can not be null"
            self.form["error"] = True  
        if(DataValidator.isNotNull(self.form["confirmpassword"])):
            if(self.form["password"] != self.form["confirmpassword"]):
                inputError["confirmpassword"] = "Passwords mismatch"
                self.form["error"] = True
        if(DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "DOB can not be null"
            self.form["error"] = True
        if(DataValidator.isNotNull(self.form["dob"])):
            if(DataValidator.isDate(self.form["dob"])):
                self.form["error"] = True
                inputError["dob"] = "Invalid date of birth"
        if(DataValidator.isNull(self.form["address"])):
            inputError["address"] = "Address can not be null"
            self.form["error"] = True 
        if(DataValidator.isNull(self.form["gender"])):
            inputError["gender"] = "Gender can not be null"
            self.form["error"] = True    
        if(DataValidator.isNull(self.form["mobilenumber"])):
            inputError["mobilenumber"] = "Mobile No. can not be null"
            self.form["error"] = True
        if(DataValidator.isNotNull(self.form["mobilenumber"])):
            if( DataValidator.ismobilecheck(self.form['mobilenumber'])):
                self.form["error"] = True
                inputError["mobilenumber"] = "Enter Correct Mobile No."
        if(DataValidator.isNull(self.form["role_Id"])):
            self.form["error"] = True
            inputError["role_Id"] = "Role name can not be null"
        return self.form["error"]        

    def get(self,request,params):
        userObject = self.get_service().get(params["id"])
        print(userObject)
        res = {}
        if userObject != None:
            data_dict = userObject.to_json()
            res["error"] = False
            res["message"] = ""
        else:
            res["error"] = True
            res["message"] = "No record found"
        return JsonResponse({"data":data_dict,"result":res})
    
    def delete(self,request,params={}):
        userObject = self.get_service().get(params["id"])
        res = {}
        if (userObject != None):
            self.get_service().delete(params["id"])
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
            params["login_id"] = json_request.get("login_id",None)
            params["pageNo"] = json_request.get("pageNo",None)
        userListOfDict = self.get_service().search(params)
        res = {}
        if (userListOfDict["data"] != [] ):
            res["data"] = userListOfDict["data"]
            res["MaxId"] = params["MaxId"]
            res["index"] = params["index"]
            res["LastId"] = User.objects.last().id
            res["error"] = False
            res["mesg"] = ''
        else:
            res["error"] = True
            res["mesg"] = "No record found"
        print("RES_____+__+_+_+_+_= ",res)
        return JsonResponse({"result":res})
    
    def form_to_model(self, obj):
        r = RoleService().get(self.form["role_Id"])
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.login_id = self.form["login_id"]
        obj.password = self.form["password"]
        obj.confirmpassword = self.form["confirmpassword"]
        obj.dob = self.form["dob"]
        obj.gender = self.form["gender"]
        obj.address = self.form["address"]
        obj.mobilenumber = self.form["mobilenumber"]
        obj.role_Id = self.form["role_Id"]
        obj.role_Name = r.name
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
                duplicateUserObj = User.objects.exclude(pk=self.form["id"]).filter(login_id = self.form["login_id"])
                if (duplicateUserObj.count()>0):
                    res["error"] = True
                    res["message"] = "Email Id already exists"
                else:
                    userObj = self.form_to_model(User())
                    self.get_service().save(userObj)
                    res["data"] = userObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Updated successfully"
            else:
                duplicateUserObj = User.objects.filter(login_id = self.form["login_id"])
                if (duplicateUserObj.count()>0):
                    res["error"] = True
                    res["message"] = "Email Id already exists"
                else:
                    userObj = self.form_to_model(User())
                    self.get_service().save(userObj)
                    res["data"] = userObj.to_json()
                    res["error"] = False
                    res["message"] = "Data has been Saved successfully"
        return JsonResponse({"data":res,"form":self.form,})

    def get_service(self):
        return UserService()