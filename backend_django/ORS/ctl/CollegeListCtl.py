from ast import Try
from .BaseCtl import BaseCtl
from ORS.utility.DataValidator import DataValidator
from django.shortcuts import render
from service.forms import CollegeForm
from service.models import College
from service.service.CollegeService import CollegeService

class CollegeListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['collegeName'] = requestForm.get("collegeName", None)
        self.form['collegeAddress'] = requestForm.get("collegeAddress", None)
        self.form['collegeState'] = requestForm.get("collegeState", None)
        self.form['collegeCity'] = requestForm.get("collegeCity", None)
        self.form['collegePhoneNumber'] = requestForm.get("collegePhoneNumber", None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        CollegeListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = College.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def previous(self, request, params={}):
        CollegeListCtl.count -= 1
        self.form['pageNo'] = CollegeListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def next(self, request, params={}):
        CollegeListCtl.count += 1
        self.form['pageNo'] = CollegeListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = College.objects.last().id
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def submit(self, request, params={}):
        CollegeListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['msg'] = "No record found"
        ress = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return ress

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = CollegeListCtl.count
        if (bool(self.form['ids']) == False):
            self.form['error'] = True
            self.form['message'] = "Please select atleast one checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        else:
            for ids in self.form['ids']:
                record = self.get_service().search(self.form)
                self.page_list = record['data']

                id = int(ids)
                if(id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']
                        self.form['LastId'] = College.objects.last().id
                        CollegeListCtl.count = 1

                        self.form['error'] = False
                        self.form['message'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        print("ppppppppp----->>", self.page_list)
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "DATA WAS NOT DELETED"
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def get_template(self):
        return "CollegeList.html"

    def get_service(self):
        return CollegeService()
