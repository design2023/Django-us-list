from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns =[
    path('',views.getData),
    path('get-transactions',views.getTransactions),
    path('add/',views.addUser),
    path('upload/', views.postFile, name='file-upload'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
