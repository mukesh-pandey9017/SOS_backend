from service.service.EmailMessage import EmailMessage
import json
from django.http.response import JsonResponse
from ORSAPI.utility.DataValidator import DataValidator
from service.models import User
from service.service.EmailService import EmailService
from service.service.UserService import UserService
from .BaseCtl import BaseCtl


class RegistrationCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]
        self.form["confirmpassword"] = requestForm["confirmpassword"]
        self.form["dob"] = requestForm["dob"]
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["mobilenumber"] = requestForm["mobilenumber"]
        self.form["role_Id"] = 2
        self.form["role_Name"] = "Student"

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
        return self.form["error"]         

    def form_to_model(self, obj):
        pk = int(self.form["id"])
        if (pk>0):
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.login_id = self.form["login_id"]
        obj.password = self.form["password"] 
        obj.confirmpassword = self.form["confirmpassword"]
        obj.dob = self.form["dob"]
        obj.address = self.form["address"]
        obj.gender = self.form["gender"]
        obj.mobilenumber = self.form["mobilenumber"]
        obj.role_Id  = self.form["role_Id"]
        obj.role_Name = self.form["role_Name"]
        return obj
    
    def save(self,request,params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request) 
        res = {}

        if (self.input_validation()):
            res["error"] = True
            res["message"] = ""
        else:
            user = User.objects.filter(login_id = self.form["login_id"])
            if (user.count()>0):
                res["error"] = True
                res["message"] = "Email Id already exists"
            else:
                emsg = EmailMessage()
                emsg.to = [self.form["login_id"]]
                emsg.subject = "Registraion Successful"
                e = {}
                e["login"] = self.form["login_id"]
                e["password"] = self.form["password"]
                mailResponse = EmailService.send(emsg,"signUp",e)
                if mailResponse == 1:
                    usrObj = self.form_to_model(User())
                    self.get_service().save(usrObj)
                    res["data"] = usrObj.to_json()
                    res["error"] = False
                    res["message"] = "Registered Successfully!!! Please login"
                else:
                    res["error"] = True
                    res["message"] = "Please Check Your Internet Connection"
        return JsonResponse({"form":self.form,"data":res})

    def get_service(self):
        return UserService()