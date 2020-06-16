''' App URLs '''
from django.urls import path
from vm_app import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('venues/', views.venues_view, name='venues_view'),
    path('venues/<int:pk>/', views.imgmap_view, name='imgmap_view'),
    path('room_detail/', views.room_detail, name='room_detail'),
    path('room_create/', views.new_room_create_view, name='room_create_view'),
    path('room_manage/', views.room_manage_view, name='room_manage_view'),
    path('room_list/', views.room_list_view, name='room_list_view'),
    path('activity_create/', views.activity_create_view, name='activity_create_view'),
    path('profile/', views.profile_update_view, name='profile_update_view'),
    path('manage_users/', views.manage_users_view, name='manage_users_view'),
    path('edit_user/<int:pk>/', views.edit_user_view, name='edit_user_view'),
    path('change_client/<int:pk>', views.change_client, name='change_client'),
]
