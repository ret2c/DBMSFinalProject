from django.urls import path
from . import views

urlpatterns = {
    # path('queries/', views.queries, name='queries'),
    # path('queries/', views.display_content, name='display_content'),
    # path('queries/', views.index, name='index'),
    path('updateContent/', views.updateContent, name='update-content')
    # path('queries/', views.display_content, name='queries')
    # path('queries/', views.display_content, name='display_content'),
    # path('queries/', views.index, name='index'),


}