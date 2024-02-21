import json
from django.http.response import JsonResponse
from .BaseCtl import BaseCtl
from ORSAPI.utility.DataValidator import DataValidator
from service.models import User
from service.service.EmailMessage import EmailMessage
from service.service.EmailService import EmailService


class ForgetPasswordCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["login_id"] = requestForm["login_id"]

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["login_id"])):
            self.form["error"] = True
            inputError["login_id"] = "Login Id can not be null"
        if(DataValidator.isNotNull(self.form["login_id"])):
            if(DataValidator.isemail(self.form["login_id"])):
                self.form["error"] = True
                inputError["login_id"] = "Enter correct Login Id"
        return self.form["error"]
    
    def submit(self,request,params):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        response = {}
        if (self.input_validation()):
            response["error"] = True
            response["message"] = ""
        else:
            q = User.objects.filter(login_id = self.form["login_id"])
            print("forgetpwd--data--->>",q)
            if q.count() > 0:                
                emsg = EmailMessage()
                emsg.to = [self.form["login_id"]]
                emsg.subject = "Forgot Password"
                mailResponse = EmailService.send(emsg,"forgotPassword",q[0])
                if mailResponse == 1:
                    response["error"] = False
                    response["message"] = "Your password has been sent successfully"
                else:
                    response["error"] = True
                    response["message"] = "Please Check Your Internet Connection"
            else:
                response["error"] = True
                response["message"] = "Login Id is Incorrect"
        return JsonResponse({"form":self.form,"data":response})