from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('links/', views.links, name='links'),
    path('delete/<int:link_id>/', views.delete_link, name='delete_link'),
    path('<str:short_code>/', views.redirect_short, name='redirect_short'),
]