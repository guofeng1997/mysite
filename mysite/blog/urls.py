from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('posts/', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('posts/', views.PostListView.as_view(),),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='detail'),
    path('<int:post_id>/share.html/', views.post_share, name='post_share')

]
