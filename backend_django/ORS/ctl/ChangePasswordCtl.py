from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from service.utility.DataValidator import DataValidator
from service.models import User
from service.service.ChangePasswordService import ChangePasswordService
from service.service.EmailService import EmailService
from service.service.EmailMessage import EmailMessage

class ChangePasswordCtl(BaseCtl):

    # populate form from Http request
    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['newPassword'] = requestForm['newPassword']
        self.form['oldPassword'] = requestForm['oldPassword']
        self.form['confirmPassword'] = requestForm['confirmPassword']

    # convert form into module
    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.password = self.form['newPassword']
        obj.confirmpassword = self.form['confirmPassword']
        return obj

    # Populate form from model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['newPassword'] = obj.newPassword
        self.form['oldPassword'] = obj.oldPassword
        self.form['confirmPassword'] = obj.confirmPassword

    # Validate Form
    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['oldPassword'])):
            inputError['oldPassword'] = "Old Password can not be Null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['newPassword'])):
            inputError['newPassword'] = "New Password can not be Null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['confirmPassword'])):
            inputError['confirmPassword'] = "Confirm Password can not be Null"
            self.form['error'] = True

        if (self.form['newPassword'] != self.form['confirmPassword']):
            inputError['confirmPassword'] = "Pwd & Confirm Pwd aren't same"
            self.form["error"] = True

        return self.form['error']

    # Display Change Password Page
    def display(self, request, params={}):
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        user = request.session.get('user', None)
        q = User.objects.filter(login_id=user.login_id, password=self.form['oldPassword'])
        if q.count() > 0:
            emsg = EmailMessage()
            emsg.to = [user.login_id]
            emsg.subject = "Password Changed Successfully"
            mailResponse = EmailService.send(emsg, "changePassword", user)
            if mailResponse == 1:
                self.form['id'] = user.id
                r = self.form_to_model(user)
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message'] = "Your password has been changed successfully, Please check your mail"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                self.form['error'] = True
                self.form['message'] = "Please Check Your Internate Connection"
                res = render(request, self.get_template(), {'form': self.form})
        else:
            self.form['error'] = True
            self.form['message'] = "Old Password is Uncorrect"
            res = render(request, self.get_template(), {'form': self.form})
        return res

    def get_template(self):
        return "ChangePassword.html"

    def get_service(self):
        return ChangePasswordService()

