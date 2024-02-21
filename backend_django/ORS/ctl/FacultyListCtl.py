from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from .BaseCtl import BaseCtl
from service.models import Faculty
from service.forms import FacultyForm
from service.service.FacultyService import FacultyService

class FacultyListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id', None)
        self.form['firstName'] = requestForm.get('firstName', None)
        self.form['lastName'] = requestForm.get('lastName', None)
        self.form['email'] = requestForm.get('email', None)
        self.form['password'] = requestForm.get('password', None)
        self.form['address'] = requestForm.get('address', None)
        self.form['gender'] = requestForm.get('gender', None)
        self.form['dob'] = requestForm.get('dob', None)
        self.form['college_ID']  = requestForm.get('college_ID', None)
        self.form['course_ID'] = requestForm.get('course_ID', None)
        self.form['subject_ID'] = requestForm.get('subject_ID', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        FacultyListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Faculty.objects.last().id
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res

    def next(self, request,params={}):
        FacultyListCtl.count += 1
        self.form['pageNo'] = FacultyListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Faculty.objects.last().id
        res  = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res

    def previous(self, request,params={}):
        FacultyListCtl.count -= 1
        self.form['pageNo'] = FacultyListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res  = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res

    def submit(self, request,params={}):
        FacultyListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list==[]:
            self.form['msg'] = "No record found"
        res  = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = FacultyListCtl.count
        if (bool(self.form['ids'])==False):
            self.form['error'] = True
            self.form['message'] = "Please Select at least one Checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res =  render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        else:
            for ids in self.form['ids']:
                record = self.get_service().search(self.form)
                self.page_list = record['data']

                id = int(ids)
                if id>0:
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']
                        self.form['LastId'] = Faculty.objects.last().id
                        FacultyListCtl.count = 1
                        
                        self.form['error'] = False
                        self.form['message'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res =  render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "DATA WAS NOT DELETED"    
                        res =  render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res


    # Template html of AddFaculty list page
    def get_template(self):
        return "FacultyList.html"

    def get_service(self):
        return FacultyService()
