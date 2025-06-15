from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),  
    path('create/', views.create_post, name='create_post'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('users/', views.user_list_view, name='user_list'),
    path('feed/', views.feed_view, name='feed'),
]

