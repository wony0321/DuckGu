from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.follow_user),
    path('profile/<str:user_name>/', views.userInfo),
]
