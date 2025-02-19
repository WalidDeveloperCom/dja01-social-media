from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('like-post/', views.like_post, name='like_post'),
    path('add-comment/', views.add_comment, name='add_comment'),
    path('share-post/<int:post_id>/', views.share_post, name='share_post'),
]

