from django.conf.urls import url
from django.conf.urls.static import static
from . import views
from django.conf import settings
from django.conf.urls import include
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^question1/$', views.question1, name='question1'),
    url(r'^question2/$', views.question2, name='question2'),
    url(r'^question3/$', views.question3, name='question3'),
    url(r'^question4/$', views.question4, name='question4'),
    url(r'^question5/$', views.question5, name='question5'),
    url(r'newsession/$', login_required(views.newsession_form.as_view()),name='newsession'),
    url('^newuser$',views.newuser,name='newuser'),
    url('show_qr/$',views.show_qr_view,name='show_qr'),
    url(r'^start_session/$',views.start_session,name="start_session"),
    url(r'^sessionclosed$',views.sessionclosed,name="sessionclosed"),
    url(r'^process/$',views.process,name="process"),
    url(r'^endpage$',views.endpage,name="endpage"),
    url(r'^mostragrafici$',views.mostragrafici,name="mostragrafici"),
    url(r'^processautente/$', views.newuserprocess, name='newuserprocess'),
    url('^', include('django.contrib.auth.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)