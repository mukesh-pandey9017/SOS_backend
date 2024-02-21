from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import StudentForm
from service.models import Student
from service.service.StudentService import StudentService

class StudentListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['firstName'] = requestForm.get('firstName', None)
        self.form['lastName'] = requestForm.get('lastName', None)
        self.form['dob'] = requestForm.get('dob', None)
        self.form['mobileNumber'] = requestForm.get('mobileNumber', None)
        self.form['email'] = requestForm.get('email', None)
        self.form['college_ID'] = requestForm.get('college_ID', None)
        self.form['collegeName'] = requestForm.get('collegeName', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        StudentListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Student.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list,'form':self.form})
        return res

    def next(self, request, params={}):
        StudentListCtl.count += 1
        self.form['pageNo'] = StudentListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Student.objects.last().id
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form})
        return res

    def previous(self, request, params={}):
        StudentListCtl.count -= 1
        self.form['pageNo'] = StudentListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form})
        return res

    def submit(self, request, params={}):
        StudentListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list==[]:
            self.form['msg'] = "No record found"
        res = render(request, self.get_template(),{'pageList':self.page_list,'form':self.form})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = StudentListCtl.count
        if (bool(self.form['ids']) == False):
            self.form['error'] = True
            self.form['message'] = "Please Select at least one Checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form})
        else:
            for ids in self.form['ids']:
                record = self.get_service().search(self.form)
                self.page_list = record['data']

                id = int(ids)
                if (id>0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']
                        self.form['LastId'] = Student.objects.last().id
                        StudentListCtl.count = 1

                        self.form['error'] = False
                        self.form['message'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "DATA WAS NOT DELETED"
                        res =  render(request, self.get_template(),{'pageList':self.page_list,'form':self.form})
        return res


    # Template html of Student List Page
    def get_template(self):
        return "StudentList.html"

    def get_service(self):
        return StudentService()