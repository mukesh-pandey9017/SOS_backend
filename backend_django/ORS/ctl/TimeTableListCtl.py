from urllib import request
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import TimeTable
from .BaseCtl import BaseCtl
from service.service.TimeTableService import TimeTableService

class TimeTableListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['examTime'] = requestForm.get('examTime', None)
        self.form['examDate'] = requestForm.get('examDate', None)
        self.form['course_ID'] = requestForm.get('course_ID', None)
        self.form['courseName'] = requestForm.get('courseName', None)
        self.form['subject_ID'] = requestForm.get('subject_ID', None)
        self.form['subjectName'] = requestForm.get('subjectName', None)
        self.form['semester'] = requestForm.get('semester', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        TimeTableListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = TimeTable.objects.last().id
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res

    def next(self,request, params={}):
        TimeTableListCtl.count += 1
        self.form['pageNo'] = TimeTableListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = TimeTable.objects.last().id
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res
 

    def previous(self,request, params={}):
        TimeTableListCtl.count -= 1
        self.form['pageNo'] = TimeTableListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res

    def submit(self,request, params={}):
        TimeTableListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list==[]:
            self.form['msg'] = "No record found"
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = TimeTableListCtl.count
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
                if (id>0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']
                        self.form['LastId'] = TimeTable.objects.last().id
                        TimeTableListCtl.count = 1

                        self.form['error'] = False
                        self.form['message'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        print("ppppp------>",self.page_list)
                        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "DATA WAS NOT DELETED"
                        res = render(request,self.get_template(),{'form':self.form,'pagelist':self.page_list})
        return res


    # Template html of TimeTable List page
    def get_template(self):
        return "TimeTableList.html"

    def get_service(self):
        return TimeTableService()