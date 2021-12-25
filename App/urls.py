from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',views.AmazonScraper,name='index'),
    path('fetchProducts',views.fetchProducts,name = 'fetchProducts'),
    path('delete',views.delete,name='delete'),  
]
urlpatterns += staticfiles_urlpatterns()