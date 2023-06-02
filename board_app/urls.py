from django.urls import path
from .views import *

urlpatterns = [
    path('', PostList.as_view(), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('my/', MyPosts.as_view(), name='my_posts'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
    path('<int:pk>/response/', CreateResponse.as_view(), name='make_response'),
    path('response/detail/<int:pk>', DetailResponse.as_view(), name='detail_response'),
    path('response/detail/<int:pk>/delete', ResponseDelete.as_view(), name='response_delete'),
    path('response/<int:pk>/accept/', accept_response, name='accept'),
    path('sendnews', SendEmail.as_view(), name='send_news')
]
