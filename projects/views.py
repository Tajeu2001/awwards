from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Profile,Project,Rating
from .forms import SignUpForm,UpdateUserForm,UpdateProfileForm,PostProjectForm,RatingForm
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.http import Http404,HttpResponseRedirect, JsonResponse
from django.views.generic import RedirectView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def index(request):
    title = "Awwards"
    current_user = request.user
    projects = Project.get_all_projects()
    return render(request, 'index.html',{'title':title,'current_user':current_user,'projects':projects})


@login_required(login_url='login')
def profile(request, username):
    return render(request, 'profile.html')


def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    params = {
        'user_prof': user_prof,
    }
    return render(request, 'profile.html', params)

@login_required(login_url='login')
def update_profile(request):
    current_user = request.user
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST,instance=request.user)
        profile_form = UpdateProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile',id=current_user.id)

    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    
@login_required(login_url='login')
def post_project(request):
    current_user = request.user
    if request.method == 'POST':
        project_form = PostProjectForm(request.POST,request.FILES)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.user = current_user
            project.save()
        return redirect('index')
    else:
        project_form = PostProjectForm()

    title = 'New Project'
    return render(request,'new_project.html',{'title':title,'project_form':project_form,'current_user':current_user})


@login_required(login_url='/login/')
def project(request,project_id):
    current_user = request.user
    project = Project.objects.filter(id=project_id).first()
    ratings = Rating.objects.filter(project_id=project_id)
    usability_rating = Rating.objects.filter(project_id=project_id).aggregate(Avg('usability'))
    content_rating = Rating.objects.filter(project_id=project_id).aggregate(Avg('content'))
    design_rating = Rating.objects.filter(project_id=project_id).aggregate(Avg('design'))

    title = f'{project.title} details'
    return render(request,'project.html',{'title':title,'project':project,'current_user':current_user,'ratings':ratings,'usability_rating':usability_rating,'content_rating':content_rating,'design_rating':design_rating})

@login_required(login_url='login')
def rate(request,project_id):
    current_user = request.user
    project = Project.objects.filter(id=project_id).first()
    if request.method == 'POST':
        rate_form = RatingForm(request.POST)
        if rate_form.is_valid():
            rating = rate_form.save(commit=False)
            rating.project = project
            rating.user = current_user
            rating.save()
            return redirect('project', project_id)
    else:
        rate_form = RatingForm()

    return render(request, 'rate.html',{'current_user':current_user,'rate_form':rate_form,'project':project})

class ProfileList(APIView):
    def get(self,request,format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)
        permission_classes = (IsAdminOrReadOnly,)
class ProjectList(APIView):
    def get(self,request,format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects,many=True)
        return Response(serializers.data)

