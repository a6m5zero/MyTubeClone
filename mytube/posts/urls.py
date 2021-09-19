from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name = 'index'), 
    path('community/<slug:slug>/', views.group_posts , name = 'community_posts'),
    path('contact/', views.user_contact, name='user_contact'),
    path('new/', views.add_new_post, name='add_new_post'),
]

# Взаимодействие с юзверем и его постами
urlpatterns += [
    path("follow/", views.follow_index, name="follow_index"),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path('<str:username>/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('<str:username>/<int:post_id>/add_comment/', views.add_comment, name='add_comment'), 
    path("<str:username>/follow/", views.profile_follow, name="profile_follow"), 
    path("<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),
]