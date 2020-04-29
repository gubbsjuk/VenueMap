''' App URLs '''
from django.urls import path
from vm_app import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('venues/', views.venues_view, name='venues_view'),
    path('<int:pk>/', views.imgmap_view, name='imgmap_view'),
    path('room_detail/', views.room_detail, name='room_detail'),
    path('room_create/', views.room_create_view, name='room_create_view'),
    path('room_create_coordinates/', views.room_create_coordinates_view, name='room_create_coordinates'),
    path('room_manage/', views.room_manage_view, name='room_manage_view'),
    path('room_list/', views.room_list_view, name='room_list_view'),
]
