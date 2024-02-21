from django.shortcuts import render,redirect
from service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import User
from service.service.UserService import UserService
from service.service.RoleService import RoleService


class MyProfileCtl(BaseCtl):

    def preload(self, request):
        self.page_list = RoleService().preload()
        self.preloadData = self.page_list


    #populate form from http request
    def request_to_form(self, requestForm):
        self.form["id"]  = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]
        self.form["dob"] = requestForm["dob"]
        self.form["mobilenumber"] = requestForm["mobilenumber"]
        self.form["gender"] = requestForm["gender"]
        self.form['address'] = requestForm['address']

    # Populate Form from model
    def model_to_form(self, obj):
        print("------model_to_form(self, obj):-->>",self, obj)
        if (obj == None):
            return
        self.form["id"]  = obj.id 
        self.form["firstName"] = obj.firstName 
        self.form["lastName"] = obj.lastName 
        self.form["login_id"] = obj.login_id 
        self.form["password"] = obj.password 
        self.form["dob"] = obj.dob
        self.form["mobilenumber"] = obj.mobilenumber
        self.form["gender"] = obj.gender
        self.form['address'] = obj.address

    # Convert form into module
    def form_to_model(self,obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.firstName  = self.form['firstName']
        obj.lastName  = self.form['lastName']
        obj.login_id = self.form['login_id']
        obj.password = self.form['password']
        obj.dob = self.form['dob']
        obj.mobilenumber = self.form['mobilenumber']
        obj.gender = self.form['gender']
        obj.address = self.form['address']

        return obj

    # Validate Form
    def input_validation(self):
        print("------input validation called-->>")
        super().input_validation()
        inputError = self.form['inputError']
        if( DataValidator.isNull(self.form['firstName'])):
            inputError['firstName'] = "First name can not be null"
            self.form['error'] = True
        if( DataValidator.isNull(self.form['lastName'])):
            inputError['lastName'] =  "Last name can not be null"
            self.form['error'] = True
        if(DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "Login can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "dob can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["mobilenumber"])):
            inputError["mobilenumber"] = "mobileNumber can not be null"
            self.form["error"] = True

        return self.form['error']

    # Display Profile page
    def display(self, request, params={}):
        print("------display(self, request, params={}):-->>",self, request, params)
        user = request.session.get('user', None)
        print("------------->>>>>>>>",user)
        if user is not None:
            self.form['username'] = user.login_id
        if( user.id > 0):
            r = self.get_service().get(user.id)
            self.model_to_form(r)
        res = render(request, self.get_template(), {'form': self.form, 'roleList': self.preloadData})
        return res


    # Submit Profile page
    def submit(self, request, params={}):
        print("-------submit called-->>")
        r = self.form_to_model(User())
        self.get_service().save(r)
        self.form['id'] = r.id
        self.form['error'] = False
        self.form['messege'] = "Data is Saved"
        res = render(request, self.get_template(),{'form':self.form})
        return res

    def get_template(self):
        return "MyProfile.html"

    def get_service(self):
        return UserService()

