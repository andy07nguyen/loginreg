from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from datetime import date
import re, bcrypt, datetime


# Create your models here.
class UserManager(models.Manager):
#REGISTER CLASS:
    def register(self, postData):
        fname_Regex = r'^(?P<firstname>[\w\s\w]*)'
        lname_Regex = r'^(?P<lastname>[\w\s\w]*)'
        email_Regex = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
        password_Regex = r'[A-Za-z0-9!@#$%^&*+=]{8,}$'
        error = []
        no_error = True

    #FIRST & LAST NAME VALIDATION:
        #FIRST NAME:
        if not len(postData['fname']) >= 3 and not re.match(fname_Regex, postData['fname']):
            error.append("Invalid First Name. Required 2 or more characters.")
            no_error = False

        #LAST NAME:
        if not len(postData['lname']) >= 3 and not re.match(lname_Regex, postData['lname']):
            error.append("Invalid Last Name. Required 2 or more characters.")
            no_error = False
    #EMAIL VALIDATION:
        #EMAIL REGEX:
        if not re.search(email_Regex, postData['email']):
            error.append("Invalid Email Address")
            no_error = False
        #DUPLCATE
        if User.objects.filter(email=postData['email']):
            error.append("Email Address is already taken. Please Try Again")
            no_error = False
        else:
            pass

    #PASSWORD & CONFIRMPW VALIDATION:
        if re.match(password_Regex, postData['password']) and postData['password'] == postData['confirmPw']:
            hashed = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        else:
            error.append("Invalid Password. Required 8 or more characters.")
            no_error = False
    #ERROR CHECK:
        if no_error == True:
            newUser = User.objects.create(first_name = postData['fname'], last_name = postData['lname'], email = postData['email'], password = hashed)
            error.append("Successful Registration! Please Log in")
            return (True, newUser)
        else:
            # messages.error(request, "Invalid Info")
            error.append("Invalid Information")
            return (False, error)

#LOGIN CLASS:
    def login(self, email, password):
        error = []
        no_error = True
        user = User.objects.filter(email = email)
        if not len(user) > 0: # if there's nothing in the field, that's an error
            error.append("Invalid Email Address")
            no_error = False
        elif bcrypt.hashpw(password.encode(), user[0].password.encode()) == user[0].password: # if there is something in the field and it matches, then we're good.
            error.append("Valid Password")
            no_error = True
        else:
            error.append("Invalid Email Address & Password") # there is something in the field, but it's not the right password
            no_error = False
    #ERROR CHECK:
        if no_error == True:
            error.append("Successful Logged In!")
            return(True, error, user[0])
        else:
            return(False, error)

#ADDTRIP CLASS:
    def addTrip(self, postData):
        today = date.today()
        errorMsg = []
        check = True
    #DESTINATION VALIDATION:
        if not len(postData['destination']) > 0:
            errorMsg.append("Invaild Destination Entry")
            check = False
    #DESCRIPTION VALIDATION:
        if not len(postData['description']) > 0:
            errorMsg.append("Invaild Description Entry")
            check = False
    #DATE VALIDATION:
        # fDate = str(postData['fromDate'])
        # tDate = str(postData['toDate'])
        # fromDate = datetime.datetime.strptime(fDate, "%Y+"-"+%m+"-"+%d").date()
        # toDate = datetime.datetime.strptime(tDate, "%Y+"-"+%m+"-"+%d").date()
        # #DATE FROM:
        # if not fromDate >= today:
        #     errorMsg.append("Invaild Date From Entry")
        #     check = False
        # #DATE TO:
        # if not toDate >= today and not postData['toDate'] >= postData['fromDate']:
        #     errorMsg.append("Invaild Date To Entry")
        #     check = False
    #ERROR CHECK:
        if check == True:
            newTrip = Trip.objects.create(destination = postData['destination'], description = postData['description'])
            errorMsg.append("Successful Added A Trip!")
            return(True, newTrip)
        else:
            errorMsg.append("Invaild Entries. Please Try Again.")
            return(False, errorMsg)




#OBJECT CLASS:
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.TextField(max_length=45)
    description = models.TextField(max_length=45)
    start_date = models.DateField(auto_now_add = True)
    end_date = models.DateField(auto_now = True)
    user_id = models.ManyToManyField(User, related_name="trips")
    objects = UserManager()




    # def __str__(self):
    #     return "First Name : " + self.first_name + "Last Name:  " + self.last_name + "ID:  " + str(self.id) + "\n"
