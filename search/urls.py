from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': r'C:\Users\bit\Boogle\search\images'}),
]