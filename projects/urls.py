from django.urls import path, include
from . import views

urlpatterns = [
  path('signup/', views.signup, name='signup'),
  path('account/', include('django.contrib.auth.urls')),
  path('',views.index,name='index'),
  path('profile',views.profile,name='profile'),
  path('update_profile',views.update_profile,name='update_profile'),
  path('post_project',views.post_project,name='newProject'),
  path('project',views.project,name='project'),
]