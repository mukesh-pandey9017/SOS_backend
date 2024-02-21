from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import CourseForm
from service.models import  Course
from service.service.CourseService import CourseService

class CourseListCtl(BaseCtl):
    count = 1
    # print("Last ID in Table",Course.objects.last().id)

    def request_to_form(self, requestForm):
        self.form['courseName'] = requestForm.get('courseName', None)
        self.form['courseDescription'] = requestForm.get('courseDescription', None)
        self.form['courseDuration'] = requestForm.get('courseDuration', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        CourseListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Course.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def next(self, request, params={}):
        CourseListCtl.count += 1
        self.form['pageNo'] = CourseListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = Course.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def previous(self, request, params={}):
        CourseListCtl.count -= 1
        self.form['pageNo'] = CourseListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def submit(self, request, params={}):
        CourseListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['msg'] = "No record found"
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = CourseListCtl.count
        if (bool(self.form['ids']) == False):
            self.form['error'] = True
            self.form['message'] = "Please Select at least one Checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
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
                        self.form['LastId'] = Course.objects.last().id
                        CourseListCtl.count = 1

                        self.form['error'] = False
                        self.form['message'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "DATA WAS NOT DELETED"
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    # Template html of CourseList page
    def get_template(self):
        return "CourseList.html"

    def get_service(self):
        return CourseService()
