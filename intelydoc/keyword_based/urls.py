from django.urls import path
from . import views

urlpatterns = [
    path('keyword_based', views.keyword_based, name='keyword_based'),
    path('upload', views.upload, name='upload'),
    path('download', views.download, name='download'),
    path('create_zip', views.create_zip, name='create_zip'),
    path('duplicate', views.duplicate, name='duplicate'),
    path('reports', views.reports, name='reports'),
    path('view_reports', views.view_reports, name='view_reports'),
]