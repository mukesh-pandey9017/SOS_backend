from django.shortcuts import render,redirect
from service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import User
from service.service.UserService import UserService
from service.service.RoleService import RoleService

class UserListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['firstName'] = requestForm.get("firstName", None)
        self.form['lastName'] = requestForm.get("lastName", None)
        self.form['login_id'] = requestForm.get("login_id", None)
        self.form['ids'] = requestForm.getlist("ids", None)

    def display(self, request, params={}):
        UserListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['lastId'] = User.objects.last().id 
        res = render(request, self.get_template(), {'pageList':self.page_list, "form": self.form})
        return res

    def next(self, request, params={}):
        UserListCtl.count += 1
        self.form['pageNo'] = UserListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        self.form['LastId'] = User.objects.last().id
        print(self.form)
        res = render(request, self.get_template(), {"pageList":self.page_list, "form":self.form})
        return res

    def previous(self, request, params={}):
        UserListCtl.count -= 1
        self.form['pageNo'] = UserListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = UserListCtl.count
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
                        self.form['LastId'] = User.objects.last().id
                        UserListCtl.count = 1

                        self.form['error'] = False
                        self.form['message'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
                    else:
                        self.form['error'] = True
                        self.form['message'] = "DATA WAS NOT DELETED"
                        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def submit(self, request, params={}):
        UserListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['msg'] = "No record found"
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def get_template(self):
        return "UserList.html"

    def get_service(self):
        return UserService()