from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/post/<int:id>', views.post, name='post'),
    path('blog/category/<int:id>', views.category, name='category'),
    path('blog/search/', views.search, name='search'),
    path('blog/add_post/', views.add_post, name='add_post'),
    path('blog/post/<int:id>/add_comment/', views.add_comment, name='add_comment'),
    path('blog/post/<int:id>/delete/', views.delete_post, name='delete_post'),
    path('profile/<int:id>/usersposts/', views.users_posts, name='users_posts'),
    path('register/', views.register, name='register'),
]