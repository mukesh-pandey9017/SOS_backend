from .BaseCtl import BaseCtl
from django.shortcuts import render


class LogoutCtl(BaseCtl):

    def display(self, request, params={}):
        del request.session['user']
        request.session['user'] = None
        self.form['message'] = "Logout Successfull !!!"
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def submit(self, request, params={}):
        pass

    # Template html of Logout Page
    def get_template(self):
        return "Login.html"

    def get_service(self):
        pass
