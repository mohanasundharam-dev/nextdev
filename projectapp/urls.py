from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('main/',views.main,name="main"),
    path('project/<str:i>/', views.projects, name='project'),
    path('CreateProject/', views.CreateProject,name='CreateProject'),
    path('update_project/<str:i>', views.UpdateProject,name='update_project'),
    path('delete_project/<str:i>', views.DeleteProject,name='delete_project')
]
