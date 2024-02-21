from service.service.CollegeService import CollegeService
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ORS.utility.DataValidator import DataValidator
from service.models import Student
from service.service.StudentService import StudentService


class StudentCtl(BaseCtl):
    def preload(self, request):
        self.page_list = CollegeService().preload()
        self.preload_data = self.page_list

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['firstName'] = requestForm['firstName']
        self.form['lastName'] = requestForm['lastName']
        self.form['dob'] = requestForm['dob']
        self.form['mobileNumber'] = requestForm['mobileNumber']
        self.form['email'] = requestForm['email']
        self.form['college_ID'] = requestForm['college_ID']

    def model_to_form(self, obj):
        if (obj==None):
            return
        self.form['id'] = obj.id
        self.form['firstName'] = obj.firstName
        self.form['lastName'] = obj.lastName
        self.form['dob'] = obj.dob.strftime("%Y-%m-%d")
        self.form['mobileNumber'] = obj.mobileNumber
        self.form['email'] = obj.email
        self.form['college_ID'] = obj.college_ID
        self.form['collegeName'] = obj.collegeName

    def form_to_model(self, obj):
        c = CollegeService().get(self.form['college_ID'])
        pk = int(self.form['id'])
        if (pk>0):
            obj.id = pk
        obj.firstName = self.form['firstName']
        obj.lastName = self.form['lastName']
        obj.dob = self.form['dob']
        obj.mobileNumber = self.form['mobileNumber']
        obj.email = self.form['email']
        obj.college_ID = self.form['college_ID']
        obj.collegeName = c.collegeName
        return obj

    # Validate Form
    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['firstName'])):
            inputError['firstName'] = "First Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['firstName'])):
                inputError['firstName'] = "First Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['lastName'])):
            inputError['lastName'] = "Last Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['lastName'])):
                inputError['lastName'] = "Last Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['dob'])):
            inputError['dob'] = "DOB can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['dob'])):
                inputError['dob']= "Incorrect Date, should be YYYY-MM-DD"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['mobileNumber'])):
            inputError['mobileNumber'] = "Mobile Number can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ismobilecheck(self.form['mobileNumber'])):
                inputError['mobileNumber'] = "Mobile Number must start with 6,7,8,9"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['email'])):
            inputError['email'] = "Email can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isemail(self.form['email'])):
                inputError['email'] = "Email Id must be like student@gmail.com"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['college_ID'])):
            inputError['college_ID'] = "College can not be null"
            self.form['error'] = True
        else:
            o = CollegeService().find_by_unique_key(self.form['college_ID'])
            self.form['collegeName'] = o.collegeName
        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(), {'form':self.form, 'collegeList':self.preload_data})
        return res

    def submit(self, request, params={}):
        if (params['id']>0):
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(email = self.form['email'])
            if dup.count()>0:
                self.form['error'] = True
                self.form['message'] = "Email already exists"
                res = render(request, self.get_template(),{'form':self.form,'collegeList':self.preload_data})
            else:
                r = self.form_to_model(Student())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message'] = "Data has been updated successfully"
                res = render(request, self.get_template(),{'form':self.form,'collegeList':self.preload_data})
        else:
            duplicate = self.get_service().get_model().objects.filter(email = self.form['email'])
            if duplicate.count()>0:
                self.form['error'] = True
                self.form['message'] = "Email already exists"
                res = render(request, self.get_template(),{'form':self.form,'collegeList':self.preload_data})
            else:
                r = self.form_to_model(Student())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message'] = "Data has been saved successfully"
                res = render(request, self.get_template(),{'form':self.form,'collegeList':self.preload_data})
        return res


    # Template html of Student Page
    def get_template(self):
        return "Student.html"

    def get_service(self):
        return StudentService()



















