from django.urls import path, include
from . import views
from django.conf import settings

urlpatterns = [
  path('signup/', views.signup, name='signup'),
  path('account/', include('django.contrib.auth.urls')),
  path('',views.index,name='index'),
  path('profile/<username>',views.profile,name='profile'),
  path('update_profile',views.update_profile,name='update_profile'),
  path('post_project',views.post_project,name='newProject'),
  path('project/<project_id>',views.project,name='project'),
  path('rate/<project_id>',views.rate,name='rate'),
  path('api/profile/',views.ProfileList.as_view()),
  path('api/project/',views.ProjectList.as_view()),
] 