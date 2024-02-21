from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .RestCtl.LoginCtl import LoginCtl
from .RestCtl.ForgetPasswordCtl import ForgetPasswordCtl
from .RestCtl.ChangepasswordCtl import ChangepasswordCtl
from .RestCtl.UserCtl import UserCtl
from .RestCtl.RegistrationCtl import RegistrationCtl
from .RestCtl.CollegeCtl import CollegeCtl
from .RestCtl.CourseCtl import CourseCtl
from .RestCtl.RoleCtl import RoleCtl
from .RestCtl.MarksheetCtl import MarksheetCtl
from .RestCtl.StudentCtl import StudentCtl
from .RestCtl.SubjectCtl import SubjectCtl
from .RestCtl.TimeTableCtl import TimeTableCtl
from .RestCtl.FacultyCtl import FacultyCtl
from .RestCtl.MyProfileCtl import MyProfileCtl


# Create your views here.

def info(request, page, action):
    print('Request Method--->>', request.method)
    print('Page------!', page)
    print('Action----!', action)
    print("Base----Path--->>", __file__)

@csrf_exempt
def action(request, page, action='get', id=0, pageNo=1):
    print("ID----!",id)
    info(request, page, action)
    methodCall = page + "Ctl()." + action + "(request, {'id':id, 'pageNo':pageNo})"
    print("action method call------>>",methodCall)
    response = eval(methodCall)
    return response