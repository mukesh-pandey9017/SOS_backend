from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from .ctl.BaseCtl import BaseCtl
from .ctl.LoginCtl import LoginCtl
from .ctl.RegistrationCtl import RegistrationCtl
from .ctl.WelcomeCtl import WelcomeCtl
from .ctl.LogoutCtl import LogoutCtl
from .ctl.ChangePasswordCtl import ChangePasswordCtl
from .ctl.ForgetPasswordCtl import ForgetPasswordCtl
from .ctl.UserCtl import UserCtl
from .ctl.UserListCtl import UserListCtl
from .ctl.CollegeCtl import CollegeCtl
from .ctl.CollegeListCtl import CollegeListCtl
from .ctl.CourseCtl import CourseCtl
from .ctl.CourseListCtl import CourseListCtl
from .ctl.RoleCtl import RoleCtl
from .ctl.RoleListCtl import RoleListCtl
from .ctl.FacultyCtl import FacultyCtl
from .ctl.FacultyListCtl import FacultyListCtl
from .ctl.SubjectCtl import SubjectCtl
from .ctl.SubjectListCtl import SubjectListCtl
from .ctl.StudentCtl import StudentCtl
from .ctl.StudentListCtl import StudentListCtl
from .ctl.TimeTableCtl import TimeTableCtl
from .ctl.TimeTableListCtl import TimeTableListCtl
from .ctl.MyProfileCtl import MyProfileCtl
from .ctl.MarksheetCtl import MarksheetCtl
from .ctl.MarksheetListCtl import MarksheetListCtl
from .ctl.MarksheetMeritListCtl import MarksheetMeritListCtl

# Create your views here.

@csrf_exempt
def actionId(request, page='', operation="", id=0):
    path = request.META.get("PATH_INFO")
    if request.session.get("user") is not None and page != "":
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = None
        res = ctlObj.execute(request, {"id": id})

    elif page in ["Login","Registration","Home","ForgetPassword"]:
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = None
        res = ctlObj.execute(request, {"id": id})

    else:
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = "Session Expired,Please Login again"
        res = ctlObj.execute(request, {"id": id, 'path': path})

    return res


@csrf_exempt
def auth(request, page="", operation="", id=0):

    if page == "Logout":
        Session.objects.all().delete()
        request.session['user'] = None
        out = "Logout Successfull"
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id, "operation": operation, 'out': out})

    else:
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = "Session Expired,Please Login again"
        res = ctlObj.execute(request, {"id": id,})
    return res

def index(request):
    return render(request,"Home.html")
