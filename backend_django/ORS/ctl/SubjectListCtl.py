from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Subject
from .BaseCtl import BaseCtl
from service.service.SubjectService import SubjectService

class SubjectListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['subjectName'] = requestForm.get('subjectName',None)
        self.form['subjectDescription'] = requestForm.get('description',None)
        self.form["course_ID"] = requestForm.get('course_ID', None)
        self.form['courseName'] = requestForm.get('courseName', None)
        self.form['ids'] = requestForm.getlist('ids', None)


    def display(self, request, params={}):
        SubjectListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Subject.objects.last().id
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res

    def next(self, request,params={}):
        SubjectListCtl.count += 1
        self.form['pageNo'] = SubjectListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Subject.objects.last().id
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res

    def previous(self, request,params={}):
        SubjectListCtl.count -= 1
        self.form['pageNo'] = SubjectListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res

    def submit(self, request,params={}):
        SubjectListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list==[]:
            self.form['msg'] = "No record found"
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = SubjectListCtl.count
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
                if id>0 :
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']
                        self.form['LastId'] = Subject.objects.last().id                        
                        SubjectListCtl.count = 1
                        
                        self.form['error'] = False
                        self.form['message'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res =  render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "DATA WAS NOT DELETED"
                        res =  render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res

    # Template html of SubjectList page
    def get_template(self):
        return "SubjectList.html"

    def get_service(self):
        return SubjectService()


