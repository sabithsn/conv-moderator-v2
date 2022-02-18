from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update_db/', views.update_db, name='update_db'),
    path('export/', views.export_db, name='export_db'),


]