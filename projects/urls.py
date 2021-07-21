from django.urls import path, include
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [

  path('accounts/register/',views.register,name='register'),
  path('accounts/login/',auth_views.LoginView.as_view(template_name = 'registration/login.html'),name='login'),
  path('',views.index,name='index'),
  path('accounts/profile/',views.profile,name='profile'),
  path('update_profile',views.update_profile,name='update_profile'),
  path('post_project',views.post_project,name='newProject'),
  path('project/<project_id>',views.project,name='project'),
  path('rate/<project_id>',views.rate,name='rate'),
  path('api/profile/',views.ProfileList.as_view()),
  path('api/project/',views.ProjectList.as_view()),
] 