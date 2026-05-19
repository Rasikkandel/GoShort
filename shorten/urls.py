from django.urls import path 
from . import views
urlpatterns = [ 
    path("<path:long_url>", views.makeshort) 
]