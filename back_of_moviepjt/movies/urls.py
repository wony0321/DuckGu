from django.urls import path
from . import views


urlpatterns = [
    path('meet/', views.meet),
    path('joined_meets/', views.joined_meets),
    path('join_meet/<int:meet_id>/', views.join_or_leave_meet),
    path('meet/<int:meet_id>/', views.meet_detail),
    path('movie/', views.movie_list),
    path('movie/<int:movie_pk>/', views.movie_detail),
    path('movie/<int:movie_pk>/like/', views.movie_like),
    path('movie/<int:movie_pk>/review/', views.reiview_list),
    path('movie/<int:movie_pk>/review/<int:review_pk>/', views.review_detail),
]
