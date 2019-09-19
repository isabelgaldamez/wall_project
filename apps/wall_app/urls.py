from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.registration),
    url(r'^authenticate$', views.auth_user),
    url(r'^success$', views.user_logged),
    url(r'^new_post$', views.new_post),
    url(r'^comment$', views.post_comment),
    url(r'^delete_message$', views.delete_message),
    url(r'^clear_session$', views.clear_session),
]