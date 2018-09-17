from __future__ import division
from django import forms
from django_range_slider.fields import RangeSliderField
import datetime
import json
import numpy as np
import boto3
import io
from bootstrap_datepicker.widgets import DatePicker
from django.forms import ModelForm
from .models import Session,Admindata,User,Risposta
from PIL import Image
import qrcode
import tinyurl
#import matplotlib.pyplot as plt
#import pandas as pd
#from math import pi
host_url='http://104.248.46.248:8000'
ACCESS_KEY = 'RPIBQG3DPFHSGPEKIXSI'
SECRET_KEY = 'e+SvUUoKa3S61BF020aOzOmvRFZz3MRb7YfmytlTiEs'


ora = datetime.datetime.now()
anno=ora.year
giorno=ora.day
mese=ora.month


def mean(a):
    return sum(a) / len(a)


class NameForm( forms.Form ): 
    scelte=[(x,x) for x in range (ora.year-100,anno)]
    yob=forms.ChoiceField(choices=scelte,label="Anno di Nascita",initial=ora.year-20, required=True)
    gender=forms.ChoiceField(choices=[('F','Femmina'),('M','Maschio'),('N','Non Rispondere')],label="Sesso", required=True)

def get_replies(qset): #qset un queryset; la funzione restituisce una lista di liste con le risposte
    myreplies=[]
    for k in qset:
        lista_risposte=[]
        lista_risposte.append(k.item1)
        lista_risposte.append(k.item2)
        lista_risposte.append(k.item3)
        lista_risposte.append(k.item4)
        lista_risposte.append(k.item5)
        myreplies.append(lista_risposte)
    return myreplies
      

  
class SessionForm( ModelForm ):
    class Meta:
        model=Session
        fields=['data','tipologia','note','hash']
        hash=forms.CharField(max_length=128)
        TIPO_CHOICES=(('','Seleziona una tipologia'),('UNI','Universita'),('AZI','Azienda'),('IST','Istituzioni'))
        widgets={'data': forms.DateInput(attrs={'class': 'datepicker'}),'tipologia':forms.Select(choices=TIPO_CHOICES,attrs={'class':'form-control'}),}
    def process_session(self):
        uni_replies=[]
        emplo_sessions_id=[]
        employer_replies=[]
        uni_sessions_id=[]
        id=self.cleaned_data.get("hash")
        latestsession=Session.objects.filter(hash=id)[0]
        print "sessione numero"+id+"creata"
        qr = qrcode.QRCode(
                           version = 1,
                           error_correction = qrcode.constants.ERROR_CORRECT_H,
                           box_size = 10,
                           border = 4,
                           )

        data=host_url+'/start_session/?session='+id
        qr.add_data(data)
        qr.make(fit=True)
        # Create an image from the QR Code instance
        img = qr.make_image()
        img_data=io.BytesIO()
        img.save(img_data)
        img_data.seek(0)
        session = boto3.session.Session()
        client = session.client('s3',
        region_name='ams3',
        endpoint_url='https://ams3.digitaloceanspaces.com',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY)
        s3 = boto3.resource('s3')
        client.put_object(Body=img_data, Bucket="careerspace",ContentType='image/png', Key=id+'.png')
        #img.save('./media/qrcodes/'+id+'.jpg')
        latestsession.qrcode=id+'.png'
        latestsession.save()
        #CALCOLIAMO LE MEDIE DEGLI EMPLOYER CHE STOREREMO POI NEL DATABASE PER USO FUTURO
        #anzitutto troviamo le sessioni relative a emplyer e uni        
        emplo_sessions_id=Session.objects.all().exclude(tipologia="UNI").values('hash')
        print emplo_sessions_id
        uni_sessions_id=Session.objects.filter(tipologia="UNI").values('hash')
        print uni_sessions_id

        for a in range (0,5):
            empquery=Risposta.objects.filter(session__in=emplo_sessions_id, questionId=a)
            print empquery
            employer_replies.append(np.mean(np.array(get_replies(empquery)),axis=0).tolist())
            uniquery=Risposta.objects.filter(session__in=uni_sessions_id, questionId=a)
            print uniquery

            uni_replies.append(np.mean(np.array(get_replies(Risposta.objects.filter(session__in=uni_sessions_id, questionId=a))),axis=0).tolist())
        
        
        admin_record=Admindata.objects.get(id=1)
        employer_averages=json.dumps(employer_replies)
        print employer_averages
        uni_averages=json.dumps(uni_replies)
        print uni_averages

        admin_record.employer_averages=employer_averages
        admin_record.uni_averages=uni_averages
        admin_record.save()        
        pass
