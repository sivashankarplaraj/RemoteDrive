from django.urls import path
from . import views

urlpatterns = [
    path('init-upload', views.InitUploadView.as_view(), name='init-upload'),
    path('commit', views.CommitView.as_view(), name='commit'),
]
