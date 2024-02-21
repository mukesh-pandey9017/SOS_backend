from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from service.models import College
from service.service.CollegeService import CollegeService



class CollegeCtl(BaseCtl):

    #populate form from request
    def request_to_form(self, requestForm):
        self.form['id']  =  requestForm['id']
        self.form['collegeName'] = requestForm['collegeName']
        self.form['collegeAddress'] = requestForm['collegeAddress']
        self.form['collegeState']  = requestForm['collegeState']
        self.form['collegeCity'] = requestForm['collegeCity']
        self.form['collegePhoneNumber'] = requestForm['collegePhoneNumber']

    
    #convert form into model
    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.collegeName = self.form['collegeName']
        obj.collegeAddress = self.form['collegeAddress']
        obj.collegeState = self.form['collegeState']
        obj.collegeCity = self.form['collegeCity']
        obj.collegePhoneNumber = self.form['collegePhoneNumber']
        return obj
    
    #populate form form model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['collegeName'] = obj.collegeName
        self.form['collegeAddress'] = obj.collegeAddress
        self.form['collegeState'] = obj.collegeState
        self.form['collegeCity'] = obj.collegeCity
        self.form['collegePhoneNumber'] = obj.collegePhoneNumber

    
    #Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if DataValidator.isNull(self.form['collegeName']):
            inputError['collegeName'] = "College Name can not be Null"
            self.form['error'] = True
        
        else:
            if DataValidator.isalphacheck(self.form['collegeName']):
                inputError['collegeName'] = "College Name considers only letters"
                self.form['error'] = True
        
        if DataValidator.isNull(self.form['collegeAddress']):
            inputError['collegeAddress'] = "College Address Can not be Null"
            self.form['error'] = True
        
        if DataValidator.isNull(self.form['collegeState']):
            inputError['collegeState'] = "College State can not be Null"
            self.form['error'] = True
        
        if DataValidator.isNull(self.form['collegeCity']):
            inputError['collegeCity'] = "College City can not be Null"
            self.form['error'] = True

        if DataValidator.isNull(self.form['collegePhoneNumber']):
            inputError['collegePhoneNumber'] = "college phone number can't be NUll"
            self.form['error'] = True
        else:
            if(DataValidator.ismobilecheck(self.form['collegePhoneNumber'])):
                inputError['collegePhoneNumber'] = "Only Number's allowed which start with 6, 7, 8, 9"
                self.form['error'] = True
        
        return self.form['error']

    # Display College Page
    def display(self, request, params={}):
        if(params['id']>0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(), {'form':self.form})
        return res

    # Submit College Page
    def submit(self, request, params={}):
        if(params['id']>0):
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(collegeName=self.form['collegeName'])
            if dup.count() > 0:
                self.form['error'] = True
                self.form['message'] = "College Name Already Exist"
                res = render(request, self.get_template(), {'form':self.form})
            else:
                r = self.form_to_model(College())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message'] = "Data has been updated successfully"
                res = render(request, self.get_template(), {'form':self.form})

            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(collegeName=self.form['collegeName'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "College Name Already Exists"
                res = render(request, self.get_template(), {'form':self.form})
            else:
                r = self.form_to_model(College())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['message'] = False
                self.form['message'] = "Data has been saved successfully"
                res = render(request, self.get_template(), {'form':self.form})

            return res

    # Template html of College Page
    def get_template(self):
        return "College.html"

    def get_service(self):
        return CollegeService()
