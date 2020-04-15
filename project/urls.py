from django.urls import path
from . import views

app_name = "project"

urlpatterns = [
    path('', views.index, name="home"),
    path('create-project/', views.create_project, name="create-project"),
    path('project/<int:pk>/', views.project_page, name="project-page"),
    path('project/<int:project_pk>/table/', views.table_view, name="table-view"),
    path('project/<int:project_pk>/table/<int:table_pk>/', views.table_view, name="table-view"),
    path('project/<int:project_pk>/table/<int:table_pk>/add-entry/', views.add_entry, name="add-entry"),
    path('project/<int:project_pk>/table/<int:table_pk>/fields/', views.add_field, name="add-field"),
]