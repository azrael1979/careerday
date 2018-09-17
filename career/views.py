# -*- coding: utf-8 -*-
from __future__ import unicode_literals,division
from django.views.decorators.cache import never_cache
from django.shortcuts import redirect
from django.contrib import messages
from django.template import RequestContext
import random,sys,os
import io
import boto
import tinyurl
from PIL import Image
from botocore.client import Config
from scipy import spatial
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import time
import json
from .forms import NameForm, SessionForm
from .models import Question, Skill, Aziende, Admindata, User,Session,Risposta
from django.shortcuts import render
import uuid #per generare gli hash
from django.shortcuts import render_to_response
from django.template.context import RequestContext as RC
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import qrcode
from django.views.generic.edit import FormView
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import datetime
from scipy.constants.constants import yobi

ACCESS_ID = 'RPIBQG3DPFHSGPEKIXSI'
SECRET_KEY = 'e+SvUUoKa3S61BF020aOzOmvRFZz3MRb7YfmytlTiEs'
host_url='http://104.248.46.248:8000'
hash_text=''

def mean(a):
    return sum(a) / len(a)


#variabile globale con il token della sessione
session_id=''
global_user=0

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)



# Create your views here.    
def show_qr_view(request):
    session_id=request.GET.get('session')
    latestsession=Session.objects.filter(hash=session_id)[0]
#    latestsession=Session.objects.latest('id')
    #print "L'ultima sessione è:"+latestsession.hash
    url=tinyurl.create_one(host_url+'/start_session/?session='+session_id)
    #print url
    img=latestsession.qrcode
    #print img
    return render(request,"interstitial.html",{"img":img,"session":session_id,"url":url})

class newsession_form(FormView):
    def get_initial(self):
        while True:
            hash_text=uuid.uuid4().hex
            #print hash_text
            try: 
                t=Session.objects.get(hash=hash_text).exists()
                print "hex already present, new one being generated" 
            except:
                print "ok, hash is new" +hash_text
                break
        initial = super(newsession_form, self).get_initial()
        initial['hash'] = hash_text
        return initial
    #hash_text=str(random.getrandbits(128))
    template_name="newsession.html"
    form_class=SessionForm
    def form_valid(self, form):
        form.save()
        form.process_session()
        #return super(newsession_form, self).form_valid(form)
        return redirect('/show_qr?session='+form.cleaned_data.get('hash'))

@never_cache        
@csrf_protect
def newuser(request):
    anno_attuale=int(datetime.datetime.now().year)
    anno_minimo=anno_attuale-100
    anno_medio=anno_attuale-55
    session=request.GET["session"]
    user=request.GET["user"]
    anni=[x for x in range (anno_minimo,anno_attuale-10)]
    return render(request, 'name.html', {'anni':anni,'maxyear': anno_attuale-10,'averageyear':anno_medio,'minyear':anno_minimo,"userid":user,"sessionid":session})
@never_cache
@csrf_protect
def newuserprocess(request):
    genders=['F','NA','M']
    UserID=request.GET['user']
    yob=request.GET['foo']
    gender=request.GET['gender']
    sessionid=request.GET['session']
    t=User.objects.get(id=UserID)
    t.yob=yob
    t.gender=gender
    #print "il nuovo utente ha id"+UserID+"gender"+gender+"sessione"+sessionid+"yob"+str(yob)
    t.save()
    return redirect("/endpage?user="+UserID+"&session="+sessionid)
@never_cache    
def question1(request):
    session_id=str(request.GET.get("session"))
    user_id=str(request.GET.get("user"))
    if (Session.objects.get(hash=session_id).chiusa==True):
        return redirect(sessionclosed) 
    #prendiamo utente e sessione dalll'uRL
    #print session_id, user_id
    skill_set=[]
    q_id=0
    q=Question.objects.all()
    q1=q[q_id]
    context_instance = RC( request, {} )
    skills=Skill.objects.filter(question__question_text__contains=q1.question_text)
    #print q1.question_text
    for item in skills:
        skill_set.append(item.question_text)
    return render(request,
        "sortable.html",
        {'question':q1.question_text,"skill_set":skill_set,"next":"/question2?session="+session_id+"&user="+user_id,"prev":"/index","sessione":session_id,"utente":user_id,"question_id":0}
        )
@never_cache    
def question2(request):
    session_id=str(request.GET.get("session"))
    user_id=str(request.GET.get("user"))
    if (Session.objects.get(hash=session_id).chiusa==True):
        return redirect(sessionclosed) 

    skill_set=[]
    q_id=1
    q=Question.objects.all()
    q1=q[q_id]
    context_instance = RC( request, {} )
    skills=Skill.objects.filter(question__question_text__contains=q1.question_text)
    #print q1.question_text
    for item in skills:
        skill_set.append(item.question_text)
    return render(request,
        "sortable2.html",
        {'question':q1.question_text,"skill_set":skill_set,"next":"/question3?session="+session_id+"&user="+user_id,"prev":"/question1?session="+session_id+"&user="+user_id,"sessione":session_id,"utente":user_id,"question_id":1})
@never_cache    
def question3(request):
    session_id=str(request.GET.get("session"))
    user_id=str(request.GET.get("user"))
    if (Session.objects.get(hash=session_id).chiusa==True):
        return redirect(sessionclosed) 

    skill_set=[]
    q_id=2
    q=Question.objects.all()
    q1=q[q_id]
    context_instance = RC( request, {} )
    skills=Skill.objects.filter(question__question_text__contains=q1.question_text)
    #print q1.question_text
    for item in skills:
        skill_set.append(item.question_text)
    return render(request,
        "sortable3.html",
        {'question':q1.question_text,"skill_set":skill_set,"next":"/question4?session="+session_id+"&user="+user_id,"prev":"/question2?session="+session_id+"&user="+user_id,"sessione":session_id,"utente":user_id,"question_id":2
        })
@never_cache    
def question4(request):
    session_id=str(request.GET.get("session"))
    user_id=str(request.GET.get("user"))
    if (Session.objects.get(hash=session_id).chiusa==True):
        return redirect(sessionclosed) 

    skill_set=[]
    q_id=3
    q=Question.objects.all()
    q1=q[q_id]
    context_instance = RC( request, {} )
    skills=Skill.objects.filter(question__question_text__contains=q1.question_text)
    #print q1.question_text
    for item in skills:
        skill_set.append(item.question_text)
    return render(request,
        "sortable4.html",
        {'question':q1.question_text,"skill_set":skill_set,"next":"/question5?session="+session_id+"&user="+user_id,"prev":"/question3?session="+session_id+"&user="+user_id,"sessione":session_id,"utente":user_id,"question_id":3
        })

@never_cache    
def question5(request):
    session_id=str(request.GET.get("session"))
    user_id=str(request.GET.get("user"))
    if (Session.objects.get(hash=session_id).chiusa==True):
        return redirect(sessionclosed) 

    skill_set=[]
    q_id=4
    q=Question.objects.all()
    q1=q[q_id]
    context_instance = RC( request, {} )
    skills=Skill.objects.filter(question__question_text__contains=q1.question_text)
    #print q1.question_text
    for item in skills:
        skill_set.append(item.question_text)
    return render(request,
        "sortable5.html",
        {'question':q1.question_text,"skill_set":skill_set,"next":"/newuser?session="+session_id+"&user="+user_id,"prev":"/question4?session="+session_id+"&user="+user_id,"sessione":session_id,"utente":user_id,"question_id":4
        })
@csrf_exempt    
def process_id(request):
    if request.method == 'POST':
        #print "ok, ora processiamo i dati"
        stringa=request.POST        
        #log.debug(stringa)
        #print stringa
    #list (stringa.items)

def sessionclosed (request):
    return render (request, "sessionclosed.html")
    

def start_session(request):
    token=request.GET.get('session',"")
    #print "token"+token
    userID=str(User.objects.create(session=token).id)
  #  response = redirect('question1', permanent=True)
  #  response['Location'] += '?session='+token+"&user=100"
  #  return response
    return redirect ("/question1?session="+token+"&user="+userID,permanent=True)

        
@csrf_exempt    
def process(request):#processa l'ordine di ciascuna lista di skills
    array_risultati=[]
    if request.method == 'POST':
        #print "ok, ora processiamo i dati"
        stringa=request.POST     
        #array_risultati=stringa.split(',')
        sessione_proc=stringa['session']
        utente_proc=stringa['utente']
        domanda_proc=stringa['domanda_id']
        item1_proc=stringa['item1']
        item2_proc=stringa['item2']
        item3_proc=stringa['item3']
        item4_proc=stringa['item4']
        item5_proc=stringa['item5']
        t,created = Risposta.objects.get_or_create(session=sessione_proc,user=utente_proc,questionId=domanda_proc)
        t.item1=int(item1_proc)
        t.item2=int(item2_proc)
        t.item3=int(item3_proc)
        t.item4=int(item4_proc)
        t.item5=int(item5_proc)
        t.save()
        #print "reply updated"
        print created
        return (HttpResponse('successo elab dati'))

def get_replies(qset,faimedia): #k è un queryset
    myreplies=[]
    lista_risposte=[]
    for k in qset:
        lista_risposte=[]
        #lista_risposte.append(k.user)
        lista_risposte.append(k.item1)
        lista_risposte.append(k.item2)
        lista_risposte.append(k.item3)
        lista_risposte.append(k.item4)
        lista_risposte.append(k.item5)
        myreplies.append(lista_risposte)
    if faimedia==False: 
        return lista_risposte
    if faimedia==True:
        replies_media=list(map(mean, zip(*myreplies)))
        #print replies_media
        return replies_media
@csrf_protect  
def endpage (request):
    assi=[]
    session_results=[]
    nomefile=[]
    uni_replies=[]
    urlimages=['NA','NA','NA','NA','NA']
    sessione=request.GET.get("session")
    UserID=request.GET.get("user")
    #controlliamo che la sessione sia chiusa
    #if not Session.objects.get(hash=sessione).chiusa: 
    #    return redirect (request,'wait.html',{"sessione":sessione,"utente":UserID}
    for a in range (0,5):
        nomefile="user"+UserID+"sessione"+sessione+"_Q"+str(a)+".jpg"
        if os.path.isfile(nomefile): 
            #print "we got "+nomefile
            urlimages[a]=nomefile
    #print "ecco le domande che esistono"
    #print urlimages       
    
    admin_object=Admindata.objects.get(id=1)
    employer_means=json.loads(admin_object.employer_averages)
    uni_means=json.loads(admin_object.uni_averages)

    ###formato dataset: 
#    df = pd.DataFrame({
#    'group': ['Ses','Uni','Employer','D'],
#    'skill1': [38, 1.5, 30, 4],
#    'skill2': [29, 10, 9, 34],
#    'skill3': [8, 39, 23, 24],
#    'skill4': [7, 31, 33, 14],
#    'skill5': [28, 15, 32, 14]
#    })
    for a in range (0,5):
        #controlliamo che il file non esista già:
    #creiamo un array (lista di liste) con le risposte
    #OCCHIO CHE LE ID DI QUESTION e REPLIES non partono da 0
        skill_list=Skill.objects.filter(question_id=6+a).values_list('question_text',flat=True)
        assi.append(list(skill_list)) #lista dei testi delle domande
        #print skill_list
    #2: le sue risposte 
        session_means_query=Risposta.objects.filter(session=sessione,questionId=a,user=UserID)
        sessionmeans=get_replies(session_means_query,False)
        #print sessionmeans
        session_results.append(sessionmeans)
        
    #print session_results
    try:
        for k in range (0,5):
            domande=[x[0].encode('utf-8') for x in Question.objects.all().values_list('question_text')]
            if urlimages[k]=="NA":
                results2={'Group':['UNI','TU','EMPLOYER']}
                for b in range (0,5):
                    results2[assi[k][b][:10]]=[6-uni_means[k][b],6-session_results[k][b],6-employer_means[k][b]]       
                results=pd.DataFrame.from_dict(results2)
                cols=results.columns.tolist()
                differences=[1-spatial.distance.cosine(session_results[k], employer_means[k]),1-spatial.distance.cosine(session_results[k], uni_means[k])]
                #portiamo la colonna "group" in apertura
                cols.insert(0, cols.pop(cols.index('Group')))
                results=results[cols]
                #print results.head()
                urlimages[k]=("user"+str(UserID)+"sessione"+sessione+"_Q"+str(k)+".jpg")           
                try: 
                    spiderplot(results,urlimages[k],differences)
                except IOError as e:
                    print(e.errno)
                    print(e) 
            else: 
                print"we have this graph already"
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)        
    return render(request,"mostragrafici_ind.html",{"imgs":urlimages,"questions":domande,"session":sessione,"userid":UserID})

def mostragrafici(request):    
    assi=[]
    session_results=[]
    uni_replies=[]
    urlimages=[]
    sessione=request.GET.get("session")
    t=Session.objects.get(hash=sessione)
    t.chiusa=True
    t.save()
    admin_object=Admindata.objects.get(id=1)
    employer_means=json.loads(admin_object.employer_averages)
    uni_means=json.loads(admin_object.uni_averages)
    #print uni_means[1]
    #print employer_means[1]
    ###formato dataset: 
#    df = pd.DataFrame({
#    'group': ['Ses','Uni','Employer','D'],
#    'skill1': [38, 1.5, 30, 4],
#    'skill2': [29, 10, 9, 34],
#    'skill3': [8, 39, 23, 24],
#    'skill4': [7, 31, 33, 14],
#    'skill5': [28, 15, 32, 14]
#    })
    try:
        for a in range (0,5):
          #  print a
        #creiamo un array (lista di liste) con le risposte
        #OCCHIO CHE LE ID DI QUESTION e REPLIES non partono da 0
            skill_list=Skill.objects.filter(question_id=6+a).values_list('question_text',flat=True)
            assi.append(list(skill_list)) #lista dei testi delle domande
        #2: le risposte della sua sessione
            session_means_query=Risposta.objects.filter(session=sessione,questionId=a)
            sessionmeans=get_replies(session_means_query,True)
            session_results.append(sessionmeans)
           # print "skill list"
           # print skill_list
            #print session_results
            #print assi
        #print assi[0].values_list(flat=True)
        for k in range (0,5):
            results2={'Group':['UNI','SESSION','EMPLOYER']}
            for b in range (0,5):
                emplodiff=6-employer_means[k][b]
                sessdiff=6-session_results[k][b]
                unidiff=6-session_results[k][b]
                results2[assi[k][b][:10]]=[unidiff,sessdiff,emplodiff]
            differences=[1-spatial.distance.cosine(session_results[k], employer_means[k]),1-spatial.distance.cosine(session_results[k], uni_means[k])]
            #print differences
            
            results=pd.DataFrame.from_dict(results2)
            cols=results.columns.tolist()
            #portiamo la colonna "group" in apertura
            cols.insert(0, cols.pop(cols.index('Group')))
            results=results[cols]
            #print results.head()
            urlimages.append("/media/graphs/"+sessione+"_Q"+str(k)+".jpg")
            spiderplot(results,urlimages[k],differences)
            #prendiamo tutte le domande e le serviamo poi al template
            domande=[x[0].encode('utf-8') for x in Question.objects.all().values_list('question_text')]
    except Exception as e:  
        print "errore è:"
        PrintException()
    return render (request,"mostragrafici.html",{"imgs":urlimages,'questions':domande})

def spiderplot(df,urlimage,differences):
    try:
            # ------- PART 1: Create background
           # Set data
    
         
         
         
        # ------- PART 1: Create background
         
        # number of variable
        categories=list(df)[1:]
        N = len(categories)
         
        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        
        
        # Initialise the spider plot
        ax = plt.subplot(111, polar=True)
         
        # If you want the first axis to be on top:
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)
         
        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], categories)
         
        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([1,2,3,4,5], ["1","2","3","4","5"], color="grey", size=7)
        plt.ylim(0,6)
         
         
        # ------- PART 2: Add plots
         
        # Plot each individual = each line of the data
        # I don't do a loop, because plotting more than 3 groups makes the chart unreadable
         
        # Ind1
        values=df.loc[0].drop('Group').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=df.loc[0]['Group']+'{:.1%}'.format(differences[1]))
        ax.fill(angles, values, 'b', alpha=0.1)
         
        # Ind2
        values=df.loc[1].drop('Group').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=df.loc[1]['Group'])
        ax.fill(angles, values, 'r', alpha=0.1)
        
        # Ind2
        values=df.loc[2].drop('Group').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, linestyle='solid', label=df.loc[2]['Group']+'{:.1%}'.format(differences[0]))
        ax.fill(angles, values, 'y', alpha=0.1)
         
        # Add legend
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        try: 
            img_data=io.BytesIO()
            plt.savefig(img_data,format='png')
            img_data.seek(0)
            conn = boto.connect_s3(aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            host='ams3.digitaloceanspaces.com')
            bucket = conn.get_bucket('careerspace')
            bucket.put_object(Body=img_data, ContentType='image/png', Key=urlimage)



            plt.gcf().clear()
        except Exception as e:
            print "erore interno"
            print e
        return plt
    except Exception as e:
        print "errore esterno"
        print e 
        img=Image.open('/media/graphs/Error-image.jpg')
        return img
from django.utils.translation import ugettext as _
