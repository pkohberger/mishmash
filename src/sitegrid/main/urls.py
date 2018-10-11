#from django.conf.urls import *
from django.urls import re_path


from main import views


urlpatterns = [

    # Admin Views
    
    # Admin Ajax Views
    

    # Views

    #url(r'^404/$', views.test_404, name='test_404'),
    
    #url(r'^500/$', views.test_500, name='test_500'),

    #url(r'^global-search/$', views.global_search, name='global_search'),
    
    # url(r'^login/$', views.user_login_page, name='login'),

    re_path(r'^$', views.home, name='home'),

    re_path(r'^about/$', views.about, name='about'),
    
    re_path(r'^add-credential/$', views.add_cred, name='main_add_cred'),

]