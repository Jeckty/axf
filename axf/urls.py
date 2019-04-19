from django.urls import path, re_path
from .import views
app_name ='[axf]'
urlpatterns = [

    re_path(r'^home/$', views.home,name="home"),
    re_path(r'^market/(\d+)/(\d+)/(\d+)/$', views.market,name="market"),
    re_path(r'^cart/$', views.cart,name="cart"),
    re_path(r'^mine/$', views.mine,name="mine"),
]