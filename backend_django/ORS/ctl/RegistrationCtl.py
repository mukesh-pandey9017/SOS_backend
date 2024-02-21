from django.shortcuts import render, redirect
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from ORS.utility.DataValidator import DataValidator
from service.models import User
from service.service.UserService import UserService
from service.service.EmailService import EmailService
from service.service.EmailMessage import EmailMessage



class RegistrationCtl(BaseCtl):
    # Populate Form from Http Request
    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['firstName'] = requestForm['firstName']
        self.form['lastName'] = requestForm['lastName']
        self.form['login_id'] = requestForm['login_id']
        self.form['password'] = requestForm['password']
        self.form['confirmpassword'] = requestForm['confirmpassword']
        self.form['dob'] = requestForm['dob']
        self.form['address'] = requestForm['address']
        self.form['gender'] = requestForm['gender']
        self.form['mobilenumber'] = requestForm['mobilenumber']
        self.form['role_Id'] = 2
        self.form['role_Name'] = 'Student'

    # Convert Form into Module
    def form_to_model(self, obj):
        pk = int(self.form['id'])
        print("-----pk---->>",pk)
        if pk > 0:
            obj.id = pk
        obj.firstName = self.form['firstName']
        obj.lastName = self.form['lastName']
        obj.login_id = self.form['login_id']
        obj.password = self.form['password']
        obj.confirmpassword = self.form['confirmpassword']
        obj.dob = self.form['dob']
        obj.address = self.form['address']
        obj.gender = self.form['gender']
        obj.mobilenumber = self.form['mobilenumber']
        obj.role_Id = self.form['role_Id']
        obj.role_Name = self.form['role_Name']

        return obj

    # Populate Form from model
    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["login_id"] = obj.login_id
        self.form["password"] = obj.password
        self.form["confirmpassword"] = obj.confirmpassword
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d")
        self.form["address"] = obj.address
        self.form["gender"] = obj.gender
        self.form["mobilenumber"] = obj.mobilenumber
        self.form["role_Id"] = 2
        self.form["role_Name"] = "Student"


    # Validate Form
    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if(DataValidator.isNull(self.form['firstName'])):
            inputError['firstName'] = "Name can not be Null"
            self.form['error'] = True
        else:
            if(DataValidator.isalphacheck(self.form['firstName'])):
                inputError['firstName'] = "First Name contains only letters"
                self.form['error'] = True
        
        if(DataValidator.isNull(self.form['lastName'])):
            inputError['lastName'] = "Last Name can not be Null"
            self.form['error'] = True
        else:
            if(DataValidator.isalphacheck(self.form['lastName'])):
                inputError['lastName'] = "Last Name contains only letters"
                self.form['error'] = True

        if(DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "Login Id can not be Null"
            self.form['error'] = True
        else:
            if(DataValidator.isemail(self.form['login_id'])):
                inputError['login_id'] = "Login Id must be like student@gmail.com"
                self.form['error'] = True
        if(DataValidator.isNull(self.form['password'])):
            inputError['password'] = "Password can not be Null"
            self.form['error'] = True
        if(DataValidator.isNull(self.form['confirmpassword'])):
            inputError['confirmpassword'] = "Confirm Password can not be Null"
            self.form['error'] = True
        if(DataValidator.isNotNull(self.form['confirmpassword'])):
            if self.form['password'] != self.form['confirmpassword']:
                inputError['confirmpassword'] = "Password and Confirm Password are not Match"
                self.form['error'] = True

        if(DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "DOB can not be Null"
            self.form['error'] = True
        else:
            if(DataValidator.isDate(self.form['dob'])):
                inputError['dob'] = "Incorrect Date, should be YYYY-MM-DD"
                self.form['error'] = True

        if(DataValidator.isNull(self.form['address'])):
            inputError['address'] = "Address can not be Null"
            self.form['error'] = True
        if(DataValidator.isNull(self.form['gender'])):
            inputError['gender'] = "Gender can not be Null"
            self.form['error'] = True
        if(DataValidator.isNull(self.form['mobilenumber'])):
            inputError['mobilenumber'] = "Mobile No. can not be Null"
            self.form['error'] = True
        else:
            if(DataValidator.ismobilecheck(self.form['mobilenumber'])):
                inputError['mobilenumber'] = "Enter Correct Mobile No."
                self.form['error'] = True

        return self.form['error']


    # Display Role Page
    def display(self, request, params={}):
        res = render(request, self.get_template(), {"form": self.form})
        return res

    # Submit Role Page
    def submit(self, request, params={}):
        q = User.objects.filter()
        q = q.filter(login_id = self.form['login_id'])
        if q.count() > 0 :
            self.form['error'] = True
            self.form['message'] = "Login ID Already Exists"
            res = render(request, self.get_template(), {'form': self.form})
        else:
            emsg = EmailMessage()
            emsg.to = [self.form['login_id']]
            e = {}
            e['login'] = self.form['login_id']
            e['password'] = self.form['password']
            emsg.subject = "ORS Registration Successful"
            mailResponse = EmailService.send(emsg, 'signUp', e)
            if mailResponse == 1:
                r = self.form_to_model(User())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message'] =  'Registered Successfully!!! Please login'
                res = render(request, self.get_template(), {"form": self.form})
            else:
                self.form['error'] = True
                self.form['message'] = "Please Check Your Internet Connection"
                res = render(request, self.get_template(), {'form': self.form})
        return res


    def get_template(self):
        return "Registration.html"

    # Service of Role
    def get_service(self):
        return UserService()