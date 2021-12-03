from django.urls import path
from . import views

urlpatterns = [
    path('automated', views.automated, name='automated'),
    path('custom', views.custom, name='custom'),
    path('pre_trained', views.pre_trained, name='pre_trained'),
    path('classify', views.classify, name='classify'),
    path('automated_classify', views.automated_classify, name='automated_classify'),
    #path('download', views.download, name='download'),
    #path('create_zip', views.create_zip, name='create_zip'),
    #path('open_file', views.open_file, name='open_file'),
]