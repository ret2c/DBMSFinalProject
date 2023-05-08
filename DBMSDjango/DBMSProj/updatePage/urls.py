from django.urls import path
from . import views

urlpatterns = {
    path('updateContent/', views.updateContent, name='update-content')
}