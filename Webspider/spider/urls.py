from django.urls import path
from spider import views


urlpatterns = [
    # path('', views.index, name= 'home'),
    path('', views.linkview, name='results')
]