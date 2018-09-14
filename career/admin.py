# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Question, Skill, Aziende, Admindata, User, Session,Risposta


class SkillAdmin(admin.ModelAdmin):
    list_display = ('id','question_text', 'question')
admin.site.register(Skill,SkillAdmin)
class QAdmin(admin.ModelAdmin):
    list_display = ('id','question_text')
admin.site.register(Question,QAdmin)
admin.site.register(Aziende)
admin.site.register(Admindata)
admin.site.register(Session)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','tempo', 'session', 'yob','gender')
admin.site.register(User,UserAdmin)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id','tempo','questionId', 'user', 'session','item1','item2','item3','item4','item5')
admin.site.register(Risposta, ReplyAdmin)
