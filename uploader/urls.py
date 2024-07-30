from django.urls import path
from . import views

urlpatterns = [
     path('', views.welcome, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('start_prediction/', views.start_prediction, name='start_prediction'),
    path('predicted_data/', views.predicted_data, name='predicted_data'),
]
