from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('api/notices/', views.notice_api, name='notice_api'),
    path('notice-board/', views.notice_board, name='notice_board'),
    path('result/', views.search_result, name='search_result'), 

]