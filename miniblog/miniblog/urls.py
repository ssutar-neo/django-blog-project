from django.contrib import admin
from django.urls import path
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('addpost/', views.add_post, name='addpost'),
    # Read post in dashboard url
    path('updatepost/<int:id>', views.update_post, name='updatepost'),
    path('deletepost/<int:id>', views.delete_post, name='deletepost'),
    path('add_comments/<int:post_id>', views.add_comments, name='add_comments'),
]
