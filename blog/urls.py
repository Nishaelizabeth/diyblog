from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('bloggers/', views.BloggerListView.as_view(), name='bloggers'),
    path('blogger/<int:pk>', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('blog/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('blog/<int:pk>/like/', views.like_blog, name='like-blog'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('blog/create/', views.create_blog, name='create-blog'),
]
