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

class OrderView(TemplateView):
    template_name = 'basic_app/order.html'

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

def profile(request,pk,username):
    user_info = UserProfileInfo.objects.filter(user = request.user)[0]

    return render(request,'basic_app/profile.html',{'user_info':user_info})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



def register(request):

    registered = False


    if request.method == "POST":
        user_form = UserCreateForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save


            profile = profile_form.save(commit=False)
            profile.user = user



            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']


            profile.save()


            registered = True
        else:
            print(user_form.errors,profile_form.errors)


    else:
        user_form = UserCreateForm()
        profile_form = UserProfileInfoForm()

    return render (request,'basic_app/registration.html',
                    {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered' : registered})



def user_login(request):


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)


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


    else:
        return render(request,'basic_app/login.html',{})
