from django.urls import path

from django.contrib.auth.decorators import login_required

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    # path('list/', views.task_list, name='list'),
    # path('list/', login_required(views.TaskListView.as_view()), name='list'),

    # path('list/', views.TaskListView.as_view(), name='list'),
    
    path("list/", views.tasks_by_tag, name="list"),
    path("list_by_tag/tag/<slug:tag_slug>", views.tasks_by_tag, name="list_by_tag"),

    # path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('delete/<int:task_id>/', views.DeleteTaskView.as_view(), name='delete_task'),
    path('delete/<int:task_id>/<str:tag_slug>', views.DeleteTaskView.as_view(), name='delete_task_tag'),


    # path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('complete/<int:task_id>/', views.CompleteTaskView.as_view(), name='complete_task'),

    # path('create/', views.create_task, name='create_task'),
    path('create/', views.CreateTaskView.as_view(), name='create_task'),

    path("details/<int:pk>/", views.TaskDetailsView.as_view(), name="details"),

    path("edit/<int:pk>/", views.TaskEditView.as_view(), name="edit"),

    path('export/', views.TaskExportView.as_view(), name='export'),
    path('export/<str:tag_slug>/', views.TaskExportView.as_view(), name='export_by_tag'),

    path('import-from-trello/', views.ImportFromTrello.as_view(), name='trello_import'),


    # path('add-task/', views.add_task, name='add_task'),
    path('publisher/', views.PublisherView.as_view(), name='publisher'),
    path('publisher/<int:id>/', views.PublisherView.as_view(), name='publisher'),
]
