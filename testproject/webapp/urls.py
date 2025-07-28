# webapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rooms/', views.room_list, name='room_list'),
    # 이후에 회의실 목록 URL 추가 예정
]

