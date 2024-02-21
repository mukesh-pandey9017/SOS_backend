from django.shortcuts import render,redirect
from ORS.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import Course, Subject
from service.forms import SubjectForm
from service.service.SubjectService import SubjectService
from service.service.CourseService import CourseService


class SubjectCtl(BaseCtl):
    def preload(self, request):
        self.page_list = CourseService().preload()
        self.preload_data = self.page_list

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['subjectName'] = requestForm['subjectName']
        self.form['subjectDescription'] = requestForm['subjectDescription']
        self.form['course_ID'] = requestForm['course_ID']

    def model_to_form(self, obj):
        if (obj==None):
            return
        self.form['id'] = obj.id
        self.form['subjectName'] = obj.SubjectName
        self.form['subjectDescription'] = obj.SubjectDescription
        self.form['course_ID'] = obj.Course_ID
        self.form['courseName'] = obj.courseName

    def form_to_model(self, obj):
        c = CourseService().get(self.form['course_ID'])
        pk = int(self.form['id'])
        if (pk>0):
            obj.id = pk
        obj.SubjectName = self.form['subjectName']
        obj.SubjectDescription = self.form['subjectDescription']
        obj.Course_ID = self.form['course_ID']
        obj.courseName = c.courseName
        return obj

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['subjectName'])):
            inputError['subjectName'] = "Subject Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacheck(self.form['subjectName'])):
                inputError['subjectName'] = "Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['subjectDescription'])):
            inputError['subjectDescription'] = "Subject Description can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['course_ID'])):
            inputError['course_ID'] = "Course can not be null"
            self.form['error'] = True
        else:
            obj = CourseService().find_by_unique_key(self.form['course_ID'])
            self.form['courseName'] = obj.courseName
        return self.form['error']

    def display(self, request, params={}):
        if (params['id']>0):
            id = params['id']
            r = self.get_service().get(id)
            self.model_to_form(r)
        res = render(request,self.get_template(),{'form':self.form,'courseList':self.preload_data})
        return res

    def submit(self, request, params={}):
        if (params['id']>0):
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(SubjectName = self.form['subjectName'])
            if dup.count()>0:
                self.form['error'] = True
                self.form['message'] = "Subject Name already exists"
                res = render(request,self.get_template(),{'form':self.form,'courseList':self.preload_data})
            else:
                r = self.form_to_model(Subject())
                self.get_service().save(r)
                self.form['id'] = r.id

                self.form['error'] = False
                self.form['message'] = "Data has been updated successfully"
                res = render(request,self.get_template(),{'form':self.form,'courseList':self.preload_data})
        else:
            duplicate = self.get_service().get_model().objects.filter(SubjectName = self.form['subjectName'])
            if duplicate.count()>0:
                self.form['error'] = True
                self.form['message'] = "Subject Name already exists"
                res = render(request,self.get_template(),{'form':self.form,'courseList':self.preload_data})
            else:
                r = self.form_to_model(Subject())
                self.get_service().save(r)
                self.form['id'] = r.id
                self.form['error'] = False
                self.form['message'] = "Data has been saved successfully"
                res = render(request,self.get_template(),{'form':self.form,'courseList':self.preload_data})
                
        return res


    # Template html of Subject Page
    def get_template(self):
        return "Subject.html"

    def get_service(self):
        return SubjectService()
