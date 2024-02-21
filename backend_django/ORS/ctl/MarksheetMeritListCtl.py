from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Marksheet
from service.forms import MarksheetForm
from service.service.MarksheetMeritListService import MarksheetMeritListService
from service.service.StudentService import StudentService

class MarksheetMeritListCtl(BaseCtl):
    count =1
    
    def request_to_form(self, requestForm):
        self.form['rollNumber'] = requestForm.get('rollNumber', None)
        self.form['name'] = requestForm.get('name', None)
        self.form['physics'] = requestForm.get('physics', None)
        self.form['chemistry'] = requestForm.get('chemistry', None)
        self.form['maths'] = requestForm.get('maths', None)
        self.form['ids'] = requestForm.getlist('ids', None)
    
    
    #Display Marksheet page 
    def display(self,request,params={}):
        record = self.get_service().search()
        self.page_list = record['data']
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res


    #Submit Marksheet page
    def submit(self,request,params={}):
        record = self.get_service().search()
        self.page_list = record['data']
        if self.page_list==[]:
            self.form['msg'] = 'No record found'
        res = render(request,self.get_template(),{'form':self.form,'pageList':self.page_list})
        return res
        
    # Template html of Role page    
    def get_template(self):
        return "MarksheetMeritList.html"          

    # Service of Role     
    def get_service(self):
        return MarksheetMeritListService()
