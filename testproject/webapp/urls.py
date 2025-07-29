# webapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='home'),  # 기본 URL을 회의실 목록으로
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('rooms/<int:room_id>/reserve/', views.make_reservation, name='make_reservation'),
    path('reservations/<int:reservation_id>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservations/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),
    
]

