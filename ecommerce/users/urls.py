from django.urls import path

 #creating url paths for calling the views
from . import views

urlpatterns = [
    #empty string for base url


    path('index/', views.index, name='users'),

]

