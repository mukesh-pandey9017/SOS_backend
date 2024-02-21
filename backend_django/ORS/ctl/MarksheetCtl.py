from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ORS.utility.DataValidator import DataValidator
from service.models import Marksheet
from service.service.MarksheetService import MarksheetService



class MarksheetCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['rollNumber'] = requestForm['rollNumber']
        self.form['physics'] = requestForm['physics']
        self.form['chemistry'] = requestForm['chemistry']
        self.form['maths'] = requestForm['maths']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk>0:
            obj.id = pk
        obj.rollNumber = self.form['rollNumber']
        obj.name = self.form['name']
        obj.physics = self.form['physics']
        obj.chemistry = self.form['chemistry']
        obj.maths = self.form['maths']
        return obj

    def model_to_form(self, obj):
        if obj==None:
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['rollNumber'] = obj.rollNumber
        self.form['physics'] = obj.physics
        self.form['chemistry'] = obj.chemistry
        self.form['maths'] = obj.maths

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['rollNumber'])):
            inputError['rollNumber'] = "Roll Number can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ischeckroll(self.form['rollNumber'])):
                inputError['rollNumber'] = "Roll Number must be alpha numeric"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['name'])):
                inputError['name'] = "Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['physics'])):
            inputError['physics'] = "Physics can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ischeck(self.form['physics'])):
                inputError['physics'] = "Please Enter Number below 100"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['chemistry'])):
            inputError['chemistry'] = "Chemistry can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ischeck(self.form['chemistry'])):
                inputError['chemistry'] = "Please Enter Number below 100"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['maths'])):
            inputError['maths'] = "Maths can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ischeck(self.form['maths'])):
                inputError['maths'] = "Please Enter Number below 100"
                self.form['error'] = True
        return self.form['error']

        
    def display(self, request, params={}):
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(), {'form':self.form})
        return res

    def submit(self, request, params={}):
        if (params['id'] > 0):
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(rollNumber = self.form['rollNumber'])
            if dup.count()>0:
                self.form['error'] = True
                self.form['message'] = "Roll Number already exists"
                res = render(request, self.get_template(),{'form':self.form})
                return res
            else:
                r = self.form_to_model(Marksheet())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message'] = 'Data has been updated successfully'
                res = render(request, self.get_template(),{'form':self.form})
                return res
        else:
            duplicate = self.get_service().get_model().objects.filter(rollNumber = self.form['rollNumber'])
            if duplicate.count()>0:
                self.form['error'] = True
                self.form['message'] = "Roll Number already exists"
                res = render(request, self.get_template(),{'form':self.form})
                return res
            else:
                r = self.form_to_model(Marksheet())
                self.get_service().save(r)
                self.form['error'] = False
                self.form['message'] = 'Data has been saved successfully'
                res = render(request, self.get_template(),{'form':self.form})
                return res

    # Template html of Marksheet page
    def get_template(self):
        return "Marksheet.html"

    def get_service(self):
        return MarksheetService()        

