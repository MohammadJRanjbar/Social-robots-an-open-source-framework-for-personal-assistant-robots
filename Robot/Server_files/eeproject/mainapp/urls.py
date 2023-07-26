from django.urls.conf import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('setspeed',views.setspeed,name='setspeed'),
    path('setangularcam',views.setangularcam,name='setangularcam'),
    path('lincammov',views.lincammov,name='lincammov'),
]