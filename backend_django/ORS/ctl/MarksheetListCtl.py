from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import MarksheetForm
from service.models import Marksheet
from service.service.MarksheetService import MarksheetService

class MarksheetListCtl(BaseCtl):
    count=1

    def request_to_form(self,requestForm):
        self.form["rollNumber"]=requestForm.get("rollNumber",None)
        self.form["name"]=requestForm.get("name",None)
        self.form["physics"]=requestForm.get("physics",None)
        self.form["chemistry"]=requestForm.get("chemistry",None)
        self.form["maths"]=requestForm.get("maths",None)
        self.form["student_ID"]=requestForm.get("student_ID",None)
        self.form["ids"]= requestForm.getlist( "ids", None)

    def display(self,request,params={}):
        MarksheetListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list=record["data"]
        self.form['LastId'] = Marksheet.objects.last().id
        res = render(request,self.get_template(),{"pageList":self.page_list,'form':self.form})
        return res


    def next(self, request, params={}):    
        MarksheetListCtl.count+=1
        self.form["pageNo"]=MarksheetListCtl.count
        record = self.get_service().search(self.form)
        self.page_list=record["data"]
        self.form['LastId'] = Marksheet.objects.last().id
        res = render(request, self.get_template(), {"pageList": self.page_list,"form":self.form})
        return res
   
    def previous(self, request, params={}):    
        MarksheetListCtl.count-=1
        self.form["pageNo"]=MarksheetListCtl.count
        record = self.get_service().search(self.form)
        self.page_list=record["data"]
        res = render(request, self.get_template(), {"pageList": self.page_list,"form":self.form})
        return res


    def submit(self,request,params={}):
        MarksheetListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list=record["data"]
        if self.page_list==[]:
            self.form['msg'] = "No record found"
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res
        
    def get_template(self):
        return "MarksheetList.html"          

    # Service of Marksheet     
    def get_service(self):
        return MarksheetService()        

    def deleteRecord(self,request,params={}):
        self.form["pageNo"] = MarksheetListCtl.count
        if(bool(self.form["ids"])==False):
            self.form["error"] = True
            self.form["message"] = "Please Select at least one check box"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            return render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        else:
            for ids in self.form["ids"]:
                record = self.get_service().search(self.form)
                self.page_list=record["data"]

                id=int(ids)
                if( id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form["pageNo"]=1
                        record = self.get_service().search(self.form)
                        self.page_list=record["data"]
                        self.form['LastId'] = Marksheet.objects.last().id
                        MarksheetListCtl.count = 1

                        self.form["error"] = False
                        self.form["message"] = "DATA IS SUCCESSFULLY DELETED"
                        print("ppppppp-->",self.page_list)
                        return render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        return render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
