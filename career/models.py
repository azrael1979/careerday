# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import smart_str, smart_unicode
from django.db import models
import random
from datetime import datetime

# Create your models here.
#@python_2_unicode_compatible  # only if you need to support Python 2
class Question(models.Model):
    question_text = models.CharField(max_length=1500)
    page=models.IntegerField(default=0)
    def __str__(self):
        return smart_str(self.question_text)
    #sessione definita dal QR code

class Aziende(models.Model):
    settore=models.TextField()
    dislocazione=models.IntegerField()

class Admindata(models.Model):
    total_sessions=models.IntegerField()
    employer_averages=models.TextField()
    uni_averages=models.TextField()


class Session(models.Model):
    chiusa=models.BooleanField(default='False')
    tempo=models.DateTimeField(default=datetime.now, blank=True)
    data=models.DateTimeField(default=datetime.now, blank=True)
    tipologia=models.TextField(default="UNI")
    note=models.TextField()
    hash=models.CharField(max_length=128)
    qrcode = models.CharField(max_length=400)    
    
class User(models.Model):
    tempo=models.DateTimeField(default=datetime.now, blank=True)
    #classe_utente=models.IntegerField(default=0) #0=studente #1=
    yob=models.CharField(max_length=4,default=1998)
    gender=models.CharField(max_length=1,default='F')  
    session=models.CharField(max_length=128,default="")
    
#@python_2_unicode_compatible  # only if you need to support Python 2
class Skill(models.Model):
    question_text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    rank=models.IntegerField(default=0)
    session=models.IntegerField(default=0) #sessione definita dal QR code
    #pub_date = models.DateTimeField('date published')
    def __str__(self):
        return smart_str(self.question_text)
    
class Risposta(models.Model):
    tempo=models.DateTimeField(default=datetime.now, blank=True)
    questionId=models.IntegerField()
    user=models.IntegerField(default=0)
    session=models.CharField(max_length=128)
    item1=models.IntegerField(default=1)
    item2=models.IntegerField(default=2)
    item3=models.IntegerField(default=3)
    item4=models.IntegerField(default=4)
    item5=models.IntegerField(default=5)
    def __str__(self):
        return smart_str(self.session)

    