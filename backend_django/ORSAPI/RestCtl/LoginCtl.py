import json
from django.http.response import JsonResponse
from service.models import User
from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator

class LoginCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["login_id"] = requestForm.get("login_id",None)
        self.form["password"] = requestForm.get("password",None)

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["login_id"])):
            self.form["error"] = True
            inputError["login_id"] = "Login Id can not be null"
        if (DataValidator.isNotNull(self.form["login_id"])):
            if (DataValidator.isemail(self.form["login_id"])):
                self.form["error"] = True
                inputError["login_id"] = "Login Id must be Email"
        if (DataValidator.isNull(self.form["password"])):
            self.form["error"] = True
            inputError["password"] = "Password can not be null"
        return self.form["error"]
    
    def auth(self,request,params):
        print("auth request.body----->>",request.body,"auth params--->>",params)
        json_request = json.loads(request.body)
        self.request_to_form(json_request)

        q = User.objects.filter()

        if self.input_validation():
            self.form["error"] = True
            self.form["message"] = ""
        else:
            if json_request.get("login_id") != None:
                q = q.filter(login_id=self.form.get("login_id"))
            if json_request.get("password") != None:
                q = q.filter(password = json_request.get("password"))
                userList = q
            print("userList---->>",userList)
            if userList.count()>0:
                self.form["error"] = False
                self.form["message"] = "Logged In Successfully"
                request.session["user"] = userList[0]
                data = userList[0].to_json()
                print("json data---->>",data)
                self.form["sessionKey"] = request.session.session_key
                self.form["data"] = data
            else:
                self.form["error"] = True
                self.form["message"] = "Invalid Login Id or Password"
        return JsonResponse({"form":self.form})