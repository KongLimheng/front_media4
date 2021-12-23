from django.urls import path
from . import views

app_name = 'media4'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login-page'),
    path('signup/', views.signup, name='sign-up'),
    path('profile/<str:user_id>/', views.profile_page, name='profile'),
    path('verify-otp/', views.verify_otp, name='verify'),
    path('update_profile/', views.update_profile, name='profile_update'),
    path('post/', views.post_media, name='post'),
    path('new-feed/', views.feed, name='feed'),
    path('get_media/', views.get_media, name='context_media'),
    # path('*', views.notfound, name='notfound')
]


