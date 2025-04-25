from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_audio, name='upload_audio'),
    path('my-files/', views.my_audio_files, name='my_audio_files'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('audio/<str:audio_id>/', views.audio_detail, name='audio_detail'),
    path('audio/<str:audio_id>/edit/', views.edit_audio, name='edit_audio'),
    path('audio/<str:audio_id>/delete/', views.delete_audio, name='delete_audio'),
    path('about/', views.about, name='about'),
    path('media/audio/<str:audio_id>/', views.serve_audio, name='serve_audio'),
    path('media/profile-image/<str:profile_id>/', views.serve_profile_image, name='serve_profile_image'),
]