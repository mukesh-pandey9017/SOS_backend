from django.db import models

# Create your models here.


class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    login_id = models.EmailField()
    password = models.CharField(max_length=20)
    confirmpassword = models.CharField(max_length=20, default='')
    dob = models.DateField(max_length=20)
    address = models.CharField(max_length=50, default='')
    gender = models.CharField(max_length=50, default='')
    mobilenumber = models.CharField(max_length=50, default='')
    role_Id = models.IntegerField()
    role_Name = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'login_id': self.login_id,
            'password': self.password,
            'confirmpassword': self.confirmpassword,
            'dob': self.dob,
            'address': self.address,
            'gender': self.gender,
            'mobilenumber': self.mobilenumber,
            'role_Id': self.role_Id,
            'role_Name': self.role_Name
        }

        return data

    def __str__(self) -> str:
        return self.firstName + '_' + self.lastName

    class Meta:
        db_table = 'sos_user'


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def to_json(self):
        data = {
            'id':self.id,
            'name': self.name,
            'description': self.description
        }
        return data

    class Meta:
        db_table = 'ORS_ROLE'


class College(models.Model):
    collegeName = models.CharField(max_length=50)
    collegeAddress = models.CharField(max_length=50)
    collegeState = models.CharField(max_length=50)
    collegeCity = models.CharField(max_length=20)
    collegePhoneNumber = models.CharField(max_length=20)

    def to_json(self):
        data = {
            'id': self.id,
            'collegeName': self.collegeName,
            'collegeAddress': self.collegeAddress,
            'collegeState': self.collegeState,
            'collegeCity': self.collegeCity,
            'collegePhoneNumber': self.collegePhoneNumber
        }

        return data
    
    class Meta:
        db_table = 'ORS_COLLEGE'

class Course(models.Model):
    courseName = models.CharField(max_length=50)
    courseDescription = models.CharField(max_length=100)
    courseDuration = models.CharField(max_length=100)

    def to_json(self):
        data = {
            'id': self.id,
            'courseName': self.courseName,
            'courseDescription': self.courseDescription,
            'courseDuration': self.courseDuration
        }
        return data

    class Meta:
        db_table = 'ORS_COURSE'


class Marksheet(models.Model):
    rollNumber = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    physics = models.IntegerField()
    chemistry = models.IntegerField()
    maths = models.IntegerField()

    def to_json(self):
        data = {
            'id': self.id,
            'rollNumber': self.rollNumber,
            'name': self.name,
            'physics': self.physics,
            'chemistry': self.chemistry,
            'maths': self.maths
        }
        return data

    class Meta:
        db_table = 'ORS_MARKSHEET'


class Student(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    mobileNumber = models.CharField(max_length=20)
    email = models.EmailField()
    college_ID = models.IntegerField()
    collegeName = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'dob': self.dob,
            'mobileNumber': self.mobileNumber,
            'email': self.email,
            'college_ID': self.college_ID,
            'collegeName': self.collegeName
        }
        return data

    class Meta:
        db_table = 'ORS_STUDENT'


class Subject(models.Model):
    SubjectName = models.CharField(max_length=50)
    SubjectDescription = models.CharField(max_length=50)
    Course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'subjectName': self.SubjectName,
            'subjectDescription': self.SubjectDescription,
            'course_ID': self.Course_ID,
            'courseName': self.courseName
        }
        return data

    class Meta:
        db_table = 'ORS_SUBJECT'


class Faculty(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    dob = models.DateField(max_length=20)
    college_ID = models.IntegerField()
    collegeName = models.CharField(max_length=50)
    subject_ID = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'password': self.password,
            'address': self.address,
            'gender': self.gender,
            'dob': self.dob,
            'college_ID': self.college_ID,
            'collegeName': self.courseName,
            'subject_ID': self.subject_ID,
            'subjectName': self.subjectName,
            'course_ID': self.course_ID,
            'courseName': self.courseName,
        }
        return data

    class Meta:
        db_table = 'ORS_FACULTY'


class TimeTable(models.Model):
    examTime = models.CharField(max_length=40)
    examDate = models.DateField()
    subject_ID = models.IntegerField()
    subjectName = models.CharField(max_length=50)
    course_ID = models.IntegerField()
    courseName = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)

    def to_json(self):
        data = {
            'id': self.id,
            'examTime': self.examTime,
            'examDate': self.examDate,
            'subject_ID': self.subject_ID,
            'subjectName': self.subjectName,
            'course_ID': self.course_ID,
            'courseName': self.courseName,
            'semester': self.semester
        }
        return data

    class Meta:
        db_table = 'ORS_TIMETABLE'