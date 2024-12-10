from django.urls import path
from .views import (
    FacebookLoginView,
    FacebookCallbackView,
    FacebookPostsView,
    LikePostView,
    CommentOnPostView,
    SharePostFacebookView,
)

urlpatterns = [
    path("fblogin/", FacebookLoginView.as_view(), name="facebook_login"),
    path("fbcallback/", FacebookCallbackView.as_view(), name="facebook_callback"),
    path("facebook/posts/", FacebookPostsView.as_view(), name="facebook-posts"),
    path("facebook/posts/like/", LikePostView.as_view(), name="like-post"),
    path(
        "facebook/posts/comment/", CommentOnPostView.as_view(), name="comment-on-post"
    ),
    path(
        "facebook/posts/share/",
        SharePostFacebookView.as_view(),
        name="share-post-facebook",
    ),
]
