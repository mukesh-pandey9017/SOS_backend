import re

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
    def isInt(cls, val):
        if(val == 0):
            return False
        else:
            return True
            
    @classmethod
    def ismobilecheck(cls, val):
        if re.match("^[6-9]\d{9}$", val):
            return False
        else:
            return True