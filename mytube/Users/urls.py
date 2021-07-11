from django.urls.conf import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup')
]