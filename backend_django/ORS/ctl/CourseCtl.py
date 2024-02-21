from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from ORS.utility.DataValidator import DataValidator
from service.models import College, Course
from service.service.CourseService import CourseService


class CourseCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['courseName'] = requestForm['courseName']
        self.form['courseDescription'] = requestForm['courseDescription']
        self.form['courseDuration'] = requestForm['courseDuration']


    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.courseName = self.form['courseName']
        obj.courseDescription = self.form['courseDescription']
        obj.courseDuration = self.form['courseDuration']
        return obj

    def model_to_form(self, obj):
        if obj==None:
            return
        self.form['id'] =obj.id
        self.form['courseName'] = obj.courseName
        self.form['courseDescription'] = obj.courseDescription
        self.form['courseDuration'] = obj.courseDuration

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['courseName'])):
            inputError['courseName'] = "Course Name can not be Null"
            self.form['error'] = True
        else:
            if(DataValidator.isalphacheck(self.form['courseName'])):
                inputError['courseName'] = "Course Name contains only letters"
                self.form['error'] = True
        if (DataValidator.isNull(self.form['courseDescription'])):
            inputError['courseDescription'] = "Course Description can not be Null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['courseDuration'])):
            inputError['courseDuration'] = "Course Duration can not be Null"
            self.form['error'] = True

        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(), {'form':self.form})
        return res

    def submit(self, request, params={}):
        if params['id'] > 0:
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(courseName = self.form['courseName'])
            if dup.count()>0:
                self.form['error'] = True
                self.form['message'] = "Course Name Already Exists"
                res = render(request, self.get_template(), {'form':self.form})
            else:
                r = self.form_to_model(Course())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message']= 'Data has been updated successfully'
                res = render(request, self.get_template(), {'form':self.form})

            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(courseName = self.form['courseName'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Course Name Already Exists"
                res = render(request, self.get_template(), {'form':self.form})
            else:
                r = self.form_to_model(Course())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message'] ='Data has been saved successfully'
                res = render(request, self.get_template(), {'form':self.form})

            return res
    
    # Template html of Course Page
    def get_template(self):
        return "Course.html"

    def get_service(self):
        return CourseService()
