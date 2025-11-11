from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('students/', views.students_list, name='students_list'),
    path('reports/', views.reports, name='reports'),
    path('files/', views.files_list, name='files_list'),
    path('files/view/<str:filename>', views.file_view, name='file_view'),
    path('files/delete/<str:filename>', views.file_delete, name='file_delete'),
]
