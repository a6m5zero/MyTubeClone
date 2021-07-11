from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'index'), 
    path('community/<slug:slug>/', views.group_posts , name = 'community_posts'),
    path('contact/', views.user_contact, name='user_contact'),
    path('new/', views.add_new_post, name='add_new_post'),
]