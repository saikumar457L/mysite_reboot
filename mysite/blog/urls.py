from django.urls import path

from .views import post_detail,share_post
from .views import CreatePost,PostListView

from .feeds import LatestPostsFeed

app_name = "blog"

urlpatterns = [
    path("",PostListView.as_view(), name="post_list"),
    path("<int:object_id>/detail/",post_detail, name="post_detail"),
    path("new_post/",CreatePost.as_view(), name="new_post"),
    path("<int:object_id>/share/",share_post, name="post_share"),
    path("feed/",LatestPostsFeed(), name="post_feed"),
    


]
