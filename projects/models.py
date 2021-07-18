from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    profile_pic =  CloudinaryField('image')
    bio = models.TextField()
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    location = models.CharField(max_length=60, blank=True)
    contact = models.CharField(max_length=10,blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        return self.save()

    def delete_profile(self):
        return self.delete()

class Project(models.Model):
    photo =  CloudinaryField('image')
    title = models.CharField(max_length=50)
    description = models.TextField()
    link = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    technologies = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.title

    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()    

    @classmethod
    def get_all_projects(cls):
        projects = Project.objects.all()
        return projects

    @classmethod
    def get_project_by_id(cls,id):
        project = Project.objects.filter(id=id).first()
        return project

    @classmethod
    def get_project_by_user(cls,user_id):
        projects = Project.objects.filter(user_id=user_id)
        return projects

    @classmethod
    def search_project(cls,search_term):
        projects = Project.objects.filter(project_title__icontains=search_term).all()
        return projects


class Rating(models.Model):
    rating = (1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6),(7, 7),(8, 8),(9, 9),(10, 10)

    design = models.IntegerField(choices=rating,blank=True,default=0)
    usability = models.IntegerField(choices=rating, blank=True,default=0)
    content = models.IntegerField(choices=rating, blank=True,default=0)
    overall_score = models.IntegerField(blank=True,default=0)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f'{self.project.project_title} ratings'
