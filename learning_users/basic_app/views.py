from django.shortcuts import render
from django.views.generic import (View, TemplateView, ListView,
                                        DetailView,CreateView,
                                        UpdateView,DeleteView)
from basic_app.forms import UserCreateForm, UserProfileInfoForm, ObjectForm


from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from basic_app.forms import UserCreateForm, UserProfileInfoForm
from django.urls import reverse_lazy
# NEW
from .models import UserProfileInfo, Object

from django.contrib.auth import get_user_model
User = get_user_model()

def index(request):
    return render(request,'basic_app/index.html')

class ObjectListView(ListView):
    model = Object


class ObjectDetailView(DetailView):
    model = Object

class CreateObjectView(LoginRequiredMixin,CreateView):
    login_url = '/basic_app/login'
    # redirect_field_name = 'xxxxx_detail.html'
    form_class = ObjectForm
    model = Object
    success_url = reverse_lazy('basic_app:object_list')

class ObjectUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/basic_app/login'
    # redirect_field_name = 'xxxxx_detail.html'
    form_class = ObjectForm
    model = Object

class ObjectDeleteView(LoginRequiredMixin,DeleteView):
    login_url = '/basic_app/login'
    model = Object
    success_url = reverse_lazy('basic_app:object_list')

# NEW
# def profile(request):
#     profile_pic = UserProfileInfo.objects.all()
#     return render(request,'basic_app/profile.html',{'profile_pic':profile_pic})
#     # Is it correct to use the context dictionary like this?

# Abu code:

def profile(request,pk,username):
    user_info = UserProfileInfo.objects.filter(user = request.user)[0]
    # # user_info = UserProfileInfo.objects.all()
    # user_info = UserProfileInfo.portfolio_site
    # user_info = UserProfileInfo.profile_pic

    return render(request,'basic_app/profile.html',{'user_info':user_info})

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(
    #         user__username__iexact=self.kwargs.get("username")
    #     )


# My modified code:

# def profile(request,*pk,user):
#     user_info = UserProfileInfo.objects.filter(user=request.user)[0]
#     return render(request,'basicapp/profile.html',{'user_info':user_info})

# def profile(request,*pk):
#     user = UserProfileInfo.objects.get(pk=pk)
#     user_info = UserProfileInfo.objects.filter(user=request.user)[0]
#     return render(request,'basicapp/profile.html',{'user_info':user_info})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# class RegisterView(CreateView):
#     form_class = UserCreateForm
#     success_url = reverse_lazy("login")
#     template_name = "basic_app/registration.html"

#Old code

# from django.shortcuts import render
# from basic_app.forms import UserForm, UserProfileInfoForm
#
# from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponseRedirect, HttpResponse
# from django.urls import reverse
# from django.contrib.auth.decorators import login_required
#
# # Create your views here.
#
# def index(request):
#     return render(request,'basic_app/index.html')
#
# def profile(request):
#     return render(request,'basic_app/profile.html')
#
# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('index'))
#
#     #pass in a request to the built in logout function, which automatically
#     #logs out the user. Simple except for one thing - we want to make sure
#     #only a user that is logged in can log out - so we need the decorator
#     # directly above the function
#
def register(request):

    registered = False

    # Note that the name 'register' in line 8 is the name of the view.
    # When we set registered = False, we assume that they are not registered.
    # If the request.method = POST, we grab the info from the forms

    if request.method == "POST":
        user_form = UserCreateForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

    # The user_form matches the variable we are going to send back with
    # the context dictionary (grabs information from the user form)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save

        # The above grabs the user form, hashes the password i.e.
        # goes into your settings.py file and sets it as the hash
        # These changes are then saved to the user

            profile = profile_form.save(commit=False)
            profile.user = user

        # Don't want to commit to the database yet as may get collisions
        # where it wants to overwrite the user. Profile.user = user sets up
        # one to one relationship.

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

        # You use similar tactics when using other types of files, use
        # request.FILES. You will be dealing with the key ('profile_pic')
        # based on what you defined in the models.
        # If the profile pic in request.FILES, we will set the attribute
        # profile_pic equal to the profile pic as in the request.FILES 'dictionary'

            profile.save()

        # If they have done all of this, i.e. bpth forms are valid, saved the
        # user and their profile and set up the picture. Then set 'registered' = true
        # i.e. the registration was successful or print out the error.

            registered = True
        else:
            print(user_form.errors,profile_form.errors)



        # The below else, the request is not a http request i.e. nothing was posted
    else:
        user_form = UserCreateForm()
        profile_form = UserProfileInfoForm()

    return render (request,'basic_app/registration.html',
                    {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered' : registered})

    # Note that you have used 'user_form', 'profile_form' and 'registered' in the
    # registration.html file. Therefore these need to be passed into a context
    # dictionary in the views.py file.


def user_login(request):

    # Note that Django may complain if you decide to call your view
    # 'login' and you are also importing 'login' at the top of views.py
    # dont call a view just 'login', 'authenticate', 'logout' etc

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        # The above authenticates the user in one line of code
        # The below works if the user is authenticated

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied!")

#         # Once the user is logged in, we return them to a page
#         # i.e.Whatever is specified after the 'return' entry
#         # Redirect(reverse('index')) does the following:
#             #if they login and are successful, it will reverse and
#             #redirect back to homepage. if not, the page will
#             #return 'ACCOUNT NOT ACTIVE'
#         #If the user is not authenticated, the above will be printed
#         #to the console and 'Invalid login details supplied' will be returned.
#
    else:
        return render(request,'basic_app/login.html',{})

# #The last 'else' means the request.method wasnt equal to post
# #so they haven't actually submitted anything, it will take
# #them back to login page
