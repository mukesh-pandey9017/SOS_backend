from datetime import *
import re
from types import ClassMethodDescriptorType

class DataValidator:

    @classmethod
    def isNotNull(cls, val):
        if(val == None or val == ""):
            return False
        else:
            return True

    @classmethod
    def isNull(cls, val):
        if(val == None or val == ""):
            return True
        else:
            return False

    @classmethod
    def isDate(cls, val):
        if re.match("([0-2]\d{3})-(0\d|1[0-2])-([0-2]\d|3[01])", val):
            if(datetime.strptime(val,"%Y-%m-%d") <= datetime.strptime(str(date.today()),"%Y-%m-%d")):# Comparing date with current date
                return False
            else:
                return True
        else:
            return True

    @classmethod
    def ischeck(cls, val):
        if(val == None or val == ""):
            return True
        else:
            if(0 <= int(val) <= 100):
                return False
            else:
                return True

    @classmethod
    def ischeckroll(cls, val):
        if re.match("^(?=.*[0-9]$)(?=.*[A-Z])", val):
            return False
        else:
            return True


    @classmethod
    def isalphacheck(cls, val):
        if re.match("^[a-zA-z\s]+$", val):
            return False
        else:
            return True

    @classmethod
    def ismobilecheck(cls, val):
        if re.match("^[6-9]\d{9}$", val):
            return False
        else:
            return True


    @classmethod
    def isemail(cls, val):
        if re.match("[^@]+@[^@]+\.[^@]+", val):
            return False
        else:
            return True


    @classmethod
    def isphonecheck(cls, val):
        if re.match("^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$", val):
            return False
        else:
            return True
    