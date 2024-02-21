from django.shortcuts import render,redirect
from .BaseCtl import BaseCtl
from ORS.utility.DataValidator import DataValidator
from service.models import Course, Faculty
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from service.service.FacultyService import FacultyService
# from service.service.FacultyService import FacultyService


class FacultyCtl(BaseCtl):

    def preload(self, request):
        self.course_List = CourseService().preload()
        self.college_List = CollegeService().preload()
        self.subject_List = SubjectService().preload()

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['firstName'] = requestForm['firstName']
        self.form['lastName'] = requestForm['lastName']
        self.form['email'] = requestForm['email']
        self.form['password'] = requestForm['password']
        self.form['address'] = requestForm['address']
        self.form['gender'] = requestForm['gender']
        self.form['dob'] = requestForm['dob']
        self.form['college_ID'] = requestForm['college_ID']
        self.form['course_ID'] = requestForm['course_ID']
        self.form['subject_ID'] = requestForm['subject_ID']

    def model_to_form(self, obj):
        if (obj==None):
            return
        self.form['id'] = obj.id
        self.form['firstName'] = obj.firstName
        self.form['lastName'] = obj.lastName
        self.form['email'] = obj.email
        self.form['password'] = obj.password
        self.form['address'] = obj.address
        self.form['gender'] = obj.gender
        self.form['dob'] = obj.dob.strftime("%Y-%m-%d")
        self.form['college_ID'] = obj.college_ID
        self.form['course_ID'] = obj.course_ID
        self.form['subject_ID'] = obj.subject_ID
        self.form['collegeName'] = obj.collegeName
        self.form['courseName'] = obj.courseName
        self.form['subjectName'] = obj.subjectName

    def form_to_model(self, obj):
        c = CourseService().get(self.form['course_ID'])
        e = CollegeService().get(self.form['college_ID'])
        s = SubjectService().get(self.form['subject_ID'])
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.firstName = self.form['firstName']
        obj.lastName = self.form['lastName']
        obj.email  = self.form['email']
        obj.password = self.form['password']
        obj.address = self.form['address']
        obj.dob = self.form['dob']
        obj.gender = self.form['gender']
        obj.course_ID = self.form['course_ID']
        obj.college_ID = self.form['college_ID']
        obj.subject_ID = self.form['subject_ID']
        obj.courseName = c.courseName
        obj.collegeName = e.collegeName
        obj.subjectName = s.SubjectName
        return obj
    
    #Validate form
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

        if (DataValidator.isNull(self.form['email'])):
            inputError['email'] = "Email can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isemail(self.form['email'])):
                inputError['email'] = "Email must be like student@gmail.com"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['password'])):
            inputError['password'] = "password can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['address'])):
            inputError['address'] = "Address can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['gender'])):
            inputError['gender'] = "Gender can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['dob'])):
            inputError['dob'] = "DOB can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['dob'])):
                inputError['dob'] = "Incorrect date format, should be YYYY-MM-DD"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['course_ID'])):
            inputError['course_ID'] = "Course can not be null"
            self.form['error'] = True
        else:
            o = CourseService().find_by_unique_key(self.form['course_ID'])
            self.form['courseName'] = o.courseName

        if (DataValidator.isNull(self.form['college_ID'])):
            inputError['college_ID'] = "College can not be null"
            self.form['error'] = True
        else:
            o = CollegeService().find_by_unique_key(self.form['college_ID'])
            self.form['collegeName'] = o.collegeName

        if (DataValidator.isNull(self.form['subject_ID'])):
            inputError['subject_ID'] = "Subject can not be null"
            self.form['error'] = True
        else:
            o = SubjectService().find_by_unique_key(self.form['subject_ID'])
            self.form['subjectName'] = o.SubjectName
        return self.form['error']

    def display(self, request, params={}):
        if (params['id'] > 0):
            id = params['id']
            r = self.get_service().get(id)
            self.model_to_form(r)
        res = render(request, self.get_template(), {
                     'form': self.form, 'courseList': self.course_List, 'collegeList': self.college_List, 'subjectList': self.subject_List})
        return res

    def submit(self, request, params={}):
        if (params['id']>0):
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(email = self.form['email'])
            if dup.count() > 0:
                self.form['error'] = True
                self.form['message'] = "Email Already Exists"
                res = render(request, self.get_template(), {
                    'form':self.form, 'courseList':self.course_List, 'collegeList':self.college_List, 'subjectList':self.subject_List
                })
            else:
                r = self.form_to_model(Faculty())
                self.get_service().save(r)
                self.form['id'] = r.id

                self.form['error'] = False
                self.form['message'] = 'Data has been updated successfully'
                res = render(request, self.get_template(), {
                    'form':self.form, 'courseList':self.course_List, 'collegeList':self.college_List, 'subjectList':self.subject_List
                })

        else:
            duplicate = self.get_service().get_model().objects.filter(email=self.form['email'])
            if (duplicate.count() > 0):
                self.form['error'] = True
                self.form['message'] = "Email already exists"
                res = render(request, self.get_template(), {
                             'form': self.form, 'courseList': self.course_List, 'collegeList': self.course_List, 'subjectList': self.subject_List})
            else:
                r = self.form_to_model(Faculty())
                self.get_service().save(r)

                self.form['error'] = False
                self.form['message'] = 'Data has been saved successfully'
                res = render(request, self.get_template(), {
                    'form':self.form, 'courseList':self.course_List, 'collegeList':self.college_List, 'subjectList':self.subject_List
                })
        return res

    # Template html of AddFaculty page
    def get_template(self):
        return "Faculty.html"

    def get_service(self):
        return FacultyService()
