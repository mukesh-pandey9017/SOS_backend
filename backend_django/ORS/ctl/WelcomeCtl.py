from django.http import HttpResponse
from django.shortcuts import render
from .BaseCtl import BaseCtl

class WelcomeCtl(BaseCtl):

    def display(self, request, params={}):
        user = request.session.get('user', None)
        # request.session['name'] = user.role_Name
        if(user is not None):
            self.form['message'] = "Welcome " + user.role_Name
        return render(request, self.get_template(), {'form': self.form})
    
    def submit(self, request, params={}):
        pass

    # Template html of Role Page
    def get_template(self):
        return "Welcome.html"

    # Service of Role
    def get_service(self):
        return "RoleService()"